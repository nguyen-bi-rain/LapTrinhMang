import socket
import threading

host = '127.0.0.1'
port = 9050


def create_socket(HOST, PORT):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sk.bind((HOST, PORT))
    sk.listen(10)
    return sk


def receive_msg(sk):
    data = bytearray()
    msg = ''
    while not msg:
        b = sk.recv(1020)
        if not b:
            raise ConnectionError()
        data = data + b
        if b'\0' in b:
            msg = data.rstrip(b'\0')
    msg = msg.decode('utf-8')
    return msg


def create_msg(msg):
    msg = msg + '\0'
    return msg.encode('utf-8')


def send_msg(sk, msg):
    data = create_msg(msg)
    sk.sendall(data)


def process_client(sk, addr):
    try:
        msg = receive_msg(sk)
        msg = f"{addr} : {msg}"
        print(msg)
        send_msg(sk, msg)
    except ConnectionError:
        print('error')
    finally:
        print("socket closed")
        sk.close()


if __name__ == '__main__':

    sk1 = create_socket(host, port)
    addr = sk1.getsockname()
    print(f"dia chi cuc bo {addr}")
    while True:
        client_socket, addrc = sk1.accept()
        print("dia chi client {}".format(addrc))
        thread = threading.Thread(target=process_client, args=[client_socket, addr], daemon=True)
        thread.start()
        print("connect from {}".format(addr))
