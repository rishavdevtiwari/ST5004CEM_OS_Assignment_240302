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

def authenticate_user():
    """simple credential verification terminal check."""
    print("--- Secure File System Login ---")
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
    create("test.txt")
    
    # testing core cryptographic cipher components
    print("\n--- testing crypto engine strings ---")
    sample = "secret operational payload validation data"
    encrypted = run_xor_cipher(sample, ENCRYPTION_KEY)
    decrypted = run_xor_cipher(encrypted, ENCRYPTION_KEY)
    print("crypto matching validation verified: " + str(sample == decrypted))
    
    user = None
    while user is None:
        user = authenticate_user()