import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

def handle_client_connection(client_socket, client_address):
    print("client connected from: " + str(client_address))
    try:
        while True:
            raw_data = client_socket.recv(1024).decode("utf-8")
            if not raw_data: break
            print("received: " + raw_data)
            client_socket.send(("echo back: " + raw_data).encode("utf-8"))
    finally:
        client_socket.close()

def run_ipc_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print("multi-threaded server pipeline tracking loop running...")
    
    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            # multi-client concurrency handled by spinning off background worker threads[cite: 1]
            t = threading.Thread(target=handle_client_connection, args=(client_sock, client_addr))
            t.start()
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_ipc_server()