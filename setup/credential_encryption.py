"""Module to demonstrate the DB Credential Encryption using Fernet."""

from cryptography.fernet import Fernet

KEY_FILE = "config/key.bin"
CLEAR_INPUT = "setup/psql_clear_credentials.txt"

fopen = open(KEY_FILE,"rb")
key = fopen.read()
fopen.close()

fopen = open(CLEAR_INPUT,"rb")
cred = fopen.read()
fopen.close()

print("The Clear Input is:")
print(cred)

f = Fernet(key)
token = f.encrypt(cred)

print("The Encrypted Output is:")
print(token)

with open("credentials.bin", "wb") as output_file:
    output_file.write(token)
