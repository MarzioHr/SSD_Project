"""Module to handle the logging of events on the system."""

from datetime import datetime # python lib to query date and time
import psycopg2
import dbconnection as dbc

def auth_log(log_type:str, uid:int) -> bool:
    '''
    Function to create an authentication event log entry in the database.
    Takes as input the user_id that actioned the event, as well as the operation type of the log.
    Type can be: Successful Login, Password Change, Account Locked, Locked Account Login Attempt.
    Returns True if log was created successfully and false if not.
    '''
    conn = dbc.establish_connection('eventlog')
    cursor = conn.cursor() # Connect Cursor to Eventlog DB
    dt_now = datetime.now()
    datestamp = dt_now.strftime("%d/%m/%Y %H:%M:%S") # captures datetime when the function is called
    sql = """
          INSERT INTO authlogs(datetime, operation, user_id) 
          VALUES (%(datetime)s,%(operation)s,%(uid)s)
          """
    val = {'datetime':datestamp,'operation':log_type, 'uid':uid}
    try:
        cursor.execute(sql,val)
        conn.commit()
    except psycopg2.OperationalError:
        return False
    return True


def operation_log( #pylint: disable=too-many-arguments
    log_type:str, uid:int, source_id:int, modified=None, old_val=None, new_val=None
) -> bool:
    '''
    Function to create an operations event log entry in the database.
    Input: user_id that actioned the event, the operation type of the log, the id of the source,
    the modified attribute and the before and after value of the attribute.
    The operation type can be: View Source, Edit Source and Create Source.
    Returns True if log was created successfully and false if not.
    '''
    conn = dbc.establish_connection('eventlog')
    cursor = conn.cursor() # Connect Cursor to Eventlog DB
    dt_now = datetime.now()
    datestamp = dt_now.strftime("%d/%m/%Y %H:%M:%S") # captures datetime when function is called

    sql = """
          INSERT INTO operationlogs
          (datetime, operation, user_id, source_id, modified_attribute, old_value, new_value)
          VALUES(%(datetime)s,%(operation)s,%(uid)s,%(sid)s,%(attr)s,%(old)s,%(new)s)
          """
    val = {
        'datetime':datestamp,
        'operation':log_type,
        'uid':uid, 'sid':source_id,
        'attr':modified,'old':old_val,
        'new':new_val
        }
    try:
        cursor.execute(sql,val)
        conn.commit()
    except psycopg2.OperationalError:
        return False
    return True


def admin_log( #pylint: disable=too-many-arguments
    log_type:str, admin_id:int, user_id:int, modified=None, old_val=None, new_val=None
) -> bool:
    '''
    Function to create an admin event log entry in the database.
    Input: admin's id that actioned the event, the type of operation, the effected user id,
    the modified attribute and the before and after value of the attribute.
    The operation type can be: Create User, Unlock User, Deactivate User and Edit User.
    Returns True if log was created successfully and false if not.
    '''
    conn = dbc.establish_connection('eventlog')
    cursor = conn.cursor() # Connect Cursor to Eventlog DB
    dt_now = datetime.now()
    datestamp = dt_now.strftime("%d/%m/%Y %H:%M:%S") # captures datetime when function is called
    sql = """
          INSERT INTO adminlogs
          (datetime, operation, admin_id, user_id, modified_attribute, old_value, new_value)
          VALUES(%(datetime)s,%(operation)s,%(adid)s,%(uid)s,%(attr)s,%(old)s,%(new)s)
          """
    val = {
        'datetime':datestamp,
        'operation':log_type,
        'adid':admin_id,
        'uid':user_id,
        'attr':modified,
        'old':old_val,
        'new':new_val
        }
    try:
        cursor.execute(sql,val)
        conn.commit()
    except psycopg2.OperationalError:
        return False
    return True
