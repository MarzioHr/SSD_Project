import dbconnection as dbc
import notification
import secrets
import string
from argon2 import PasswordHasher

def register_new_user(first_name:str, last_name:str, dob:str, email:str, role:int) -> bool:
    '''
    Function to sign up a new user. Takes user information as arg to sign up accordingly.
    If sign-up is successful, triggers notification email.
    '''
    cursor = dbc.establish_connection('authentication').cursor() # Connect Cursor to Authentication DB
    username = generate_username(first_name, last_name)
    password = generate_password(12)
    clear_pswd = password[0]
    hash_pswd = password[1]
    
    sql = '''
          INSERT INTO users (first_name, last_name, dob, user_role, username, password, status, email)
          VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
          '''
    val = (first_name, last_name, dob, role, username, hash_pswd, 1, email)
    #val = {'first_name':first_name, 'last_name':last_name, 'dob':dob, 'role':role, 'username':username, 'password':hash_pswd, 'email':email}
    print(sql, val)
    cursor.execute(sql,val)
    try:    
        pass
    except:
        print('Issue with registering new user on database. Please check the db connection and ensure that it is working as expected.')
        return False
    else:
        print(f'User successfully created. Sending Registration email to {email}...')
    
    # eventlog TODO
    sent_email = notification.registration_email(first_name, email, username, clear_pswd)
    if sent_email:
        print('Email sent successfully!')
    else:
        print('Email could not be sent. Please ensure that the SMTP is reachable.')
    return True
    
    
def modify_user(uid:int, attribute:str, new_value:str) -> bool:
    '''
    Function to modify an existing user. Takes the user id as input to execute upon.
    The attribute denotes the datafield to be modified, the new_value denotes the new value after the modification.
    '''
    pass  


def unlock_user(uid:int) -> bool:
    '''
    Function to unlock an already locked user. Takes as input the user's id.
    If unlock was successful, will return bool 'True'. If there was an error, returns bool 'False'.
    '''
    pass


def fetch_user_info(email:str) -> tuple:
    '''
    Queries user information based on the given email.
    Returns a tuple of user id, first name, last name, email and status.
    '''
    cursor = dbc.establish_connection('authentication').cursor() # Connect Cursor to Authentication DB
    sql = "SELECT * FROM users WHERE email=%(val)s"
    val = {'val':email}
    cursor.execute(sql,val)
    result = cursor.fetchall()[0]
    #print(result)
    return (result[0], result[1], result[2], result[9], result[8])


def fetch_all_authorities() -> list:
    '''
    Query to fetch all users in the system with the 'Authority' role.
    Returns a list of tuples containing pairs of emails and first_names to be used by the source notification email.
    '''
    cursor = dbc.establish_connection('authentication').cursor() # Connect Cursor to Authentication DB
    sql = "SELECT * FROM users WHERE role=3"
    cursor.execute(sql)
    # filter results and pass list with tuples TODO
    pass


def generate_password(length:int) -> tuple:
    '''
    Function to generate a random, secure password with the given length. Returns the clear password, as well as the argon2 hash of the password.
    '''
    password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(length)))
    ph = PasswordHasher() # set password hasher for Argon2
    hash = ph.hash(password)
    return (password, hash)


def generate_username(first_name, last_name) -> str:
    '''
    Function to return a valid username for the given first and last name. If combination is taken already, will add a running number to the end of
    the username.
    '''
    user_comb = first_name[0] + '.' + last_name
    user_comb = user_comb.lower()
    if not username_exists(user_comb):
        return user_comb
    else:
        running_number = 1
        while True:
            if not username_exists(user_comb+str(running_number)):
                return user_comb+str(running_number)
            else:
                running_number += 1
    
    
def username_exists(username:str) -> bool:
    '''
    Checks the users database if a given username exists in the DB already.
    If not, returns bool 'False', if it exists returns bool 'True'.
    '''
    cursor = dbc.establish_connection('authentication').cursor() # Connect Cursor to Authentication DB
    sql = "SELECT count(*) FROM users WHERE username=%(val)s"
    val = {'val':username}
    cursor.execute(sql,val)
    result = cursor.fetchone()[0]
    if result == 0:
        return False
    else:
        return True

    
### Testcases ###
# print(fetch_user_info('marziohruschka@gmail.com'))
# print(username_exists('m.hruschka'))
# print(generate_username('Marzio', 'Hruschka'))
print(generate_password(12))
#print(register_new_user('Johnathana', 'Doee', '1980-01-21', 'marziohruschka+johndoee@gmail.com', 3))
#print(fetch_user_info('marziohruschka+johndoee@gmail.com'))