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
    if user_status==2:
        log.auth_log("Failed Login: Deactivated User", result[0])
        print('This user is deactivated. Please contact the system administrator team for further information.\n')
        quit()
    elif user_status==3:
        log.auth_log("Failed Login: Locked User", result[0])
        print('This user is currently locked. Please contact the system administrator team for further information.\n')
        quit()
    
    try:
        match = ph.verify(result[3], password)
    except:
        return False
    if match:
        return (result[0], result[1], result[2])

    
def update_last_login(uid:int) -> bool:
    '''
    Function to update a user's last login value with the current datetime stamp.
    Returns True if successful and False if not.
    '''
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor()
    now = datetime.now()
    
    sql = 'UPDATE users SET last_login = %(now)s WHERE id = %(uid)s'
    val = {'now':now, 'uid':uid}
    
    try:
        cursor.execute(sql,val)
        conn.commit()
    except:
        return False
    return True


def fetch_last_login(uid:int) -> str:
    '''
    Function to fetch a user's last login date.
    Returns date string if existent or None if empty. 
    '''
    cursor = dbc.establish_connection('authentication').cursor()
    
    sql = 'SELECT last_login FROM users WHERE id=%(uid)s'
    val = {'uid':uid}
    
    try:
        cursor.execute(sql,val)
        result = cursor.fetchall()[0][0]
    except:
        return None
    return result
    
    
### Test Cases ###
# print(existing_user('m.hruschka','f?>+"]3Hp_RP'))
# print(ph.verify(hash_pswd('f?>+"]3Hp_RP'), 'f?>+"]3Hp_RP'))
# print(fetch_last_login(3))
# print(update_last_login(3))