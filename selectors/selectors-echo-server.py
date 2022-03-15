import selectors
import socket

my_selector = selectors.DefaultSelector()
keep_running = True


def read(connection: socket.socket, mask: int):
    """
    Callback for read events

    Args:
        connection:
        mask:

    Returns:

    """
    global keep_running
    client_address = connection.getpeername()
    print('Read', client_address)
    data = connection.recv(1024)
    if data:
        # A readable client socket has data
        print(f'Received {data!r}')
        connection.sendall(data)
    else:
        print('Closing')
        my_selector.unregister(connection)
        connection.close()
        keep_running = False


def accept(sock: socket.socket, mask: int):
    """
    Callback for new connections
    Args:
        sock:
        mask:

    Returns:

    """
    new_connection, address = sock.accept()
    print(f'Accept {address}')
    new_connection.setblocking(False)
    my_selector.register(new_connection, selectors.EVENT_READ, read)


server_address = ('localhost', 10000)
print(f'Starting up on {server_address}')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(server_address)
server.listen(5)

my_selector.register(server, selectors.EVENT_READ, accept)

while keep_running:
    print('Waiting for I/O')
    for key, mask in my_selector.select(timeout=1):
        callback = key.data
        callback(key.fileobj, mask)

print('Shutting down')
my_selector.close()
