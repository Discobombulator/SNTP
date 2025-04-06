import socket
import struct
import select
from threading import Thread
from time import time


BUFFER_SIZE = 4096
NTP_EPOCH = 2208988800
HEAD_FORMAT = ">BBBBII4sQQQQ"

class SNTPServer:
    def __init__(self, request_data, offset):
        self.offset = offset
        self.request_time = self.get_current_time()
        self.dispatch_time = self.extract_client_time(request_data)

    def extract_client_time(self, data):
        return struct.unpack(HEAD_FORMAT, data)[10]

    def get_current_time(self):
        return int((time() + NTP_EPOCH + self.offset) * (2 ** 32))

    def build_response(self):
        return struct.pack(
            HEAD_FORMAT,
            (0 << 6 | 4 << 3 | 4),  # leap, version, mode
            1, 0, 0, 0, 0, b'', 0,
            self.dispatch_time, self.request_time, self.get_current_time()
        )


class RequestHandler(Thread):
    def __init__(self, sock, offset):
        super().__init__()
        self.sock = sock
        self.offset = offset

    def run(self):
        data, addr = self.sock.recvfrom(BUFFER_SIZE)
        response = SNTPServer(data, self.offset).build_response()
        self.sock.sendto(response, addr)


def read_config():
    with open('config.txt') as f:
        return {k: int(v) for k, v in (line.strip().split(':') for line in f if ':' in line)}


def run_server():
    config = read_config()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('localhost', config['port']))
        print("Сервер запущен")
        while True:
            r, _, _ = select.select([sock], [], [], 1)
            if r:
                RequestHandler(sock, config['offset']).start()
