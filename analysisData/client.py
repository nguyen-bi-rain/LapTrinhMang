import socket


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
    s.connect(('127.0.0.1', 9050))
    while True:
        data = s.recv(4096)
        print("receive from server {}".format(data.decode('utf-8')))
        if data.decode('utf-8') == "bye":
            break
        data = input("enter text to server : ")
        s.send(data.encode('utf-8'))
    s.close()