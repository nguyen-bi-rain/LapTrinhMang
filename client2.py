
import socket
import cv2
import base64
import threading
import numpy as np

# Client configuration
SERVER_IP = "192.168.2.16"  # Replace with your server's IP address
SERVER_PORT = 6000          # Server's forwarding port

# Socket for sending and receiving data
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Notify server of readiness (sends an initial "registration" message)
client_socket.sendto(b"REGISTER", (SERVER_IP, SERVER_PORT))

# Video capture and sending function
def send_video():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Encode the frame to send over UDP
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
        encoded_frame = base64.b64encode(buffer)
        client_socket.sendto(encoded_frame, (SERVER_IP, SERVER_PORT))

# Video receiving and display function
def receive_video():
    while True:
        data, _ = client_socket.recvfrom(65536)
        frame = base64.b64decode(data)
        np_frame = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow("Receiving Video", np_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Start both send and receive threads
threading.Thread(target=send_video).start()
threading.Thread(target=receive_video).start()