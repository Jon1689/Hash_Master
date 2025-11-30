# Hash Master 🔐

## Integrity and Cryptography Tool

Hash Master is a desktop application built with Python and CustomTkinter, designed for cybersecurity students and professionals. It provides a clean, fast interface for performing cryptographic hash digests on both **text input** and **large files** to verify data integrity and explore modern password hashing techniques.

The application uses a **modular architecture** (separating GUI from core logic) and **multithreading** for file operations to ensure a responsive user experience, even when processing large datasets.

---

## ✨ Features

* **Multi-Algorithm Support:** Calculate hashes using the SHA-2 family (SHA-224, SHA-256, SHA-384, SHA-512) and the modern password hashing algorithm, Argon2.
* **Text and File Hashing:** Seamlessly switch between hashing custom text input and checking the integrity of large files.
* **Robust File Integrity:** File hashing is handled in memory-efficient **chunks** within a **separate thread** to prevent the main application from freezing.
* **Clear UX:** Includes a **"Copy to Clipboard"** button and clear visual indicators for input methods (text vs. file).
* **Professional Error Handling:** Provides descriptive error messages for file issues (e.g., file not found, permission denied).
* **Argon2 Salting:** Correctly implements Argon2, generating a new unique salt for every hash operation (resulting in unique output for the same input, a key security feature).

---

## 🛠️ Installation & Setup

### Prerequisites

You need Python 3.8+ installed.

1.  **CustomTkinter:** Used for the modern GUI design.
2.  **Argon2-cffi:** Used for the secure password hashing algorithm.

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Jon1689/Hash_Master.git
    cd Hash_Master
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file containing `customtkinter` and `argon2-cffi`.)*

3.  **Ensure File Structure:**
    Verify your project has the following file structure:
    ```
    Hash_Master/
    ├── main.py
    └── hasher.py
    ```

---

## 🚀 Usage

To run the application, execute the `main.py` file:

```bash
python main.py
