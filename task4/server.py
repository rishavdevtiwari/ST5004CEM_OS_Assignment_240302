import json
import socket
import threading

HOST = "127.0.0.1"
PORT = 8080
AUTH_TOKEN = "super_secret_ipc_token"  # basic authentication passkey

def handle_client_connection(client_socket, client_address):
    """manages individual client connection threads independently."""
    print(f"[SERVER] -> client connected successfully from: {client_address}")
    try:
        while True:
            raw_data = client_socket.recv(1024).decode("utf-8")
            if not raw_data: break #no data received, client closed connection
            print("received raw payload: " + raw_data)
            
            print(f"[SERVER] -> received raw payload: {raw_data}")
            # ipc protovol envelope validation and command execution logic
            try:
                payload = json.loads(raw_data)
                # check structural presence and token authenticity parameters
                if (
                    "token" not in payload
                    or "command" not in payload
                    or "data" not in payload
                ):
                    response = {
                        "status": "error",
                        "message": "malformed packet structure",
                    }

                elif payload["token"] != AUTH_TOKEN:
                    response = {
                        "status": "error",
                        "message": "invalid security handshake token",
                    }

                else:
                    cmd = payload["command"]
                    user_data = payload["data"]
                    print(f"[SERVER] -> processing verified command [{cmd}] safely.")

                    if cmd == "PING":
                        response = {"status": "success", "message": "PONG"}
                    elif cmd == "UPPERCASE":
                        response = {
                            "status": "success",
                            "message": str(user_data).upper(),
                        }
                    else:
                        response = {
                            "status": "success",
                            "message": "command acknowledged",
                        }

            except json.JSONDecodeError:
                response = {
                    "status": "error",
                    "message": "invalid json payload format",
                }

            client_socket.send(json.dumps(response).encode("utf-8"))

    except Exception as e:
        print(f"[SERVER] -> exception raised during processing: {e}")

    finally:
        # safe resource teardown block ensures ports don't leak[cite: 1]
        client_socket.close()
        print(f"[SERVER] -> connection closed safely for: {client_address}")

def run_ipc_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(5)
    print(f"[SERVER] -> listening actively on tcp://{HOST}:{PORT}")

    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            t = threading.Thread(
                target=handle_client_connection,
                args=(client_sock, client_addr),
            )
            t.start()
    except KeyboardInterrupt:
        print("\n[SERVER] -> server shutting down manually.")
    finally:
        server_sock.close()


if __name__ == "__main__":
    run_ipc_server()