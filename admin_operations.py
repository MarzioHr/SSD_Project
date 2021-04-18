"""Module to execute user operations for Administrator Role."""

import secrets
import string
from argon2 import PasswordHasher
import psycopg2
from psycopg2 import sql
import dbconnection as dbc
import eventlog as log
import notification

RED = '\033[91m' # Erorr Messages
GREEN = '\033[92m' # Success Messages
YELLOW = '\033[93m' # Notices to User

def register_new_user(first_name:str,last_name:str,dob:str,email:str,role:int,admin_id:int) -> bool: #pylint: disable=too-many-arguments, disable=too-many-locals
    '''
    Function to sign up a new user. Takes user information as arg to sign up accordingly.
    Takes Admin's id as argument to create log in the eventlog database.
    If sign-up is successful, triggers notification email.
    '''
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor() # Connect Cursor to Authentication DB
    username = generate_username(first_name, last_name)
    password = generate_password(12)
    clear_pswd = password[0]
    hash_pswd = password[1]
    psql = """
          INSERT INTO users 
          (first_name, last_name, dob, user_role, username, password, status, email)
          VALUES (%(first_name)s,%(last_name)s,%(dob)s,%(role)s,%(uname)s,%(pw)s,%(stat)s,%(email)s)
          RETURNING id
          """
    val = {
        'first_name':first_name,
        'last_name':last_name,
        'dob':dob,
        'role':role,
        'uname':username,
        'pw':hash_pswd,
        'stat':1,
        'email':email
        }
    try:
        cursor.execute(psql, val)
        conn.commit()
    except psycopg2.OperationalError as error:
        print(RED + 'Issue with registering new user on database. Error:', error)
        print(YELLOW + 'Error TYPE:', type(error))
        return False
    except psycopg2.errors.DatetimeFieldOverflow: #pylint: disable=no-member
        print(RED + 'Issue with the given Date of Birth. Please check your input and try again.')
        return False
    else:
        created_user_id = cursor.fetchone()[0]
        log.admin_log('Create User', admin_id, created_user_id) # logging event in logs
        print(GREEN + f'User successfully created. Sending Registration email to {email}...')
    sent_email = notification.registration_email(first_name, email, username, clear_pswd)
    if sent_email:
        print(GREEN + 'Email sent successfully!')
    else:
        print(RED + 'Email could not be sent. Please ensure that the SMTP is reachable.')
    return True


def modify_user(uid:int, attribute:str, new_value:str, admin_id:int) -> bool:
    '''
    Function to modify an existing user. Takes the user id as input to execute upon.
    The attribute sets the field to be modified, the new_value denotes the value after modification.
    '''
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor() # Connect Cursor to Authentication DB

    stmt = sql.SQL("SELECT {attribute} FROM users WHERE id = {uid}").format(
            attribute = sql.Identifier(attribute),
            uid = sql.Literal(uid),
    )
    cursor.execute(stmt)

    curr_val = cursor.fetchall()[0][0]
    if attribute == 'user_role':
        new_value = int(new_value) # change new value to int type if the user role is being changed

    stmt = sql.SQL("UPDATE users SET {attribute} = {value} WHERE id = {uid}").format(
            attribute = sql.Identifier(attribute),
            uid = sql.Literal(uid),
            value = sql.Literal(new_value),
    )

    try:
        cursor.execute(stmt)
        conn.commit()
    except psycopg2.OperationalError as error:
        print(RED + 'Issue with modifying user on database. Error:', error)
        print(YELLOW + 'Error TYPE:', type(error))
        return False
    except psycopg2.errors.DatetimeFieldOverflow: #pylint: disable=no-member
        print(RED + 'Issue with the given Date of Birth. Please check your input and try again.')
        return False
    log.admin_log(
        'Edit User',
        admin_id,
        uid,
        modified=attribute,
        old_val=str(curr_val),
        new_val=str(new_value)
        ) # log Edit User event
    return True


def unlock_user(uid:int, admin_id:int) -> bool:
    '''
    Function to unlock an already locked user. Input: admin's id and the id of the user to unlock.
    If unlock was successful, will return bool 'True'. If there was an error, returns bool 'False'.
    '''
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor() # Connect Cursor to Authentication DB
    psql = "UPDATE users SET status=1 WHERE id=%(uid)s"
    val = {'uid':uid}
    try:
        cursor.execute(psql,val)
        conn.commit()
    except psycopg2.OperationalError as error:
        print(RED + 'Issue with unlocking user on database. Error:', error)
        print(YELLOW + 'Error TYPE:', type(error))
        return False
    log.admin_log('Unlock User', admin_id, uid, modified='status', old_val='3', new_val='1')
    return True


