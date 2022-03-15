# multiconn-server.py

import sys
import socket
import selectors
import types

sel = selectors.DefaultSelector()

hort, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((hort, port))
lsock.listen()
print(f'Listening on {(hort, port)}')
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)


def accept_wrapper(sock: socket.socket):
    conn, addr = sock.accept()
    print(f'Accepted connection from {addr}')
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mark):
    sock = key.fileobj
    data = key.data
    if mark & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f'Closing connection to {data.addr}')
            sel.unregister(sock)
            sock.close()
    if mark & selectors.EVENT_WRITE:
        if data.outb:
            print(f'Echoing {data.outb!r} to {data.addr}')
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <host> <port>")
    sys.exit(1)

try:
    while True:
        events = sel.select(timeout=None)
        for key, marks in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, marks)
except KeyboardInterrupt:
    print('Caught keyboard interrupt, exiting.')
finally:
    sel.close()
