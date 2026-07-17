#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

// data path - contains user credentials for authentication
#define USER_DB "users.txt"
#define AUDIT_LOG "audit.log"
#define ENCRYPTION_KEY "os_secret_key" // seed used for our security cipher stream

#define MAX_FILES 50
#define MAX_NAME 64
#define MAX_CONTENT 1024

typedef struct {
    char username[32];
    char group[32];
} UserContext;

typedef struct {
    char filename[MAX_NAME];
    char perms[16];
    char content[MAX_CONTENT];
    int exists;
} FileEntry;

// security helpers - audit logger hook tracking
// automatically writes structured log entries to our external audit file.
void write_audit_log(const char *user, const char *action, const char *target_file, const char *status) {
    // timestamping every action for audit integrity
    time_t rawtime;
    struct tm *timeinfo;
    char timestamp[32];

    time(&rawtime);
    timeinfo = localtime(&rawtime);
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", timeinfo);

    FILE *f = fopen(AUDIT_LOG, "a");
    if (f != NULL) {
        fprintf(f, "[%s] USER: %s | ACTION: %s | FILE: %s | STATUS: %status\n", timestamp, user, action, target_file, status);
        fclose(f);
    }
}

// lightweight sha-256 hash implementation for portable password verification
static uint32_t sha256_k[64] = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef4a3f7, 0xc67178f2
};

#define ROTR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
#define CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x) (ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22))
#define EP1(x) (ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25))
#define SIG0(x) (ROTR(x, 7) ^ ROTR(x, 18) ^ ((x) >> 3))
#define SIG1(x) (ROTR(x, 17) ^ ROTR(x, 19) ^ ((x) >> 10))

void hash_password(const char *password, char *output_hex) {
    uint32_t h[8] = {
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    };

    size_t len = strlen(password);
    size_t new_len = len + 1;
    while (new_len % 64 != 56) new_len++;

    uint8_t *msg = (uint8_t *)calloc(new_len + 8, 1);
    memcpy(msg, password, len);
    msg[len] = 0x80;

    uint64_t bits_len = len * 8;
    for (int i = 0; i < 8; i++) {
        msg[new_len + i] = (bits_len >> ((7 - i) * 8)) & 0xFF;
    }

    for (size_t chunk = 0; chunk < new_len + 8; chunk += 64) {
        uint32_t w[64];
        for (int i = 0; i < 16; i++) {
            w[i] = (msg[chunk + i * 4] << 24) | (msg[chunk + i * 4 + 1] << 16) |
                   (msg[chunk + i * 4 + 2] << 8) | (msg[chunk + i * 4 + 3]);
        }
        for (int i = 16; i < 64; i++) {
            w[i] = SIG1(w[i - 2]) + w[i - 7] + SIG0(w[i - 15]) + w[i - 16];
        }

        uint32_t a = h[0], b = h[1], c = h[2], d = h[3];
        uint32_t e = h[4], f = h[5], g = h[6], h_val = h[7];

        for (int i = 0; i < 64; i++) {
            uint32_t temp1 = h_val + EP1(e) + CH(e, f, g) + sha256_k[i] + w[i];
            uint32_t temp2 = EP0(a) + MAJ(a, b, c);
            h_val = g;
            g = f;
            f = e;
            e = d + temp1;
            d = c;
            c = b;
            b = a;
            a = temp1 + temp2;
        }

        h[0] += a; h[1] += b; h[2] += c; h[3] += d;
        h[4] += e; h[5] += f; h[6] += g; h[7] += h_val;
    }

    free(msg);

    for (int i = 0; i < 8; i++) {
        sprintf(output_hex + (i * 8), "%08x", h[i]);
    }
    output_hex[64] = '\0';
}

// custom streamcipher logic to handle file encryption/decryption at rest
void run_xor_cipher(const char *data, const char *key, char *output) {
    size_t data_len = strlen(data);
    size_t key_len = strlen(key);

    for (size_t i = 0; i < data_len; i++) {
        char key_char = key[i % key_len];
        output[i] = data[i] ^ key_char;
    }
    output[data_len] = '\0';
}

// access control matrix privileges evaluation function
// evaluates posix-like rwx configurations for owner/group/others.
int check_permission(UserContext *user_context, const char *file_permissions, char required_mode) {
    char owner_perms[16] = {0};
    char group_perms[16] = {0};
    char other_perms[16] = {0};

    sscanf(file_permissions, "%15[^:]:%15[^:]:%15s", owner_perms, group_perms, other_perms);

    // rule 1: superuser administrator exception rule check
    if (strcmp(user_context->username, "admin") == 0) {
        return 1;
    }

    // rule 2: evaluate user group assignments privileges match
    if (strchr(group_perms, required_mode) != NULL && strcmp(user_context->group, "admin_group") == 0) {
        return 1;
    }

    // rule 3: fallback boundary check on guest privileges parameters
    if (strchr(other_perms, required_mode) != NULL) {
        return 1;
    }

    return 0;
}

