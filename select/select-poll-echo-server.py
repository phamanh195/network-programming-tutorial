import select
import socket
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)

server_address = ('localhost', 10000)
print(f'Starting up on {server_address}')
server.bind(server_address)

server.listen(5)

message_queues = {}

TIMEOUT = 1000  # timeout pass to pill is represented in milliseconds, instead of seconds

READ_ONLY = (
    select.POLLIN |
    select.POLLPRI |
    select.POLLHUP |
    select.POLLERR
)
READ_WRITE = READ_ONLY | select.POLLOUT

poller = select.poll()
poller.register(server, READ_ONLY)

# file descriptors to socket objects
fd_to_socket = {
    server.fileno(): server,  # return the integer file descriptor of socket
}

while True:
    print('Waiting for the next event')
    events = poller.poll(TIMEOUT)

    for fd, flag in events:
        s = fd_to_socket[fd]

        if flag & (select.POLLIN | select.POLLPRI):
            if s is server:
                connection, client_address = s.accept()
                print('Connection', client_address)
                connection.setblocking(0)
                fd_to_socket[connection.fileno()] = connection
                poller.register(connection, READ_ONLY)

                # give the connection a queue for data to send
                message_queues[connection] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    print(f'Received {data!r} from {s.getpeername()}')
                    message_queues[s].put(data)
                    poller.modify(s, READ_WRITE)
                else:
                    print('Closing', s.getpeername())
                    # stop listening for input on the connection
                    poller.unregister(s)
                    s.close()

                    del message_queues[s]
        elif flag & select.POLLHUP:
            # client hung up
            print('Closing', s.getpeername())
            poller.unregister(s)
            s.close()
        elif flag & select.POLLOUT:
            # socket is ready to send data if there is any to send
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                # No messages waiting so stop checking
                print(s.getpeername(), 'queue empty')
                poller.modify(s, READ_ONLY)
            else:
                print(f'Sending {next_msg!r} to {s.getpeername()}')
                s.send(next_msg)
        elif flag & select.POLLERR:
            print('Exception on', s.getpeername())
            poller.unregister(s)
            s.close()

            del message_queues[s]
