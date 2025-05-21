import os
import time
import threading
import sqlite3
import paramiko
from flask import Flask, send_from_directory
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from parser import parse_minecraft_log
from flask import render_template
import json
from flask import request
import gzip

load_dotenv()
FERNET_KEY = os.getenv("ENCRYPT_KEY")
if not FERNET_KEY:
    raise RuntimeError("ENCRYPT_KEY not found in .env")
fernet = Fernet(FERNET_KEY.encode())

def decrypt(blob):
    return fernet.decrypt(blob).decode()

def download_log():
    while True:
        conn = sqlite3.connect('database/servers.db')
        cursor = conn.cursor()
        cursor.execute("SELECT host, port, username, password FROM servers LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            host = decrypt(row[0])
            port = int(decrypt(row[1]))
            username = decrypt(row[2])
            password = decrypt(row[3])
            remote_path = "logs"

            local_dir = 'downloads'
            local_path = os.path.join(local_dir, 'latest.log')
            os.makedirs(local_dir, exist_ok=True)

            try:
                transport = paramiko.Transport((host, port))
                transport.connect(username=username, password=password)
                sftp = paramiko.SFTPClient.from_transport(transport)
                sftp.get(f"{remote_path}/latest.log", local_path)
                sftp.close()
                transport.close()
            except Exception as e:
                print(f"Error downloading log: {e}")

        time.sleep(10)

threading.Thread(target=download_log, daemon=True).start()

app = Flask(__name__)

@app.route('/latest')
def serve_log():
    file_path = os.path.join('downloads', 'latest.log')
    if not os.path.exists(file_path):
        return "Log file not found.", 404
    try:
        parsed_output = parse_minecraft_log(file_path)
        if isinstance(parsed_output, str):
            try:
                parsed_output = json.loads(parsed_output)
            except Exception:
                parsed_output = []
        if not isinstance(parsed_output, list):
            parsed_output = []
        log_entries = []
        for entry in parsed_output:
            if isinstance(entry, dict) and all(k in entry for k in ("type", "content", "time")):
                log_entries.append(entry)
        return render_template('viewer.html', log_entries=log_entries)
    except Exception as e:
        return f"Error parsing log: {e}", 500

@app.route('/archive')
def serve_archive():
    conn = sqlite3.connect('database/servers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT host, port, username, password FROM servers LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if not row:
        return "Server credentials not found.", 404

    host = decrypt(row[0])
    port = int(decrypt(row[1]))
    username = decrypt(row[2])
    password = decrypt(row[3])
    remote_path = "logs"

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        files = sftp.listdir(remote_path)
        log_files = [
            os.path.splitext(f)[0]
            for f in files
        ]
        sftp.close()
        transport.close()
    except Exception as e:
        return f"Error accessing remote logs: {e}", 500

    print("Log files found:", log_files)
    return render_template('archive.html', log_files=log_files)

@app.route('/view_archive')
def server_log_file():
    filename = request.args.get('filename')
    if not filename:
        return "Filename not specified.", 400

    conn = sqlite3.connect('database/servers.db')
    cursor = conn.cursor()
    cursor.execute("SELECT host, port, username, password FROM servers LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if not row:
        return "Server credentials not found.", 404

    host = decrypt(row[0])
    port = int(decrypt(row[1]))
    username = decrypt(row[2])
    password = decrypt(row[3])
    remote_path = "logs"

    local_dir = 'downloads'
    gz_filename = f"{filename}.gz"
    log_filename = f"{filename}.log"
    local_gz_path = os.path.join(local_dir, gz_filename)
    local_log_path = os.path.join(local_dir, log_filename)

    os.makedirs(local_dir, exist_ok=True)

    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        remote_gz_path = f"{remote_path}/{gz_filename}"
        sftp.get(remote_gz_path, local_gz_path)
        sftp.close()
        transport.close()
    except Exception as e:
        return f"Error downloading log archive: {e}", 500

    try:
        with gzip.open(local_gz_path, 'rb') as f_in, open(local_log_path, 'wb') as f_out:
            f_out.write(f_in.read())
        os.remove(local_gz_path)
    except Exception as e:
        return f"Error extracting log file: {e}", 500

    try:
        parsed_output = parse_minecraft_log(local_log_path)
        if isinstance(parsed_output, str):
            try:
                parsed_output = json.loads(parsed_output)
            except Exception:
                parsed_output = []
        if not isinstance(parsed_output, list):
            parsed_output = []
        log_entries = []
        for entry in parsed_output:
            if isinstance(entry, dict) and all(k in entry for k in ("type", "content", "time")):
                log_entries.append(entry)
        return render_template('viewer.html', log_entries=log_entries)
    except Exception as e:
        return f"Error parsing log: {e}", 500

if __name__ == '__main__':
    app.run(port=5000)