import json
import socket
import time

HOST = "127.0.0.1"
PORT = 8080
AUTH_TOKEN = "super_secret_ipc_token"

def transmit_ipc_message(command, data_payload):
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
        print("sending serialized payload: " + serialized_string)
        client_sock.send(serialized_string.encode("utf-8"))
        
        reply = client_sock.recv(1024).decode("utf-8")
        print("server replied: " + reply)
    finally:
        client_sock.close()

if __name__ == "__main__":
    transmit_ipc_message("PING", "checking system lines")
    time.sleep(1)
    transmit_ipc_message("UPPERCASE", "lowercased student message sample")