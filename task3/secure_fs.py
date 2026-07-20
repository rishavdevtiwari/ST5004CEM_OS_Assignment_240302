import hashlib
import os
import time

# data path - contains user credentials for authentication
USER_DB = "users.txt"
AUDIT_LOG = "audit.log"
ENCRYPTION_KEY = "os_secret_key"  # seed used for our security cipher stream


#security helpers - audit lohher hock tracking
def write_audit_log(user, action, target_file, status):
    """automatically writes structured log entries to our external audit file."""
    # timestamping every action for audit integrity
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] USER: {user} | ACTION: {action} | FILE: {target_file} | STATUS: {status}\n"

    # appending straight to the file system log
    f = open(AUDIT_LOG, "a")
    try:
        f.write(log_entry)
    finally:
        f.close()

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
    write_audit_log(username, "LOGIN", "N/A", "FAILED")
    return None

#comprehensive oobject oriented secure shell interface
class SecureFileSystem:

    def __init__(self):
        # mock internal tracking dictionary representing metadata directory
        self.directory = {}

    def create_file(self, user_ctx, filename, perms):
        # setting up baseline metadata configurations
        self.directory[filename] = {"perms": perms, "content": ""}
        write_audit_log(user_ctx["username"], "CREATE", filename, "SUCCESS")
        print(f"File '{filename}' created successfully.")

    def write_file(self, user_ctx, filename, plain_text):
        if filename not in self.directory:
            print("Error: File not found.")
            return

        # validating permission settings before saving data
        meta = self.directory[filename]
        if not check_permission(user_ctx, meta["perms"], "w"):
            print("Access Denied: You do not have write permissions.")
            write_audit_log(user_ctx["username"], "WRITE", filename, "DENIED")
            return

        # encryption happens right before pushing bytes down to disk storage
        encrypted_data = run_xor_cipher(plain_text, ENCRYPTION_KEY)
        meta["content"] = encrypted_data
        write_audit_log(user_ctx["username"], "WRITE", filename, "SUCCESS")
        print(f"Data safely encrypted and written to '{filename}'.")

    def read_file(self, user_ctx, filename):
        if filename not in self.directory:
            print("Error: File not found.")
            return

        meta = self.directory[filename]
        if not check_permission(user_ctx, meta["perms"], "r"):
            print("Access Denied: You do not have read permissions.")
            write_audit_log(user_ctx["username"], "READ", filename, "DENIED")
            return

        # read decrypts ciphertext back into original plaintext format
        decrypted_data = run_xor_cipher(meta["content"], ENCRYPTION_KEY)
        write_audit_log(user_ctx["username"], "READ", filename, "SUCCESS")
        print(f"[{filename} Content]: {decrypted_data}")

    def delete_file(self, user_ctx, filename):
        if filename not in self.directory:
            print("Error: File not found.")
            return

        meta = self.directory[filename]
        if not check_permission(user_ctx, meta["perms"], "w"):  # write access needed to delete
            print("Access Denied: Insufficient permissions to delete.")
            write_audit_log(user_ctx["username"], "DELETE", filename, "DENIED")
            return

        del self.directory[filename]
        write_audit_log(user_ctx["username"], "DELETE", filename, "SUCCESS")
        print(f"File '{filename}' deleted from directory inventory.")


#main interactive interface
if __name__ == "__main__":
    fs = SecureFileSystem()

    # run authentication system loop first
    user = None
    while user is None:
        user = authenticate_user()

    # setup default dummy sandbox files for testing
    # format layout specifies -> owner_perms : group_perms : other_perms
    fs.create_file(user, "confidential.txt", "rw:r:")
    fs.create_file(user, "public.txt", "rw:r:r")

    # interactive testing execution sequence
    print("\n--- starting secure interaction test routine ---")
    fs.write_file(user, "confidential.txt", "this is a top secret grade file.")
    fs.read_file(user, "confidential.txt")

    # mock a permission restriction scenario by swapping out active contexts
    guest_user = {"username": "guest_user", "group": "guest_group"}
    print("\n--- testing guest context cross-boundary restrictions ---")
    fs.read_file(guest_user, "confidential.txt")  # should trigger authorization failure
    fs.read_file(guest_user, "public.txt")  # should succeed under other access rules

    print(f"\n[INFO] Complete operations recorded inside external '{AUDIT_LOG}' file.")