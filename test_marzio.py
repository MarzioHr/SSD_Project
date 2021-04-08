from cryptography.fernet import Fernet

PAYLOAD = b'7&53$QdvV53j$3zC'

try:
  loginFRetrieve = open("config/key.bin", "rb")
  retrieved_key = loginFRetrieve.read()
  loginFRetrieve.close()
except:
  print("Error retrieving key.")

print("The Clear Input is:")
print(PAYLOAD)

f = Fernet(retrieved_key)
token = f.encrypt(PAYLOAD)

print("The Encrypted Output is:")
print(token)