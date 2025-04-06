import socket
import struct
import time

SERVER = 'localhost'
PORT = 12345  # тот же, что в config.txt
NTP_EPOCH = 2208988800

def SNTP_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    request = b'\x1b' + 47 * b'\0'
    client.sendto(request, (SERVER, PORT))
    data, _ = client.recvfrom(1024)
    timestamp = struct.unpack('!12I', data)[10] - NTP_EPOCH
    print("Время: ", time.ctime(timestamp))

if __name__ == '__main__':
    SNTP_client()
