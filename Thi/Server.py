import socket
import requests
import ftplib
import threading
def send_page_content(client_socket, url):
    try:
        # Fetch the page content
        response = requests.get(url)
        data = response.text

        # Send the length of the data first
        data_length = len(data)
        client_socket.sendall(str(data_length).encode('utf-8'))

        # Wait for the client to acknowledge
        client_socket.recv(1024)

        # Send the data in chunks
        chunk_size = 1024
        for i in range(0, data_length, chunk_size):
            client_socket.sendall(data[i:i+chunk_size].encode('utf-8'))

    except Exception as e:
        print(f"Error: {str(e)}")

def upload_file_in_ftp(ftp ,filename):
    try:
        with open(filename) as file:
            ftp.storbinary(f"STOR {filename}", file)
        ftp.quit()
    except Exception as e:
        print(f"Error uploading file: {e} ")


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 5050))
    server.listen(5)
    ftp = ftplib.FTP(host='127.0.0.1')
    ftp.login("user01","123")
    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        # threading.Thread(target=send_page_content, args=(client_socket, "https://vi.wikipedia.org/wiki/Trang_Chính")).start()
        send_page_content(client_socket, "https://vi.wikipedia.org/wiki/Trang_Chính")
        # request = client_socket.recv(1024).decode('utf-8')
        # if request.startswith('upload'):
        #     filename = request.split(' ')[1]
        #     upload_file_in_ftp(ftp, filename)
        #     client_socket.send("Upload file completed successfully".encode('utf-8'))
        # response = client_socket.recv(1024)
        # print(f"Received: {response.decode('utf-8')}")
        client_socket.close()

    server.close()