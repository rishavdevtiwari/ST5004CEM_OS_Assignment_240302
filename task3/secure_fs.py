import hashlib
import os

# data path - contains user credentials for authentication
USER_DB = "users.txt"

# baseline file system map layout
mock_dir = {}

def create(filename):
    # simple directory storage map update
    mock_dir[filename] = ""
    print("file initialized")

def hash_password(password):
    """hashes a plain text password using sha-256."""
    return hashlib.sha256(password.encode()).hexdigest()

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
    user = None
    while user is None:
        user = authenticate_user()