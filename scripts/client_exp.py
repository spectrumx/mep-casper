import socket

def start_client():
    ## Server information to connect to
    host = '127.0.0.1'  ## localhost - same as server
    port = 12345        ## same port as server

    try:
        ## Create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ## Connect to server
        print(f"Connecting to server at {host}:{port}...")
        client_socket.connect((host, port))
        print("Connected to server")

        ## Send a message
        message = "Hello from the client!"
        print(f"Sending message: {message}")
        client_socket.send(message.encode())

        ## Receive response
        response = client_socket.recv(1024)
        print(f"Response from server: {response.decode()}")

    except ConnectionRefusedError:
        print("Connection failed. Make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        ## Close socket
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    start_client()