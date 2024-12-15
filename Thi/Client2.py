import socket

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 5050))
    client_socket.send("test1".encode('utf-8'))
    data = input("what you want to calculate: ")
    client_socket.sendall(data.encode('utf-8'))
    number = input("Enter two numbers: ")
    client_socket.sendall(number.encode('utf-8'))
    res = client_socket.recv(1024).decode('utf-8')
    print(res)
