import socket
import struct

try:
    from machine import idle
except ImportError:
    from time import sleep_us


    def idle():
        sleep_us(1)

import os


def _recv_exactly(sock, num_bytes):
    received_bytes = bytearray()
    len_received_bytes = 0
    while len_received_bytes != num_bytes:
        received_bytes += sock.recv(num_bytes - len_received_bytes)
        len_received_bytes = len(received_bytes)
        idle()
    return received_bytes


def run(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = socket.getaddrinfo('0.0.0.0', port)[0][-1]
    sock.bind(server_addr)
    sock.listen(5)

    conn, addr = sock.accept()
    # ip = socket.inet_ntop(socket.AF_INET, addr)  # FIX on ESP32
    print('Client connected')

    files_count_bytes = _recv_exactly(conn, 1)
    files_count = struct.unpack('>B', files_count_bytes)[0]
    for file_counter in range(files_count):
        filepath_length_bytes = _recv_exactly(conn, 1)
        filepath_length = struct.unpack('>B', filepath_length_bytes)[0]
        filepath_bytes = _recv_exactly(conn, filepath_length)
        filepath = filepath_bytes.decode('ascii')
        print('File to receive:', filepath)
        *dirs, _ = filepath.split('/')

        for i in range(len(dirs)):
            try:
                os.mkdir('/'.join(dirs[:i + 1]))
            except OSError:
                pass

        file_length_bytes = _recv_exactly(conn, 2)
        file_length = struct.unpack('>H', file_length_bytes)[0]

        with open(filepath, 'wb+') as f:
            received_len = 0
            while received_len != file_length:
                file_bytes = conn.recv(file_length - received_len)
                received_len += f.write(file_bytes)
        file_counter_bytes = struct.pack('>B', file_counter)
        conn.send(file_counter_bytes)
        print('Deployer: Received', filepath)
    conn.close()

    return True
