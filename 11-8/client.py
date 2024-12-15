import socket
from ftplib import FTP

def upload_file_socket(server_ip, file_path, username, password):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 12345))
    client.send(f'{username} {password}'.encode())
    response = client.recv(1024).decode()
    if response == 'Authentication failed':
        print('Authentication failed')
        client.close()
        return
    client.send(f'upload {file_path}'.encode())

    with open(file_path, 'rb') as f:
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break
            client.send(bytes_read)
    response = client.recv(1024)
    print(response.decode())
    client.close()

def download_file_socket(server_ip, file_name, username, password):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 12345))
    client.send(f'{username} {password}'.encode())
    response = client.recv(1024).decode()
    if response == 'Authentication failed':
        print('Authentication failed')
        client.close()
        return
    client.send(f'download {file_name}'.encode())

    with open(file_name, 'wb') as f:
        while True:
            bytes_read = client.recv(1024)
            if bytes_read == b'Download complete':
                break
            if bytes_read == b'File not found':
                print('File not found on server')
                break
            f.write(bytes_read)
    client.close()

def upload_file_ftp(ftp_server, ftp_user, ftp_password, file_path):
    ftp = FTP(ftp_server)
    ftp.login(user=ftp_user, passwd=ftp_password)

    with open(file_path, 'rb') as file:
        ftp.storbinary(f'STOR {file_path}', file)

    ftp.quit()
    print(f'Uploaded {file_path} to {ftp_server}')

def download_file_ftp(ftp_server, ftp_user, ftp_password, file_name):
    ftp = FTP(ftp_server)
    ftp.login(user=ftp_user, passwd=ftp_password)

    with open(file_name, 'wb') as file:
        ftp.retrbinary(f'RETR {file_name}', file.write)

    ftp.quit()
    print(f'Downloaded {file_name} from {ftp_server}')

if __name__ == '__main__':
    method = input('Enter method (socket/ftp): ')
    if method == 'socket':
        server_ip = input('Enter server IP: ')
        username = input('Enter username: ')
        password = input('Enter password: ')
        command = input('Enter command (upload/download): ')
        file_path = input('Enter file path or name: ')

        if command == 'upload':
            upload_file_socket(server_ip, file_path, username, password)
        elif command == 'download':
            download_file_socket(server_ip, file_path, username, password)
        else:
            print('Invalid command')
    elif method == 'ftp':
        ftp_server = input('Enter FTP server: ')
        ftp_user = input('Enter FTP username: ')
        ftp_password = input('Enter FTP password: ')
        command = input('Enter command (upload/download): ')
        file_path = input('Enter file path or name: ')

        if command == 'upload':
            upload_file_ftp(ftp_server, ftp_user, ftp_password, file_path)
        elif command == 'download':
            download_file_ftp(ftp_server, ftp_user, ftp_password, file_path)
        else:
            print('Invalid command')
    else:
        print('Invalid method')