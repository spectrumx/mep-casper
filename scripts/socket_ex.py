import socket

def start_server():
    ## Server configuration
    host = '127.0.0.1'  ## localhost
    port = 12345        ## arbitrary non-privileged port

    ## Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ## Set socket option to reuse address (helps avoid "Address already in use" errors)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ## Bind socket to address and port
    server_socket.bind((host, port))

    ## Listen for connections (queue up to 5 connection requests)
    server_socket.listen(5)

    print(f"Server started on {host}:{port}")
    print("Waiting for client connection...")

    try:
        ## Accept connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        ## Receive data from client
        data = client_socket.recv(1024)  ## receive up to 1024 bytes
        print(f"Message received: {data.decode()}")

        ## Send response to client
        response = "Message received by server"
        client_socket.send(response.encode())

        ## Close client connection
        client_socket.close()

    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        ## Close server socket
        server_socket.close()
        print("Server socket closed")

if __name__ == "__main__":
    start_server()