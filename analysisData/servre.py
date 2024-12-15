import socket
from time import ctime

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    s.bind(('127.0.0.1', 9050))
    while True:
        s.listen(2)

        client_sk, client_addr = s.accept()
        print(f"client address : {client_addr}")
        while True:
            data = input("enter message : ")
            client_sk.send(data.encode('utf-8'))
            data = client_sk.recv(4096)
            print(f"receive from client {data.decode('utf-8')}")
            if data.decode('utf-8') == 'bye':
                client_sk.send("bye".encode('utf-8'))
                break
            if data.decode('utf-8') == "GET_TIME":
                client_sk.send(ctime().encode('utf-8'))
            else:
                client_sk.send(data)
            client_sk.close()
    s.close()

