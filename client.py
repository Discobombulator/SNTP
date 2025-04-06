import socket
import struct
import time

SERVER = 'localhost'
PORT = 123
NTP_EPOCH = 2208988800

def SNTP_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'  # Байтовый пакет, 48 байт ровно
    client.sendto(data, (SERVER, PORT))
    data, _ = client.recvfrom(1024)
    timestamp = struct.unpack('!12I', data)[10] - NTP_EPOCH
    print("Время: ", time.ctime(timestamp))

if __name__ == '__main__':
    SNTP_client()
