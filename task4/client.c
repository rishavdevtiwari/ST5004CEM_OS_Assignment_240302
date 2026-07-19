#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#include <windows.h>
#define CLOSE_SOCKET(s) closesocket(s)
#define sleep_sec(x) Sleep((DWORD)((x) * 1000))
typedef SOCKET socket_t;
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#define CLOSE_SOCKET(s) close(s)
#define sleep_sec(x) sleep(x)
typedef int socket_t;
#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#endif

#define HOST "127.0.0.1"
#define PORT 9090

char AUTH_TOKEN[64] = "super_secret_ipc_token";

// establishes standard socket connection loop to transmit verified message blocks.
void transmit_ipc_message(const char *command, const char *data_payload) {
#ifdef _WIN32
    WSADATA wsa;
    WSAStartup(MAKEWORD(2, 2), &wsa);
#endif

    socket_t client_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (client_sock == INVALID_SOCKET) {
        printf("[CLIENT] -> socket creation failed\n");
        return;
    }

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, HOST, &server_addr.sin_addr);

    if (connect(client_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        printf("[CLIENT] -> transmission networking failure encountered: connection failed\n");
        CLOSE_SOCKET(client_sock);
#ifdef _WIN32
        WSACleanup();
#endif
        return;
    }

    // application layer protocol envelope construction for IPC message transmission
    char serialized_string[512];
    snprintf(serialized_string, sizeof(serialized_string),
             "{\"token\": \"%s\", \"command\": \"%s\", \"data\": \"%s\"}",
             AUTH_TOKEN, command, data_payload);

    printf("[CLIENT] -> transmitting payload: %s\n", serialized_string);
    fflush(stdout);

    send(client_sock, serialized_string, (int)strlen(serialized_string), 0);

    char server_reply[512] = {0};
    int bytes = recv(client_sock, server_reply, sizeof(server_reply) - 1, 0);
    if (bytes > 0) {
        server_reply[bytes] = '\0';
        printf("[CLIENT] -> incoming server response decoded: %s\n", server_reply);
        fflush(stdout);
    }

    // clear connection cleanup routine execution
    CLOSE_SOCKET(client_sock);
#ifdef _WIN32
    WSACleanup();
#endif
}

int main(void) {
    printf("--- starting network programming ipc validation run ---\n");

    transmit_ipc_message("PING", "hello server node");
    sleep_sec(1);

    transmit_ipc_message("UPPERCASE", "lowercased student message sample");
    sleep_sec(1);

    // security testing block to validate server-side token authentication and command execution logic
    printf("\n--- initiating security boundary validation run ---\n");
    char old_token[64];
    strcpy(old_token, AUTH_TOKEN);
    strcpy(AUTH_TOKEN, "wrong_hacker_token");
    transmit_ipc_message("PING", "malicious attempt");
    strcpy(AUTH_TOKEN, old_token);

    return 0;
}
