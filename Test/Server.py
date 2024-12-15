import socket
import os


def handle_client_connection(client_socket):
    while True:
        request = client_socket.recv(4096).decode()  # Receive the request from the client
        if not request:
            break

        if os.path.isdir(request):
            # If the request is a directory, list the contents
            try:
                files_and_dirs = os.listdir(request)
                response = "\n".join(files_and_dirs)
            except Exception as e:
                response = str(e)
        elif os.path.isfile(request):
            # If the request is a file, send the file contents
            try:
                with open(request, 'r') as file:
                    response = file.read()
            except Exception as e:
                response = str(e)
        else:
            # If the path is invalid
            response = "Invalid directory or file."

        client_socket.send(response.encode())  # Send the response back to the client


# Set up the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12345))  # Bind to localhost and port 12345
server_socket.listen(5)  # Allow up to 5 connections

print("Server listening on port 12345...")

while True:
    client_socket, addr = server_socket.accept()  # Accept a client connection
    print(f"Connected to {addr}")
    handle_client_connection(client_socket)  # Handle the client connection
    client_socket.close()
