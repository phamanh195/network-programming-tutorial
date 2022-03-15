"""
The echo client example processes all of the I/O events
in the main loop, instead of using callbacks
"""
import selectors
import socket

my_selector = selectors.DefaultSelector()
keep_running = True

outgoing = [
    b'It will be repeated.',
    b'This is the message. ',
]
bytes_sent = 0
bytes_received = 0

server_address = ('localhost', 10000)
print(f'Connecting to {server_address}')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)
sock.setblocking(False)

my_selector.register(
    sock,
    selectors.EVENT_READ | selectors.EVENT_WRITE,
)

while keep_running:
    print('waiting for I/O')
    for key, mask in my_selector.select(timeout=1):
        connection = key.fileobj
        client_address = connection.getpeername()
        print(f'Client {client_address}')

        if mask & selectors.EVENT_READ:
            print('Ready to read')
            data = connection.recv(1024)
            if data:
                print(f'Received {data!r}')
                bytes_received += len(data)

            keep_running = not (
                data or
                (bytes_received and bytes_received == bytes_sent)
            )

        if mask & selectors.EVENT_WRITE:
            print('Ready for write')
            if not outgoing:
                my_selector.modify(sock, selectors.EVENT_READ)
            else:
                next_msg = outgoing.pop()
                print(f'Sending {next_msg!r}')
                sock.sendall(next_msg)
                bytes_sent += len(next_msg)

print('shutting down')
my_selector.unregister(connection)
connection.close()
my_selector.close()
