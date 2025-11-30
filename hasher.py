import hashlib
from argon2 import PasswordHasher

class HashProcessor:
    """
    A class dedicated to processing text usinng various SHA-2 family hash algoriothms.
    """

    def __init__(self):
        self.sha_hashes = ["SHA-224", "SHA-256", "SHA-384", "SHA-512"]
        self.ph = PasswordHasher()
    
    def hash_text(self, text: str, algorithm: str) -> str:
        """
        Hashes the given text using the specified algorithm
        """

        if algorithm in self.sha_hashes:
            hash_func_name = algorithm.replace('-', '').lower()

            try:
                hasher = hashlib.new(hash_func_name)
                data_bytes = text.encode('utf-8')
                hasher.update(data_bytes)
                return hasher.hexdigest()
            
            except Exception as e:
                return f"Error with hashlib: {e}"
        
        elif algorithm == "Argon2":
            try:
                return self.ph.hash(text)
            except Exception as e:
                return f"Error with Argon2: {e}"
            
        else:
            return f"Error: Algorithm {algorithm} not supported by this version."
    
    def hash_file(self, file_path: str, algorith: str) -> str:
        """
        Hashes the content of a file using the specified SHA algorithm.
        Reads file in 64 KB chunks for memory efficiency.
        """

        if algorith not in self.sha_hashes:
            return f"Error: File hashing is not supported for {algorith}."
        
        hash_func_name = algorith.replace('-', '').lower()

        try:
            hasher = hashlib.new(hash_func_name)

            with open(file_path, 'rb') as f:
                chunk = 0
                while chunk != b'':
                    chunk = f.read(65536)
                    hasher.update(chunk)
            
            return hasher.hexdigest()
        
        except FileNotFoundError:
            return f"Error: File not found or path is invalid."
        except Exception as e:
            return f"An error occurred during file hashing: {e}"

# Simple Test case to verify the hasher works
if __name__ == "__main__":
    processor = HashProcessor()
    test_text = "All your base are belong to us"

    print(f"Original Text: {test_text}\n")
    print(f"SHA-256 Hash: {processor.hash_text(test_text, 'SHA-256')}")
    print(f"Argon2 Hash: {processor.hash_text(test_text, 'Argon2')}")