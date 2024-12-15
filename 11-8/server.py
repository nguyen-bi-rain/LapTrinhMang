import socket
import os

# Hardcoded credentials for simplicity
USERNAME = 'user01'
PASSWORD = '123'

def handle_client(client_socket):
    # Authentication
    credentials = client_socket.recv(1024).decode()
    username, password = credentials.split()
    if username != USERNAME or password != PASSWORD:
        client_socket.send(b'Authentication failed')
        client_socket.close()
        return
    client_socket.send(b'Authentication successful')

    # Handle commands
    request = client_socket.recv(1024).decode()
    command, file_path = request.split()

    if command == 'upload':
        with open(file_path, 'wb') as f:
            while True:
                bytes_read = client_socket.recv(1024)
                if not bytes_read:
                    break
                f.write(bytes_read)
        client_socket.send(b'Upload complete')
    elif command == 'download':
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    client_socket.send(bytes_read)
            client_socket.send(b'Download complete')
        else:
            client_socket.send(b'File not found')
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))
    server.listen(5)
    print('Server listening on port 12345')

    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr}')
        handle_client(client_socket)

if __name__ == '__main__':
    main()