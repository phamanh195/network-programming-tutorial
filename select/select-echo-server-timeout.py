import select
import socket
import sys
import queue


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)

# Bind the socket to the port
server_address = ('localhost', 10000)
print(f'Starting up on {server_address}')
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(server_address)
server.listen(5)

inputs = [server]
outputs = []
timeout = 1
message_queues = {}

while inputs:
    print('Waiting for the next event')
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs, timeout
    )

    if not (readable or writable or exceptional):
        print('Timed out, do some other work here')
        continue

    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            print(f'Connection from {client_address}')
            connection.setblocking(False)
            inputs.append(connection)

            message_queues[connection] = queue.Queue()

        else:
            data = s.recv(1024)
            if data:
                print(
                    'Received {!r} from {}'.format(
                        data, s.getpeername()
                    )
                )
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                print(f'Closing {s.getpeername()}')
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                del message_queues[s]

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            print(
                'No message waiting {}'.format(
                    s.getpeername()
                )
            )
            outputs.remove(s)
        else:
            print(
                'Sending {!r} to {}'.format(
                    next_msg, s.getpeername()
                )
            )
            s.send(next_msg)

    for s in exceptional:
        print('Exception condition on', s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
