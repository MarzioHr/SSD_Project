"""Module to execute user operations for Specialist and Authority Role."""

from datetime import datetime
import psycopg2
from psycopg2 import sql
import dbconnection as dbc
import eventlog as log
import notification
import admin_operations as adops


def search_for_source(attribute:str, value:str) -> list:
    '''
    Function to query a specific search on the sources table.
    Two arguments are being passed: attribute and value.
    The attribute indicates the column to search for (e.g. by ID or by Name).
    The value indicates the value to search for within the column.
    Example: search_for_source('name', 'Google') -> would search for 'Google' in the 'name' column
    The return value contains all results from the query (i.e. the 'fetchall()' result)
    '''
    cursor = dbc.establish_connection('data').cursor()
    if attribute == "threat_level":
        value = int(value)
        stmt=sql.SQL(
        "SELECT id, name FROM sources WHERE {attribute} = {value} order by id"
        ).format(
            attribute = sql.Identifier(attribute.lower()),
            value = sql.Literal(value),
        )
    else:
        value = value.lower()
        value = '%'+value+'%'
        stmt=sql.SQL(
        "SELECT id, name FROM sources WHERE lower({attribute}) like {value} order by id"
        ).format(
            attribute = sql.Identifier(attribute.lower()),
            value = sql.Literal(value),
        )

    cursor.execute(stmt)
    result = cursor.fetchall()
    output = []
    for item in result:
        output.append((item[0], item[1]))
    return output

def get_source_by_id(source_id:int) -> list:
    '''
    Function to return source information by its id.
    Used in the search operation of the interface module.
    Takes as argument the source id and returns a tuple:
    (id, name, url, threat level, description, creation date, modified date)
    '''
    cursor = dbc.establish_connection('data').cursor()
    psql = """
          SELECT id, name, url, threat_level, description, creation_date, modified_date 
          FROM sources WHERE id = %(value)s
          """
    val = {'value': source_id}
    try:
        cursor.execute(psql, val)
        result = cursor.fetchall()[0]
    except IndexError:
        return None
    return (result[0], result[1], result[2], result[3], result[4], result[5], result[6])


def create_new_source(name:str, url:str, threat_level:int, description:str, uid:int) -> bool:
    '''
    Function to create a new entry in the sources database table.
    Takes as input the name of the source, the url, the threat level and the description.
    Returns bool True/False depending on whether the creation was successful.
    If successful, triggers email notification to all users with role=3 (External Authority).
    '''
    conn = dbc.establish_connection('data')
    cursor = conn.cursor()
    psql = """
          INSERT INTO sources (name, url, threat_level, description, creation_date, modified_date)
          VALUES (%(name)s,%(url)s,%(threat_level)s,%(description)s,%(creation_date)s,%(modified_date)s) 
          RETURNING id;
          """
    val = {
        'name':name,
        'url':url,
        'threat_level':threat_level,
        'description':description,
        'creation_date':datetime.now(),
        'modified_date':datetime.now()
        }
    try:
        cursor.execute(psql, val)
        conn.commit()
    except psycopg2.OperationalError:
        return False
    else:
        recipients = adops.fetch_all_authorities() # fetching list of authority users
        source_id = cursor.fetchone()[0] # retrieving the id of the newly created source
        log.operation_log("Create Source", uid, source_id) # log source creation event
        notification.new_source_email(recipients, source_id, name, url, threat_level) # notification
        return True


def modify_source(source_id:int, attribute:str, new_value:str, uid:int) -> bool:
    '''
    Function to modify the information of an existing source.
    Takes as input the id of the source that is being modified, the attribute to be modified
    and the new value that should be saved.
    Example: modify_source(1, 'name', 'Google') -> Changes the 'name' of the source id=1 to 'Google'
    Returns bool True/False depending on whether the modification was successful.
    '''
    conn = dbc.establish_connection('data')
    cursor = conn.cursor()

    stmt = sql.SQL("SELECT {attribute} FROM sources WHERE id = {sid}").format(
            attribute = sql.Identifier(attribute),
            sid = sql.Literal(source_id),
    )
    cursor.execute(stmt)
    curr_val = cursor.fetchall()[0][0]

    if attribute == 'threat_level':
        new_value = int(new_value) # change new value to int type if Threat Level is being changed

    stmt = sql.SQL(
        "UPDATE sources SET {attribute}={value}, modified_date={dtnow} WHERE id = {sid}"
    ).format(
            attribute = sql.Identifier(attribute),
            sid = sql.Literal(source_id),
            value = sql.Literal(new_value),
            dtnow = sql.Literal(datetime.now()),
    )
    try:
        cursor.execute(stmt)
        conn.commit()
    except psycopg2.OperationalError:
        return False
    log.operation_log(
        "Edit Source",
        uid,
        source_id,
        modified=attribute,
        old_val=str(curr_val),
        new_val=str(new_value)
        ) # log edit source event
    return True


def change_password(user_id:int, new_password:str) -> bool:
    '''
    Function to change the password of a specific user. Input: user id and new password hash.
    Returns a bool value depending on whether the modification was successful.
    If successful, triggers email notification to user that password has changed.
    '''
    conn = dbc.establish_connection('authentication')
    cursor = conn.cursor()
    psql = "UPDATE users SET password = %(val)s WHERE id = %(id)s;"
    val = {'val':new_password, 'id': user_id}
    try:
        cursor.execute(psql,val)
        conn.commit()
    except psycopg2.OperationalError:
        return False
    log.auth_log("Password Change", user_id)
    fetch_user = adops.fetch_user_info(uid=user_id) # retrieves user's information
    u_email = fetch_user[3]
    u_first_name = fetch_user[1]
    notification.changed_password_email(u_first_name, u_email) # triggers email notification
    return True
