import socket


HOST = '127.0.0.1'
PORT = 65430

buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
    udp_sock.bind((HOST, PORT))
    while True:
        message, address = udp_sock.recvfrom(buffer_size)
        udp_sock.sendto(message, address)
