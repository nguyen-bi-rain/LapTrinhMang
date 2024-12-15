import socket

# viet chuong trinh gui server yeu cau kiem tra lenh va gui ve


if __name__ == '__main__':
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    data = 'hello server'
    sk.sendto(data.encode('utf-8'),('127.0.0.1',9050))
    data = sk.recvfrom(1024)
    print("server gui: {}".format(data))
    sk.close()