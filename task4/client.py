import socket
import time

HOST = "127.0.0.1"
PORT = 8080

def transmit_ipc_message(msg):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_sock.connect((HOST, PORT))
        print("sending: " + msg)
        client_sock.send(msg.encode("utf-8"))
        reply = client_sock.recv(1024).decode("utf-8")
        print("server replied: " + reply)
    finally:
        client_sock.close()

if __name__ == "__main__":
    transmit_ipc_message("test message loop 1")
    time.sleep(1)
    transmit_ipc_message("test message loop 2")