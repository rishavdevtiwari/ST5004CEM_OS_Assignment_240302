import socket

# client that connects to the server on port 8080
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(("127.0.0.1", 8080))
print("[CLIENT] successfully connected to server loop.")
c.close()