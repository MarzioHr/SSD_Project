import dbconnection as dbc
from argon2 import PasswordHasher  # Argon2 lib to hash password
from datetime import datetime

# set Argon2 password hasher object
ph = PasswordHasher()

def hash_pswd(password:str) -> str:
    """
    Uses Argon2 to hash password and returns hash as string.
    Takes clear text password string as input.
    """
    hash = ph.hash(password)
    return hash


def existing_user(user:str, password:str) -> tuple:
    '''
    Function to authenticate existing user against the database.
    Takes username and clear password as input.
  
    If successful, returns authenticated user as tuple: (user id, first name, user role).
    If username not found or user is locked or deactivated, returns None.
    If password was incorrect, returns False.
    '''
    cursor = dbc.establish_connection('authentication').cursor()
    
    sql = 'SELECT id, first_name, user_role, password, status FROM users WHERE username = %(val)s'
    val = {'val':user}
    
    try:
        cursor.execute(sql,val)
        result = cursor.fetchall()[0]
    except:
        return None
    user_status = result[4]
    if user_status in (2,3):
        print('This user is either deactivated or currently locked. Please contact the system administrator team for further information.\n')
        quit()
    
    try:
        match = ph.verify(result[3], password)
    except:
        return False
    if match:
        return (result[0], result[1], result[2])


### Test Cases ###
# print(existing_user('m.hruschka','f?>+"]3Hp_RP'))
# print(ph.verify(hash_pswd('f?>+"]3Hp_RP'), 'f?>+"]3Hp_RP'))