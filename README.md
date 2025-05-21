# 🛡️ TrustLog

**TrustLog** is a secure, modern Minecraft server log viewer and archiver.  
It fetches, decrypts, and displays your server logs in a beautiful web UI, with search and filtering, all while keeping your credentials safe.

---

## ✨ Features

- 🔒 **Encrypted SFTP Credentials** — Your server info is always safe.
- 📜 **Live Log Viewer** — See your latest logs in real time.
- 🗂️ **Archive Browser** — Browse and view historical logs.
- 🔍 **Search & Filter** — Instantly search and filter by log type or content.
- 🎨 **Modern UI** — Responsive, clean, and easy to use (Bootstrap 5).
- 🛠️ **Easy Setup** — One command to get started.

---

## 🚀 Quickstart

1. **Clone the repo**
    ```sh
    git clone https://github.com/da-wood69/TrustLog.git
    cd TrustLog
    ```

2. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

3. **Generate encryption key**
    ```sh
    python generate.py
    ```
    > ⚠️ This will create a `.env` file with your encryption key.

4. **Add your SFTP server**
    ```sh
    python setup.py
    ```
    - Enter your SFTP host, port, username, and password when prompted.

5. **Run the app**
    ```sh
    python app.py
    ```
    - Visit [http://localhost:5000/latest](http://localhost:5000/latest) for the latest log.
    - Visit [http://localhost:5000/archive](http://localhost:5000/archive) for the archive.

---

## 📸 Screenshots

![TrustLog Viewer Screenshot](https://raw.githubusercontent.com/da-wood69/TrustLog/main/.github/screenshot-viewer.png)
![TrustLog Archive Screenshot](https://raw.githubusercontent.com/da-wood69/TrustLog/main/.github/screenshot-archive.png)

---

## 🧩 Project Structure

```
TrustLog/
├── app.py              # Main Flask app
├── setup.py            # SFTP credential setup (encrypted)
├── generate.py         # Fernet key generator
├── parser.py           # Minecraft log parser
├── requirements.txt
├── .env                # Encryption key (never share this!)
├── database/
│   └── servers.db      # Encrypted SFTP credentials
├── downloads/          # Downloaded logs (auto-created)
└── templates/
    ├── viewer.html     # Log viewer UI
    └── archive.html    # Archive browser UI
```

---

## 🛡️ Security

- All SFTP credentials are **encrypted** using [Fernet](https://cryptography.io/en/latest/fernet/) and never stored in plaintext.
- The `.env` file contains your encryption key. **Do not share it!**
- Add `.env`, `downloads/`, and `database/servers.db` to your `.gitignore` (already done).

---

## 📝 License

MIT — see [LICENSE](LICENSE)

---

## 👤 Author

Made by [Dawood](https://dawoood.tech)  
Open source on [GitHub](https://github.com/da-wood69/TrustLog) ❤️

---