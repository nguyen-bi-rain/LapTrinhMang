import socket

if __name__ == '__main__':
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sk.bind(('127.0.0.1',9050))
    data,addr = sk.recvfrom(1024)
    print("client gui {}".format(data))
    data = 'hello client'
    sk.sendto(data.encode('utf-8'),addr)
    sk.close()
