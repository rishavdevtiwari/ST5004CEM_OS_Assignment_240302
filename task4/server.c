#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <pthread.h>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
#define CLOSE_SOCKET(s) closesocket(s)
typedef SOCKET socket_t;
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#define CLOSE_SOCKET(s) close(s)
typedef int socket_t;
#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#endif

#define HOST "127.0.0.1"
#define PORT 9090
#define AUTH_TOKEN "super_secret_ipc_token" // basic authentication passkey

typedef struct {
    socket_t client_sock;
    struct sockaddr_in client_addr;
} ClientContext;

// helper function to extract json string field values cleanly
int extract_json_field(const char *json, const char *key, char *out_val, size_t out_size) {
    char search_key[64];
    snprintf(search_key, sizeof(search_key), "\"%s\"", key);
    const char *pos = strstr(json, search_key);
    if (!pos) return 0;

    pos = strchr(pos, ':');
    if (!pos) return 0;
    pos++;
    while (*pos == ' ' || *pos == '\t') pos++;

    if (*pos == '"') {
        pos++;
        const char *end = strchr(pos, '"');
        if (!end) return 0;
        size_t len = end - pos;
        if (len >= out_size) len = out_size - 1;
        strncpy(out_val, pos, len);
        out_val[len] = '\0';
        return 1;
    }
    return 0;
}

// manages individual client connection threads independently.
void *handle_client_connection(void *arg) {
    ClientContext *ctx = (ClientContext *)arg;
    socket_t client_socket = ctx->client_sock;
    char client_ip[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &(ctx->client_addr.sin_addr), client_ip, INET_ADDRSTRLEN);
    int client_port = ntohs(ctx->client_addr.sin_port);

    printf("[SERVER] -> client connected successfully from: (%s, %d)\n", client_ip, client_port);
    fflush(stdout);

    char buffer[1024];
    while (1) {
        memset(buffer, 0, sizeof(buffer));
        int bytes_received = recv(client_socket, buffer, sizeof(buffer) - 1, 0);
        if (bytes_received <= 0) break; // no data received, client closed connection

        printf("[SERVER] -> received raw payload: %s\n", buffer);
        fflush(stdout);

        char token[128] = {0};
        char command[128] = {0};
        char data[256] = {0};
        char response[512] = {0};

        int has_token = extract_json_field(buffer, "token", token, sizeof(token));
        int has_command = extract_json_field(buffer, "command", command, sizeof(command));
        int has_data = extract_json_field(buffer, "data", data, sizeof(data));

        // ipc protocol envelope validation and command execution logic
        if (!has_token || !has_command || !has_data) {
            strcpy(response, "{\"status\": \"error\", \"message\": \"malformed packet structure\"}");
        } else if (strcmp(token, AUTH_TOKEN) != 0) {
            strcpy(response, "{\"status\": \"error\", \"message\": \"invalid security handshake token\"}");
        } else {
            printf("[SERVER] -> processing verified command [%s] safely.\n", command);
            fflush(stdout);

            if (strcmp(command, "PING") == 0) {
                strcpy(response, "{\"status\": \"success\", \"message\": \"PONG\"}");
            } else if (strcmp(command, "UPPERCASE") == 0) {
                char upper_data[256];
                int i = 0;
                while (data[i] != '\0') {
                    upper_data[i] = toupper((unsigned char)data[i]);
                    i++;
                }
                upper_data[i] = '\0';
                snprintf(response, sizeof(response), "{\"status\": \"success\", \"message\": \"%s\"}", upper_data);
            } else {
                strcpy(response, "{\"status\": \"success\", \"message\": \"command acknowledged\"}");
            }
        }

        send(client_socket, response, (int)strlen(response), 0);
    }

    // safe resource teardown block ensures ports don't leak
    CLOSE_SOCKET(client_socket);
    printf("[SERVER] -> connection closed safely for: (%s, %d)\n", client_ip, client_port);
    fflush(stdout);
    free(ctx);
    return NULL;
}

void run_ipc_server(void) {
#ifdef _WIN32
    WSADATA wsa;
    WSAStartup(MAKEWORD(2, 2), &wsa);
#endif

    socket_t server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock == INVALID_SOCKET) {
        perror("socket creation failed");
        return;
    }

    int opt = 1;
    setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, (const char *)&opt, sizeof(opt));

    struct sockaddr_in server_addr;
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    inet_pton(AF_INET, HOST, &server_addr.sin_addr);

    if (bind(server_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        perror("bind failed");
        CLOSE_SOCKET(server_sock);
        return;
    }

    listen(server_sock, 5);
    printf("[SERVER] -> listening actively on tcp://%s:%d\n", HOST, PORT);
    fflush(stdout);

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t addr_len = sizeof(client_addr);
        socket_t client_sock = accept(server_sock, (struct sockaddr *)&client_addr, &addr_len);

        if (client_sock == INVALID_SOCKET) break;

        ClientContext *ctx = (ClientContext *)malloc(sizeof(ClientContext));
        ctx->client_sock = client_sock;
        ctx->client_addr = client_addr;

        pthread_t tid;
        pthread_create(&tid, NULL, handle_client_connection, ctx);
        pthread_detach(tid);
    }

    CLOSE_SOCKET(server_sock);
#ifdef _WIN32
    WSACleanup();
#endif
}

int main(void) {
    run_ipc_server();
    return 0;
}
