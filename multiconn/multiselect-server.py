import select
import socket
import queue


HOST = '127.0.0.1'
PORT = 9432
TIMEOUT = 10000
BACKLOG = 2
PACKAGE_LENGTH = 1024
SERVER_ADDR = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(SERVER_ADDR)
server.listen(BACKLOG)
server.setblocking(False)

inputs = {server, }
outputs = set()
message_queues = {}


def send_message(sender: socket.socket, message:  bytes):
    for conn, m_queues in message_queues.items():
        if conn == sender:
            continue
        m_queues.put(message)
        outputs.add(conn)


def logout(_conn: socket.socket):
    inputs.discard(_conn)
    outputs.discard(_conn)
    del message_queues[_conn]
    send_message(sender=_conn, message=f'{_conn.getpeername()} out chat room.\n'.encode())
    _conn.close()


while inputs:
    readable, writable, exeptional = select.select(
        inputs, outputs, inputs
    )

    for rsock in readable:
        if rsock is server:
            conn, addr = rsock.accept()
            conn.setblocking(False)
            inputs.add(conn)
            message_queues[conn] = queue.Queue()

            # notice room chat
            send_message(sender=conn, message=f'{conn.getpeername()} join chat room.\n'.encode())
        else:
            data = rsock.recv(PACKAGE_LENGTH)
            if data:
                send_message(sender=rsock, message=f'{rsock.getpeername()}: '.encode() + data)
            else:
                logout(rsock)

    for wsock in writable:
        try:
            msg = message_queues[wsock].get_nowait()
        except queue.Empty:
            outputs.discard(wsock)
        else:
            wsock.send(msg)

    for esock in exeptional:
        print('Exception on ' + esock.getpeername())
        logout(esock)
