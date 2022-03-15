import socket
import time

server_address = ('localhost', 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f'Connecting to {server_address}')
sock.connect(server_address)

time.sleep(1)

messages = [
    'Part one of the message.',
    'Part two of the message.',
]
amount_expected = len(''.join(messages))

try:
    for message in messages:
        data = message.encode()
        print(f'Sending {data!r}')
        sock.sendall(data)
        time.sleep(1.5)

    amount_received = 0

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print(f'Received {data!r}')

finally:
    print('Closing socket')
    sock.close()
