import json
import socket
import time

HOST = "127.0.0.1"
PORT = 8080
AUTH_TOKEN = "super_secret_ipc_token"

def transmit_ipc_message(command, data_payload):
    """establishes standard socket connection loop to transmit verified message blocks."""
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_sock.connect((HOST, PORT))
        
        #application layer protocol envelope construction for IPC message transmission
        packet_envelope = {
            "token": AUTH_TOKEN,
            "command": command,
            "data": data_payload
        }
        
        serialized_string = json.dumps(packet_envelope)
        print(f"[CLIENT] -> transmitting payload: {serialized_string}")

        client_sock.send(serialized_string.encode("utf-8"))

        server_reply = client_sock.recv(1024).decode("utf-8")
        print(f"[CLIENT] -> incoming server response decoded: {server_reply}")

    except Exception as e:
        print(f"[CLIENT] -> transmission networking failure encountered: {e}")

    finally:
        # clear connection cleanup routine execution[cite: 1]
        client_sock.close()

if __name__ == "__main__":
    print("--- starting network programming ipc validation run ---")

    transmit_ipc_message("PING", "hello server node")
    time.sleep(1)

    transmit_ipc_message("UPPERCASE", "lowercased student message sample")
    time.sleep(1)

#security testing block to validate server-side token authentication and command execution logic
    print("\n--- initiating security boundary validation run ---")
    old_token = AUTH_TOKEN
    AUTH_TOKEN = "wrong_hacker_token"
    transmit_ipc_message("PING", "malicious attempt")
    AUTH_TOKEN = old_token