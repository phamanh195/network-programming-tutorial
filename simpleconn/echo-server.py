# echo-server.py

import socket

HOST = '127.0.0.1'
PORT = 65432

"""
socket.socket creates a socket object that support the context manager type,
so you can use it in a with statement. There is no need to call s.close()
"""

"""
socket.AF_INET: (IPv4), so it expects a two-tuple (host, port)
host: can be hostname, IP address or empty string

IP address '127.0.0.1' is the standard IPv4 for loopback interface,
so only the host will able to connect to server.
If you pass an empty string, the server will accept connections on all
available IPv4 interface.

port represents the TCP port number to accept connections from client
It should be an integer from 1 to 65535, as 0 is received.
Some system may required superuser privileges if the port number is less than 1024

"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()  # backlog the number of connections allow on incoming queue
    while True:
        conn, addr = s.accept()
        while conn:
            while True:
                """
                The bufsize argument used is the maximum amount of data to be received at once.
                It doesn't mean that .recv() will return 1024 bytes.
                The send() method also behave this way.
                Unlike send(), sendall() contines to send data from bytes until either all data has been sent
                or an error occurs. None is returned on success.
                """
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)
            conn.close()
            break
