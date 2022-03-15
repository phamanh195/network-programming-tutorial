import select
import socket
import queue
import time

HOST = '127.0.0.1'
PORT = 9432
TIMEOUT = 10000
PACKAGE_LENGTH = 10
SERVER_ADDR = (HOST, PORT)

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

lsock.bind(SERVER_ADDR)
lsock.listen()
lsock.setblocking(False)

fd_to_socket = {
    lsock.fileno(): lsock
}
message_queues = {}

READ_ONLY = (
    select.POLLIN |
    select.POLLPRI |
    select.POLLHUP |
    select.POLLERR
)
READ_WRITE = READ_ONLY | select.POLLOUT


poller = select.poll()
poller.register(lsock, READ_ONLY)


def accept_wrapper(sock: socket.socket):
    conn, addr = sock.accept()
    print(f'Accept connection from {addr}')
    conn.setblocking(False)
    fd_to_socket[conn.fileno()] = conn
    poller.register(conn, READ_WRITE)
    message_queues[conn] = queue.Queue()


def service_connection(conn: socket.socket, flag: int):
    if flag & select.POLLIN:
        data = conn.recv(PACKAGE_LENGTH)
        if data:
            print(f'Receive "{data}" from {conn.getpeername()}')
            message_queues[conn].put(data)
            poller.modify(conn, READ_WRITE)
        else:
            print(f'Closing {conn.getpeername()}')
            poller.unregister(conn)
            conn.close()
            del message_queues[conn]
    elif flag & select.POLLOUT:
        try:
            msg = message_queues[conn].get_nowait()
        except queue.Empty:
            print(f'{conn.getpeername()} queue empty')
            poller.modify(conn, READ_ONLY)
        else:
            print(f'Sending message {msg} to {conn.getpeername()}')
            conn.send(b'R:' + msg)
    elif flag & select.POLLHUP:
        print(f'Closing {conn.getpeername()}')
        poller.unregister(conn)
        conn.close()
    elif flag & select.POLLERR:
        print(f'Exception on {conn.getpeername()}')
        poller.unregister(conn)
        conn.close()
        del message_queues[conn]


while True:
    print(f'{time.time():.0f} Still going..')
    fd_events = poller.poll(TIMEOUT)
    for fd, flag in fd_events:
        sock = fd_to_socket[fd]
        if sock == lsock:
            accept_wrapper(lsock)
        else:
            service_connection(sock, flag)
