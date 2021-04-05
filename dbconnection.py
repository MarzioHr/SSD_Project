from cryptography.fernet import Fernet # lib to decrypt Postgresql credentials from binary file
import psycopg2 # Postgresql connector library

# Try retrieving the Fernet encryption key from bin file
try:
  loginFRetrieve = open("config/key.bin", "rb")
  retrievedKey = loginFRetrieve.read()
  loginFRetrieve.close()
except:
  print("Error retrieving key.")
  
# Try retrieving the Postgresql credentials from bin file
try:
  loginFRetrieve = open("config/credentials.bin", "rb")
  retrievedCred = loginFRetrieve.read()
  loginFRetrieve.close()
except:
  print("Error retrieving credentials.")
  
# Decrypt the retrieved Postgresql creds and split into list
cipher = Fernet(retrievedKey)
credential = cipher.decrypt(retrievedCred)
credential = credential.decode('utf-8')
splitCreds = credential.split(":")

# Try connecting to Postgresql DB with decrypted credentials
try:
  conn = psycopg2.connect(host=splitCreds[0],dbname=splitCreds[1],user=splitCreds[2],password=splitCreds[3])

except:
  print("Postgresql connection failed.")
#Test