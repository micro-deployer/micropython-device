import socket
import struct
import time


def run(ip, port, interval, unique_id, deployer_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.getaddrinfo(ip, port)[0][-1]
    message = struct.pack(">BH", interval, deployer_port) + unique_id
    while True:
        sock.sendto(message, addr)
        time.sleep(interval)