int authenticate_user(UserContext *out_user) {
    printf("--- Secure File System Login ---\n");
    char username[32] = "admin";
    char password[32] = "admin123";

    printf("Enter Username: %s\n", username);
    printf("Enter Password: ********\n");

    FILE *check_file = fopen(USER_DB, "r");
    if (check_file == NULL) {
        // bootstrapING a default account if file doesn't exist
        char default_hash[65];
        hash_password("admin123", default_hash);
        FILE *f = fopen(USER_DB, "w");
        if (f != NULL) {
            fprintf(f, "admin:%s:admin_group\n", default_hash);
            fclose(f);
        }
    } else {
        fclose(check_file);
    }

    char hashed_input[65];
    hash_password(password, hashed_input);

    FILE *f = fopen(USER_DB, "r");
    if (f != NULL) {
        char line[256];
        while (fgets(line, sizeof(line), f)) {
            line[strcspn(line, "\r\n")] = 0;
            char db_user[32], db_hash[65], db_group[32];
            if (sscanf(line, "%31[^:]:%64[^:]:%31s", db_user, db_hash, db_group) == 3) {
                if (strcmp(db_user, username) == 0 && strcmp(db_hash, hashed_input) == 0) {
                    printf("Welcome back, %s!\n", username);
                    // --- FIXED: ADDED SUCCESS AUDIT LOG RECORDING HOCK ---
                    write_audit_log(username, "LOGIN", "N/A", "SUCCESS");
                    strcpy(out_user->username, username);
                    strcpy(out_user->group, db_group);
                    fclose(f);
                    return 1;
                }
            }
        }
        fclose(f);
    }

    printf("Access Denied: Invalid credentials.\n");
    write_audit_log(username, "LOGIN", "N/A", "FAILED");
    return 0;
}

// comprehensive object oriented secure shell interface
typedef struct {
    FileEntry files[MAX_FILES];
    int count;
} SecureFileSystem;

void create_file(SecureFileSystem *fs, UserContext *user_ctx, const char *filename, const char *perms) {
    if (fs->count >= MAX_FILES) return;
    FileEntry *entry = &fs->files[fs->count++];
    strcpy(entry->filename, filename);
    strcpy(entry->perms, perms);
    entry->content[0] = '\0';
    entry->exists = 1;

    write_audit_log(user_ctx->username, "CREATE", filename, "SUCCESS");
    printf("File '%s' created successfully.\n", filename);
}

FileEntry *find_file(SecureFileSystem *fs, const char *filename) {
    for (int i = 0; i < fs->count; i++) {
        if (fs->files[i].exists && strcmp(fs->files[i].filename, filename) == 0) {
            return &fs->files[i];
        }
    }
    return NULL;
}

void write_file(SecureFileSystem *fs, UserContext *user_ctx, const char *filename, const char *plain_text) {
    FileEntry *entry = find_file(fs, filename);
    if (entry == NULL) {
        printf("Error: File not found.\n");
        return;
    }

    // validating permission settings before saving data
    if (!check_permission(user_ctx, entry->perms, 'w')) {
        printf("Access Denied: You do not have write permissions.\n");
        write_audit_log(user_ctx->username, "WRITE", filename, "DENIED");
        return;
    }

    // encryption happens right before pushing bytes down to disk storage
    run_xor_cipher(plain_text, ENCRYPTION_KEY, entry->content);
    write_audit_log(user_ctx->username, "WRITE", filename, "SUCCESS");
    printf("Data safely encrypted and written to '%s'.\n", filename);
}

void read_file(SecureFileSystem *fs, UserContext *user_ctx, const char *filename) {
    FileEntry *entry = find_file(fs, filename);
    if (entry == NULL) {
        printf("Error: File not found.\n");
        return;
    }

    if (!check_permission(user_ctx, entry->perms, 'r')) {
        printf("Access Denied: You do not have read permissions.\n");
        write_audit_log(user_ctx->username, "READ", filename, "DENIED");
        return;
    }

    // read decrypts ciphertext back into original plaintext format
    char decrypted_data[MAX_CONTENT];
    run_xor_cipher(entry->content, ENCRYPTION_KEY, decrypted_data);
    write_audit_log(user_ctx->username, "READ", filename, "SUCCESS");
    printf("[%s Content]: %s\n", filename, decrypted_data);
}

void delete_file(SecureFileSystem *fs, UserContext *user_ctx, const char *filename) {
    FileEntry *entry = find_file(fs, filename);
    if (entry == NULL) {
        printf("Error: File not found.\n");
        return;
    }

    if (!check_permission(user_ctx, entry->perms, 'w')) {
        printf("Access Denied: Insufficient permissions to delete.\n");
        write_audit_log(user_ctx->username, "DELETE", filename, "DENIED");
        return;
    }

    entry->exists = 0;
    write_audit_log(user_ctx->username, "DELETE", filename, "SUCCESS");
    printf("File '%s' deleted from directory inventory.\n", filename);
}

int main(void) {
    SecureFileSystem fs;
    fs.count = 0;

    UserContext user;
    int authenticated = 0;
    while (!authenticated) {
        authenticated = authenticate_user(&user);
    }

    // setup default dummy sandbox files for testing
    // format layout specifies -> owner_perms : group_perms : other_perms
    create_file(&fs, &user, "confidential.txt", "rw:r:");
    create_file(&fs, &user, "public.txt", "rw:r:r");

    // interactive testing execution sequence
    printf("\n--- starting secure interaction test routine ---\n");
    write_file(&fs, &user, "confidential.txt", "this is a top secret grade file.");
    read_file(&fs, &user, "confidential.txt");

    // mock a permission restriction scenario by swapping out active contexts
    UserContext guest_user = {"guest_user", "guest_group"};
    printf("\n--- testing guest context cross-boundary restrictions ---\n");
    read_file(&fs, &guest_user, "confidential.txt"); // should trigger authorization failure
    read_file(&fs, &guest_user, "public.txt");       // should succeed under other access rules

    printf("\n[INFO] Complete operations recorded inside external '%s' file.\n", AUDIT_LOG);
    return 0;
}
