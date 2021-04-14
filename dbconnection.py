"""This module establishes a connection to the PostgreSQL DB."""

from cryptography.fernet import Fernet # lib to decrypt Postgresql credentials from binary file
import psycopg2 # Postgresql connector library

RED = '\033[91m' # Erorr Messages
YELLOW = '\033[93m' # Notices to User

def retrieve_key():
    '''Function to retrieve the Fernet Encryption Key from the config folder.'''
    # Try retrieving the Fernet encryption key from bin file
    try:
        key_file = open("config/key.bin", "rb")
        retrieved_key = key_file.read()
        key_file.close()
    except OSError:
        print(RED + "Error retrieving key.")
        return None
    return retrieved_key

# Try retrieving the Postgresql credentials from bin file
try:
    loginFRetrieve = open("config/credentials.bin", "rb")
    retrieved_cred = loginFRetrieve.read()
    loginFRetrieve.close()
except OSError:
    print(RED + "Error retrieving credentials.")

# Decrypt the retrieved Postgresql creds and split into list
cipher = Fernet(retrieve_key())
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
        conn = psycopg2.connect(
            host=split_creds[0],
            dbname=db_name,
            user=split_creds[2],
            password=split_creds[3]
        )
    except psycopg2.OperationalError as error:
        print(RED + "Error:", error)
        print(YELLOW + "Exception TYPE:", type(error))
        return None
    else:
        return conn
