import socket
import threading
import datetime

def handle_client(socket):
    command = socket.recv(1024).decode('utf-8')
    if command == "Max":
        a, b = socket.recv(1024).decode('utf-8').split("-")
        socket.sendall(str(max(int(a), int(b))).encode('utf-8'))
    elif command == "Min":
        a, b = socket.recv(1024).decode('utf-8').split("-")
        socket.sendall(str(min(int(a), int(b))).encode('utf-8'))
    elif command == "GET TIME":
        time = datetime.datetime.now().strftime("%H:%M:%S")
        socket.sendall(time.encode('utf-8'))
    else:
        count = 0
        for char in command:
            if char.isupper():
                count += 1
        socket.sendall(str(count).encode('utf-8'))

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('127.0.0.1',5050))
    while True:
        server.listen(5)
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_socket.recv(1024).decode('utf-8')}")
        threading.Thread(target=handle_client,args=(client_socket,)).start()
    server.close()