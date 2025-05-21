import os
import sqlite3
import getpass
import base64
from cryptography.fernet import Fernet
from pathlib import Path
from dotenv import load_dotenv

# ASCII Art Welcome
WELCOME_ART = r"""
████████╗██████╗ ██╗   ██╗███████╗████████╗     ██╗      ██████╗  ██████╗ 
╚══██╔══╝██╔══██╗██║   ██║██╔════╝╚══██╔══╝     ██║     ██╔═══██╗██╔════╝ 
    ██║   ██████╔╝██║   ██║███████╗   ██║        ██║     ██║   ██║██║  ███╗
    ██║   ██╔══██╗██║   ██║╚════██║   ██║        ██║     ██║   ██║██║   ██║
    ██║   ██║  ██║╚██████╔╝███████║   ██║        ███████╗╚██████╔╝╚██████╔╝
    ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝        ╚══════╝ ╚═════╝  ╚═════╝ 
                                                                                                  
Welcome to TrustLog Setup! 🚀
"""

def print_separator():
     print("=" * 72)

def get_env_key():
     load_dotenv()
     key = os.getenv("ENCRYPT_KEY")
     if not key:
          key = Fernet.generate_key()
          print("No ENCRYPT_KEY found in .env. Generating a new one for you.")
          print(f"Add this to your .env file:\nENCRYPT_KEY={key.decode()}")
          exit(1)
     try:
          # Validate key
          Fernet(key)
     except Exception:
          print("Invalid ENCRYPT_KEY in .env. Must be a valid Fernet key.")
          exit(1)
     return key.encode() if isinstance(key, str) else key

def encrypt_data(fernet, data):
     return fernet.encrypt(data.encode())

def decrypt_data(fernet, token):
     return fernet.decrypt(token).decode()

def get_input(prompt, secret=False):
     if secret:
          return getpass.getpass(prompt)
     else:
          return input(prompt)

def setup_database(db_path, fernet):
     Path(db_path).parent.mkdir(parents=True, exist_ok=True)
     conn = sqlite3.connect(db_path)
     c = conn.cursor()
     c.execute("""
          CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host BLOB NOT NULL,
                port BLOB NOT NULL,
                username BLOB NOT NULL,
                password BLOB NOT NULL
          )
     """)
     conn.commit()
     return conn

def main():
     print(WELCOME_ART)
     print_separator()
     print("Let's get your SFTP server details securely stored! 🔒\n")

     key = get_env_key()
     fernet = Fernet(key)

     host = get_input("SFTP Host: ")
     port = get_input("SFTP Port [2022]: ") or "2022"
     username = get_input("SFTP Username: ")
     password = get_input("SFTP Password: ", secret=True)

     db_path = os.path.join("database", "servers.db")
     conn = setup_database(db_path, fernet)
     c = conn.cursor()

     c.execute("INSERT INTO servers (host, port, username, password) VALUES (?, ?, ?, ?)", (
          encrypt_data(fernet, host),
          encrypt_data(fernet, port),
          encrypt_data(fernet, username),
          encrypt_data(fernet, password)
     ))
     conn.commit()
     conn.close()

     print_separator()
     print("🎉 Success! Your SFTP server details are securely stored in TrustLog.")
     print("You can now use TrustLog with peace of mind. Have a great day! 🌈\n")

if __name__ == "__main__":
     main()