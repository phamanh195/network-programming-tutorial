import socket
import sys

messages = [
    'This is the message',
    'It will be sent',
    'in parts.',
]
server_address = ('localhost', 10000)

socks = [
    socket.socket(socket.AF_INET, socket.SOCK_STREAM),
    socket.socket(socket.AF_INET, socket.SOCK_STREAM),
]

print(f'Connecting to {server_address}')
for s in socks:
    s.connect(server_address)

for message in messages:
    outgoing_data = message.encode()

    for s in socks:
        print('{}: sending {!r}'.format(s.getsockname(), outgoing_data))
        s.send(outgoing_data)

    for s in socks:
        data = s.recv(1024)
        print('{}: received {!r}'.format(s.getsockname(), data))

        if not data:
            print('Closing socket', s.getsockname())
            s.close()
