from cryptography.fernet import Fernet # lib to decrypt Postgresql credentials from binary file
import psycopg2 # Postgresql connector library

# Try retrieving the Fernet encryption key from bin file
try:
    loginFRetrieve = open("config/key.bin", "rb")
    retrieved_key = loginFRetrieve.read()
    loginFRetrieve.close()
except:
    print("Error retrieving key.")
    
# Try retrieving the Postgresql credentials from bin file
try:
    loginFRetrieve = open("config/credentials.bin", "rb")
    retrieved_cred = loginFRetrieve.read()
    loginFRetrieve.close()
except:
    print("Error retrieving credentials.")

# Decrypt the retrieved Postgresql creds and split into list
cipher = Fernet(retrieved_key)
credential = cipher.decrypt(retrieved_cred)
credential = credential.decode('utf-8')
split_creds = credential.split(":")


# Try connecting to Postgresql DB with decrypted credentials
def establish_connection(db_name:str):
    '''
    Tries to establish a connection to the specified database.
    Returns the connection object if successful.
    '''
    try:
        conn = psycopg2.connect(host=split_creds[0],dbname=db_name,user=split_creds[2],password=split_creds[3])
    except:
        print("Postgresql connection failed.")
    else:
        return conn