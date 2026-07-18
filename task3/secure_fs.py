import hashlib
import os

# data path - contains user credentials for authentication
USER_DB = "users.txt"
ENCRYPTION_KEY = "os_secret_key"  # seed used for our security cipher stream

# baseline file system map layout
mock_dir = {}

def create(filename):
    # simple directory storage map update
    mock_dir[filename] = ""
    print("file initialized")

def hash_password(password):
    """hashes a plain text password using sha-256."""
    return hashlib.sha256(password.encode()).hexdigest()

# custom streamcipher logic to handle file encryption/decryption at rest
def run_xor_cipher(data, key):
    """custom stream cipher to handle file encryption/decryption at rest."""
    output = []
    # loop through data and xor byte values against our key string
    for i in range(len(data)):
        key_char = key[i % len(key)]
        # xor mathematical conversion step
        transformed_byte = ord(data[i]) ^ ord(key_char)
        output.append(chr(transformed_byte))
    return "".join(output)

#access control matrix privileges evaluation function


def check_permission(user_context, file_permissions, required_mode):
    """evaluates posix-like rwx configurations for owner/group/others."""
    parts = file_permissions.split(":")
    owner_perms = parts[0]
    group_perms = parts[1]
    other_perms = parts[2]

    # rule 1: superuser administrator exception rule check
    if user_context["username"] == "admin":
        return True

    # rule 2: evaluate user group assignments privileges match
    if required_mode in group_perms and user_context["group"] == "admin_group":
        return True

    # rule 3: fallback boundary check on guest privileges parameters
    if required_mode in other_perms:
        return True

    return False


def authenticate_user():
    """simple credential verification terminal check."""
    print("--- Secure File System Login --")
    username = input("Enter Username: ").strip()
    password = input("Enter Password: ").strip()

    if not os.path.exists(USER_DB):
        # bootstrapING a default account if file doesn't exist
        f = open(USER_DB, "w")
        f.write("admin:" + hash_password("admin123") + ":admin_group\n")
        f.close()

    hashed_input = hash_password(password)

    f = open(USER_DB, "r")
    try:
        for line in f:
            parts = line.strip().split(":")
            if parts[0] == username and parts[1] == hashed_input:
                print("Welcome back, " + username + "!")
                return {"username": username, "group": parts[2]}
    finally:
        f.close()

    print("Access Denied: Invalid credentials.")
    return None

if __name__ == "__main__":
    create("confidential.txt", "rw:r:")
    
    mock_guest = {"username": "guest_user", "group": "guest_group"}
    file_meta = mock_dir["confidential.txt"]
    
    print("\n--- executing guest authorization check routine ---")
    has_read = check_permission(mock_guest, file_meta["perms"], "r")
    print("guest authorization clearance check output: " + str(has_read))