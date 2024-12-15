import socket
import json
import threading
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import io
import os

# Load user credentials from JSON file
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users():
    with open(USER_FILE, "w") as file:
        json.dump(users, file)

# Initialize user credentials
users = load_users()

# Create a new user
def create_user(username, password):
    if username in users:
        return False  # Username already exists
    users[username] = password
    save_users()
    return True

# Authenticate user credentials
def authenticate(username, password):
    return users.get(username) == password

# Start server to handle client connections
def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

# Handle each client connection
def handle_client(conn, addr):
    try:
        data = conn.recv(1024).decode()
        credentials = json.loads(data)
        action = credentials.get("action")

        username = credentials['username']
        password = credentials['password']

        if action == "register":
            if create_user(username, password):
                conn.send("Registration Successful".encode())
            else:
                conn.send("Username already exists".encode())
            conn.close()
            return

        elif action == "login":
            if not authenticate(username, password):
                conn.send("Authentication Failed".encode())
                conn.close()
                return
            conn.send("Authenticated".encode())

            # Start receiving and displaying video frames
            while True:
                img_size = conn.recv(8).decode()  # Get image size header
                if not img_size:
                    break  # Stop if client disconnects

                img_data = b""
                img_size = int(img_size)
                while len(img_data) < img_size:
                    packet = conn.recv(img_size - len(img_data))
                    if not packet:
                        return  # Exit on disconnection
                    img_data += packet

                # Display image in the GUI
                show_image(img_data, username)

                # Echo the image back to the client
                conn.sendall(f"{len(img_data):08d}".encode() + img_data)

    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()
        reset_gui()  # Reset GUI on client disconnect

# Display image in server's Tkinter GUI
def show_image(img_data, username):
    img = Image.open(io.BytesIO(img_data))
    img = img.resize((300, 250))
    tk_img = ImageTk.PhotoImage(img)

    # Determine grid position for the new client
    client_count = len(label_dict)
    row, col = divmod(client_count, 3)  # Arrange 3 clients per row

    if username in label_dict:
        label_dict[username].config(image=tk_img)
        label_dict[username].image = tk_img
    else:
        # Add username label and image in the grid layout
        lbl = Label(root, text=username)
        lbl.grid(row=row * 2, column=col, padx=10, pady=10)
        img_label = Label(root, image=tk_img)
        img_label.image = tk_img
        img_label.grid(row=row * 2 + 1, column=col, padx=10, pady=10)
        label_dict[username] = img_label

    # Resize the window based on the number of clients
    root.update_idletasks()
    width = 300 * min(3, client_count + 1)  # 3 clients per row
    height = (row + 1) * 300
    root.geometry(f"{width}x{height}")

# Reset the GUI when a client disconnects
def reset_gui():
    for widget in root.winfo_children():
        widget.destroy()
    label_dict.clear()
    tk.Label(root, text="Waiting for client connections...").grid(row=0, column=0, columnspan=3)

# Set up Tkinter GUI
root = tk.Tk()
root.geometry("500x500")
root.title("Server - Video Monitoring")
label_dict = {}

reset_gui()  # Show initial "waiting" message
threading.Thread(target=start_server).start()
root.mainloop()
