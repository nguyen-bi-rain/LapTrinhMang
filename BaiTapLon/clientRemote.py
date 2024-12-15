import socket
import pickle
import struct
import cv2
import numpy as np

def send_command(client, action, position=None):
    command = {'action': action}
    if position:
        command['position'] = position
    client.sendall(pickle.dumps(command))

def mouse_event(event, x, y, flags, param):
    client = param['client']
    original_width, original_height = param['original_size']
    display_width, display_height = param['display_size']

    # Tính toán vị trí chuột trên ảnh gốc
    if event == cv2.EVENT_LBUTTONDOWN:  # Nhấp chuột trái
        send_command(client, 'click')
    elif event == cv2.EVENT_MOUSEMOVE:  # Di chuyển chuột
        # Chuyển đổi vị trí chuột theo tỷ lệ
        x_original = int(x * (original_width / display_width))
        y_original = int(y * (original_height / display_height))
        send_command(client, 'move', position=(x_original, y_original))

def receive_screen(ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    print(f"Đã kết nối tới {ip}:{port}")

    data = b""
    payload_size = struct.calcsize("Q")  # Kích thước 64-bit

    # Kích thước cửa sổ hiển thị
    display_width, display_height = 800, 600  # Điều chỉnh kích thước theo mong muốn

    try:
        # Tạo cửa sổ và gán hàm sự kiện chuột
        cv2.namedWindow("Màn hình từ xa", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Màn hình từ xa", display_width, display_height)  # Đặt kích thước cửa sổ

        # Thông tin kích thước gốc
        original_size = None

        cv2.setMouseCallback("Màn hình từ xa", mouse_event, param={'client': client, 'display_size': (display_width, display_height)})

        while True:
            # Nhận kích thước của dữ liệu
            while len(data) < payload_size:
                data += client.recv(4096)

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]  # Kích thước dữ liệu ảnh

            # Nhận dữ liệu ảnh
            while len(data) < msg_size:
                data += client.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Giải nén và hiển thị ảnh
            try:
                screenshot = np.array(pickle.loads(frame_data))
                frame = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

                # Lưu kích thước gốc
                if original_size is None:
                    original_height, original_width = screenshot.shape[:2]
                    original_size = (original_width, original_height)
                    # Cập nhật thông tin kích thước gốc cho sự kiện chuột
                    cv2.setMouseCallback("Màn hình từ xa", mouse_event, param={'client': client, 'original_size': original_size, 'display_size': (display_width, display_height)})

                # Điều chỉnh kích thước của ảnh
                frame_resized = cv2.resize(frame, (display_width, display_height))  # Điều chỉnh kích thước
                cv2.imshow("Màn hình từ xa", frame_resized)  # Hiển thị ảnh đã điều chỉnh

            except pickle.UnpicklingError:
                print("Lỗi giải mã dữ liệu nhận được từ server.")

            # Thoát khi nhấn phím 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        client.close()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    ip = input("Nhập IP của server: ")
    port = int(input("Nhập cổng server: "))
    receive_screen(ip, port)