import socket
import string



dict = [
    {'msv' : 1,'hoten' : "thai ha", "diem" : 'diem'},
    {'msv': 2, 'hoten': "thai ha", "diem": 'diem'},
    {'msv': 3, 'hoten': "thai ha", "diem": 'diem'},
    {'msv': 4, 'hoten': "thai ha", "diem": 'diem'},
    {'msv': 5, 'hoten': "thai ha", "diem": 'diem'}
]
def string_process(s: str):
    s = s.strip()

    s = " ".join(s.split())

    s = ", ".join([part.strip() for part in s.split(",")])
    s.capitalize()
    s = ". ".join([part.strip().capitalize() for part in s.split(".")])
    if s[-1] not in string.punctuation:
        s += '.'
    return s.strip()


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind(("127.0.0.1",9080))
    s.listen(10)
    client, addr = s.accept()
    data = client.recv(4960).decode('utf-8')