def lock_user(uid:int) -> bool:
    '''
    Function to lock a user if there are more than three failed login attempts. Input: User's ID.
    If lock was successful, will return bool 'True'. If there unsuccessful, returns bool 'False'.
    '''
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor() # Connect Cursor to Authentication DB
    psql = "UPDATE users SET status=3 WHERE id=%(uid)s;"
    val = {'uid':uid}
    try:
        cursor.execute(psql,val)
        conn.commit()
    except psycopg2.OperationalError as error:
        print(RED + 'Issue with locking user on database. Error:', error)
        print(YELLOW + 'Error TYPE:', type(error))
        return False
    log.auth_log("Account Locked", uid) # log locked account event
    return True


def deactivate_user(uid:int, admin_id:int, curr_status:int) -> bool:
    '''
    Function to deactivate a user if the access is no longer needed. Input: User's ID.
    If deactivation was successful, will return bool 'True'. If not, returns bool 'False'.
    '''
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor() # Connect Cursor to Authentication DB
    psql = "UPDATE users SET status=2 WHERE id=%(uid)s;"
    val = {'uid':uid}
    try:
        cursor.execute(psql,val)
        conn.commit()
    except psycopg2.OperationalError as error:
        print(RED + 'Issue with deactivating user on database. Error:', error)
        print(YELLOW + 'Error TYPE:', type(error))
        return False
    log.admin_log(
        'Deactivate User',
        admin_id, uid,
        modified='status',
        old_val=str(curr_status),
        new_val='2'
        ) # log deactivation event
    return True


def fetch_user_info(uid=None, email=None, username=None) -> tuple: #pylint: disable=too-many-return-statements
    '''
    Queries user information based on the given email, username or uid.
    Returns a tuple of user id, first name, last name, email, dob and status if user was found.
    Returns None if user was not found.
    '''
    cursor = dbc.establish_connection('authentication').cursor() # Connect Cursor to Auth DB
    if uid is not None:
        psql = "SELECT * FROM users WHERE id=%(val)s"
        val = {'val':uid}
        try:
            cursor.execute(psql,val)
            result = cursor.fetchall()[0]
        except IndexError:
            return None
        return (result[0], result[1], result[2], result[9], result[3], result[8])
    if email is not None:
        psql = "SELECT * FROM users WHERE email=%(val)s"
        val = {'val':email}
        try:
            cursor.execute(psql,val)
            result = cursor.fetchall()[0]
        except IndexError:
            return None
        return (result[0], result[1], result[2], result[9], result[3], result[8])
    if username is not None:
        psql = "SELECT * FROM users WHERE username=%(val)s"
        val = {'val':username}
        try:
            cursor.execute(psql,val)
            result = cursor.fetchall()[0]
        except IndexError:
            return None
        return (result[0], result[1], result[2], result[9], result[3], result[8])
    return None


def fetch_all_authorities() -> list:
    '''
    Query to fetch all users in the system with the 'Authority' role.
    Returns a list of tuples containing pairs of emails and first_names
    to be used by the source notification email.
    '''
    cursor = dbc.establish_connection('authentication').cursor() # Connect Cursor to Auth DB
    psql = "SELECT * FROM users WHERE user_role=3"
    cursor.execute(psql)
    result = cursor.fetchall()
    output = []
    for item in result:
        output.append((item[9], item[1]))
    return output


def generate_password(length:int) -> tuple:
    '''
    Function to generate a random, secure password with the given length.
    Returns the clear password, as well as the argon2 hash of the password.
    '''
    password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation)
                        for i in range(length)))
    a2_ph = PasswordHasher() # set password hasher for Argon2
    hashed = a2_ph.hash(password)
    return (password, hashed)


def generate_username(first_name, last_name) -> str:
    '''
    Function to return a valid username for the given first and last name.
    If combination is taken already, will add a running number to the end of the username.
    '''
    user_comb = first_name[0] + '.' + last_name
    user_comb = user_comb.lower()
    if not username_exists(user_comb):
        return user_comb
    running_number = 1
    while True:
        if not username_exists(user_comb+str(running_number)):
            return user_comb+str(running_number)
        running_number += 1


def username_exists(username:str) -> bool:
    '''
    Checks the users database if a given username exists in the DB already.
    If not, returns bool 'False', if it exists returns bool 'True'.
    '''
    cursor = dbc.establish_connection('authentication').cursor() # Connect Cursor to Auth DB
    psql = "SELECT count(*) FROM users WHERE username=%(val)s"
    val = {'val':username}
    cursor.execute(psql,val)
    result = cursor.fetchone()[0]
    if result == 0:
        return False
    return True
