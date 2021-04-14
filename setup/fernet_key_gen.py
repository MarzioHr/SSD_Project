"""Module to generate initial Fernet Master Key."""

from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(f"Key Generated: {key}")

with open("key.bin", "wb") as key_file:
    key_file.write(key)
