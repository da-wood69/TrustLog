import os
from cryptography.fernet import Fernet

ENV_FILE = ".env"
KEY_VAR = "ENCRYPT_KEY"

def write_key_to_env(key):
    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()
        # Remove existing key line if present
        lines = [line for line in lines if not line.startswith(f"{KEY_VAR}=")]
    lines.append(f"{KEY_VAR}={key.decode()}\n")
    with open(ENV_FILE, "w") as f:
        f.writelines(lines)

def main():
    print("WARNING: Generating a new Fernet key will overwrite the existing key in .env.")
    print("This will make all previously encrypted data unrecoverable!")
    confirm = input("Are you sure you want to continue? [y/N]: ").strip().lower()
    if confirm != "y":
        print("Operation cancelled.")
        return
    key = Fernet.generate_key()
    write_key_to_env(key)
    print(f"New Fernet key generated and saved to {ENV_FILE} as {KEY_VAR}.")

if __name__ == "__main__":
    main()