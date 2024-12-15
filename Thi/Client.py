import socket

def receive_page_content(client_socket):
    try:
        # Receive the length of the data first
        data_length = int(client_socket.recv(1024).decode('utf-8'))

        # Acknowledge the length receipt
        client_socket.sendall(b'ACK')

        # Receive the data in chunks
        data = b''
        while len(data) < data_length:
            chunk = client_socket.recv(1024)
            data += chunk

        # Decode the complete data
        return data.decode('utf-8')

    except Exception as e:
        print(f"Error: {str(e)}")
        return ''


if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5050))
    # data = input("Enter your data: ")
    # client_socket.sendall(data.encode('utf-8'))
    # res = client_socket.recv(1024).decode('utf-8')
    # print(res)
    page_content = receive_page_content(client_socket)
    print(f"Received page content: {page_content}...")  # Print the first 500 characters for brevity

    client_socket.send("Hello, server!".encode('utf-8'))
    client_socket.close()