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
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor() # Connect Cursor to Authentication DB
    username = generate_username(first_name, last_name)
    password = generate_password(12)
    clear_pswd = password[0]
    hash_pswd = password[1]
    
    sql = """
          INSERT INTO users (first_name, last_name, dob, user_role, username, password, status, email)
          VALUES (%(first_name)s,%(last_name)s,%(dob)s,%(role)s,%(username)s,%(password)s,%(status)s,%(email)s);
          """
    val = {'first_name':first_name, 'last_name':last_name, 'dob':dob, 'role':role, 'username':username, 'password':hash_pswd, 'status':1, 'email':email}
    try:    
        cursor.execute(sql, val)
        conn.commit()
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
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor() # Connect Cursor to Authentication DB
    
    if attribute == 'user_role':
        new_value = int(new_value) # change new value to int type if the user role is being changed
        
    sql = "UPDATE users SET " + attribute + " = %(val)s WHERE id = %(uid)s;"
    val = {'val':new_value, 'uid': uid}
    try:
        cursor.execute(sql,val)
        conn.commit()
    except:
        return False
    return True
    

def unlock_user(uid:int) -> bool:
    '''
    Function to unlock an already locked user. Takes as input the user's id.
    If unlock was successful, will return bool 'True'. If there was an error, returns bool 'False'.
    '''
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor() # Connect Cursor to Authentication DB
    sql = "UPDATE users SET status=1 WHERE id=%(uid)s;"
    val = {'uid':uid}
    try:
        cursor.execute(sql,val)
        conn.commit()
    except:
        return False
    return True


def lock_user(uid:int) -> bool:
    '''
    Function to lock a user if there are more than three failed login atttempts. Takes as input the user's id.
    If lock was successful, will return bool 'True'. If there was an error, returns bool 'False'.
    '''
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor() # Connect Cursor to Authentication DB
    sql = "UPDATE users SET status=3 WHERE id=%(uid)s;"
    val = {'uid':uid}
    try:
        cursor.execute(sql,val)
        conn.commit()
    except:
        return False
    return True


def deactivate_user(uid:int) -> bool:
    '''
    Function to deactivate (soft-delete) a user if the access is no longer needed. Takes as input the user's id.
    If deactivation was successful, will return bool 'True'. If there was an error, returns bool 'False'.
    '''
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor() # Connect Cursor to Authentication DB
    sql = "UPDATE users SET status=2 WHERE id=%(uid)s;"
    val = {'uid':uid}
    try:
        cursor.execute(sql,val)
        conn.commit()
    except:
        return False
    return True


def fetch_user_info(uid=None, email=None, username=None) -> tuple:
    '''
    Queries user information based on the given email, username or uid.
    Returns a tuple of user id, first name, last name, email, dob and status if user was found.
    Returns None if user was not found.
    '''
    cursor = dbc.establish_connection('authentication').cursor() # Connect Cursor to Authentication DB
    
    if uid != None:
        sql = "SELECT * FROM users WHERE id=%(val)s"
        val = {'val':uid}
        try:
            cursor.execute(sql,val)
            result = cursor.fetchall()[0]
        except:
            return None
        return (result[0], result[1], result[2], result[9], result[3], result[8])
        
    if email != None:
        sql = "SELECT * FROM users WHERE email=%(val)s"
        val = {'val':email}
        try:
            cursor.execute(sql,val)
            result = cursor.fetchall()[0]
        except:
            return None
        return (result[0], result[1], result[2], result[9], result[3], result[8])
    
    if username != None:
        sql = "SELECT * FROM users WHERE username=%(val)s"
        val = {'val':username}
        try:
            cursor.execute(sql,val)
            result = cursor.fetchall()[0]
        except:
            return None
        return (result[0], result[1], result[2], result[9], result[3], result[8])


def fetch_all_authorities() -> list:
    '''
    Query to fetch all users in the system with the 'Authority' role.
    Returns a list of tuples containing pairs of emails and first_names to be used by the source notification email.
    '''
    cursor = dbc.establish_connection('authentication').cursor() # Connect Cursor to Authentication DB
    sql = "SELECT * FROM users WHERE user_role=3"
    cursor.execute(sql)
    result = cursor.fetchall()
    output = []
    for item in result:
        output.append((item[9], item[1]))
    return output


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
# print(fetch_user_info(email='kalina.mhn@gmail.com'))
# print(username_exists('k.mohonee'))
# print(generate_username('Marzio', 'Hruschka'))
# print(generate_password(12))
# print(register_new_user('Hannah', 'Monroe', '1989-12-15', 'marziohruschka+hannahmonroe@gmail.com', 3))
# print(fetch_user_info('marziohruschka+johndoe@gmail.com'))
# print(fetch_all_authorities())
# print(unlock_user(3))
# print(lock_user(1))
# print(modify_user(4, 'user_role', '3'))