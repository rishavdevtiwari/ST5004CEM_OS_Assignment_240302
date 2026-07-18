import json
import socket
import threading

HOST = "127.0.0.1"
PORT = 8080
AUTH_TOKEN = "super_secret_ipc_token"  # basic authentication passkey

def handle_client_connection(client_socket, client_address):
    print("client connected from: " + str(client_address))
    try:
        while True:
            raw_data = client_socket.recv(1024).decode("utf-8")
            if not raw_data: break
            print("received raw payload: " + raw_data)
            
            # ipc protovol envelope validation and command execution logic
            try:
                payload = json.loads(raw_data)
                # check structural presence and token authenticity parameters
                if "token" not in payload or payload["token"] != AUTH_TOKEN:
                    response = {"status": "error", "message": "unauthorized token execution verification check failed"}
                else:
                    cmd = payload.get("command", "")
                    user_data = payload.get("data", "")
                    
                    if cmd == "PING":
                        response = {"status": "success", "message": "PONG"}
                    elif cmd == "UPPERCASE":
                        response = {"status": "success", "message": str(user_data).upper()}
                    else:
                        response = {"status": "success", "message": "acknowledged"}
            except json.JSONDecodeError:
                response = {"status": "error", "message": "malformed data stream"}
                
            client_socket.send(json.dumps(response).encode("utf-8"))
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
            t = threading.Thread(target=handle_client_connection, args=(client_sock, client_addr))
            t.start()
    finally:
        server_sock.close()

if __name__ == "__main__":
    run_ipc_server()