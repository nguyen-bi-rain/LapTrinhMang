import socket
import requests
import json

def handle_client_request(client_socket):
    try:
        # Receive client request
        request_data = client_socket.recv(1024).decode('utf-8')
        print(f"Received request: {request_data}")

        # Parse the request data (assuming it's a simple API endpoint in JSON format)
        request_json = json.loads(request_data)
        api_url = request_json.get("url")
        params = request_json.get("params", {})

        if not api_url:
            response = {"error": "Missing API URL."}
        else:
            # Call the external API
            try:
                api_response = requests.get(api_url, params=params)
                response = {
                    "status_code": api_response.status_code,
                    "data": api_response.json() if api_response.status_code == 200 else api_response.text
                }
            except Exception as e:
                response = {"error": f"Failed to call API: {str(e)}"}

        # Send response back to client
        client_socket.sendall(json.dumps(response).encode('utf-8'))

    except Exception as e:
        error_response = {"error": f"Internal server error: {str(e)}"}
        client_socket.sendall(json.dumps(error_response).encode('utf-8'))
    finally:
        client_socket.close()


def start_server(host='127.0.0.1', port=5000):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            # Accept a new client connection
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Handle the client request
            handle_client_request(client_socket)

    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
