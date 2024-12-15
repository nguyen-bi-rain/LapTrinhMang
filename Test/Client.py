import tkinter as tk
import socket


def send_request():
    request = input_text.get()  # Get the input from the entry widget (either directory or file)
    client_socket.send(request.encode())  # Send the request to the server

    response = client_socket.recv(4096).decode()  # Receive the response from the server
    text_box.delete(1.0, tk.END)  # Clear the text box
    text_box.insert(tk.END, response)  # Display the server's response in the text box


# Set up the socket connection to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))  # Connect to the server

# Create the Tkinter GUI
root = tk.Tk()
root.title("File & Directory Viewer")

# Create an input text field
input_label = tk.Label(root, text="Enter Directory or File:")
input_label.pack()
input_text = tk.Entry(root)
input_text.pack()

# Create a button to send the request
send_button = tk.Button(root, text="Send", command=send_request)
send_button.pack()

# Create a text box to display the response
text_box = tk.Text(root, height=20, width=50)
text_box.pack()

# Run the tkinter main loop
root.mainloop()

# Close the socket when done
client_socket.close()
