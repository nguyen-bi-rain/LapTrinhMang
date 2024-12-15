import socket
import json

def send_request_to_server(server_host, server_port, request_data):
    try:
        # Create a socket to connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))

        # Send the request to the server
        client_socket.sendall(json.dumps(request_data).encode('utf-8'))

        # Receive the response from the server
        response_data = client_socket.recv(4096).decode('utf-8')
        response = json.loads(response_data)

        print("Response from server:")
        print(json.dumps(response, indent=4))

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    # Example request data
    request_data = {
        "url": "https://jsonplaceholder.typicode.com/posts/1",
        "params": {}
    }

    # Server connection details
    server_host = '127.0.0.1'
    server_port = 5000

    # Send the request to the server
    send_request_to_server(server_host, server_port, request_data)
