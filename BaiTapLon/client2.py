import socket
import json
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io
import cv2

# Function to send video to the server
def send_video_to_server(username, password, action, host='192.168.2.39', port=12345):
    global conn, video_streaming
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))

        # Send credentials and action (login/register)
        credentials = json.dumps({"username": username, "password": password, "action": action})
        conn.send(credentials.encode())

        # Receive server response
        response = conn.recv(1024).decode()
        if response == "Authentication Failed" or response == "Username already exists":
            messagebox.showerror("Error", response)
            conn.close()
            return
        if action == "register":
            messagebox.showinfo("Success", "Registration Successful. Please log in.")
            conn.close()
            return

        # If authenticated, set up video stream
        show_video_stream()

    except Exception as e:
        messagebox.showerror("Error", f"Connection error: {e}")

def show_video_stream():
    global video_streaming, cap
    video_streaming = True

    # Clear the login frame and set up video frame
    for widget in root.winfo_children():
        widget.destroy()

    # Disconnect button
    disconnect_button = tk.Button(root, text="Disconnect", command=disconnect)
    disconnect_button.pack()

    # Label to display video feed
    global video_label
    video_label = tk.Label(root)
    video_label.pack()

    # Start capturing and sending video
    cap = cv2.VideoCapture(1)
    threading.Thread(target=stream_video).start()

def stream_video():
    global video_streaming, conn
    while video_streaming:
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        img_data = buffer.tobytes()
        img_size = f"{len(img_data):08d}".encode()
        conn.sendall(img_size + img_data)

        # Receive image back from server
        img_size_back = int(conn.recv(8).decode())
        img_data_back = b""
        while len(img_data_back) < img_size_back:
            packet = conn.recv(img_size_back - len(img_data_back))
            if not packet:
                break
            img_data_back += packet

        # Show received image
        img = Image.open(io.BytesIO(img_data_back))
        img = img.resize((300, 250))
        tk_img = ImageTk.PhotoImage(img)
        video_label.config(image=tk_img)
        video_label.image = tk_img

    cap.release()

def disconnect():
    global video_streaming
    video_streaming = False
    conn.close()
    root.quit()

# Tkinter GUI setup for login and registration
def start_login():
    def connect(action):
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password")
            return

        # Start video stream or register
        threading.Thread(target=send_video_to_server, args=(username, password, action)).start()

    # Create main Tkinter window
    global root
    root = tk.Tk()
    root.title("Client Login")

    # Username label and entry
    tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
    entry_username = tk.Entry(root)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    # Password label and entry
    tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
    entry_password = tk.Entry(root, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    # Login and Register buttons
    login_button = tk.Button(root, text="Login", command=lambda: connect("login"))
    login_button.grid(row=2, column=0, pady=10)

    register_button = tk.Button(root, text="Register", command=lambda: connect("register"))
    register_button.grid(row=2, column=1, pady=10)

    # Label for video display after login
    global video_label
    video_label = tk.Label(root)
    video_label.grid(row=3, column=0, columnspan=2)

    root.mainloop()

# Start the GUI login window
start_login()
