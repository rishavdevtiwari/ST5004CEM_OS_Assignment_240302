import socket

#  basic single connection server that listens on port 8080 and accepts a single connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 8080))
s.listen(1)
print("[SERVER] basic single connection server listening on port 8080...")
# blocks here until something rings our socket pipeline
conn, addr = s.accept()
print("secured connection from: " + str(addr))
conn.close()
s.close()