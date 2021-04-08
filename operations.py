import dbconnection as dbc
import notification
import admin_operations as adops

def search_for_source(attribute:str, value:str) -> list:
    '''
    Function to query a specific search on the sources table. Two arguments are being passed: attribute and value.
    The attribute indicates the column to search for (e.g. by ID or by Name).
    The value indicates the value to search for within the column.
    
    Example: search_for_source('name', 'Google') -> would search for 'Google' in the 'name' column
    Note that if the attribute is 'id', the value has to be transformed from string to integer prior to searching.
    
    The return value should contain all the results from the query (i.e. the 'fetchall()' result)
    
    pass
    '''
    
    cursor = dbc.establish_connection('data').cursor()
    
    sql = "";
    val = "";
    if (attribute == "id" or attribute == "threat_level"):
        sql = "SELECT * FROM sources WHERE " + attribute + " = %(value)s", 
        val = {'value': int(value)}
    elif (attribute == "name" or attribute == "url" or attribute == "description"):
        sql = "SELECT * FROM sources WHERE " + attribute + " like %(value)s"
        val = {'value': '%'+ value +'%'}

    cursor.execute(sql, val)
    result = cursor.fetchall()
    output = []
    for item in result:
        output.append((item[0], item[1], item[2], item[3], item[4], item[5], item[6],))
    return output


def create_new_source(name:str, url:str, threat_level:int, description:str) -> bool:
    '''
    Function to create a new entry in the sources database table. Takes as input the name of the source, the url, the threat level and the description.
    Returns a bool value depending on whether the creation was successful. I.e. should return 'True' if successful and 'False' if not.
    
    If successful, should trigger an email notification to be sent out to all users with role=3 (External Authority)
   
    pass
    '''
    
    cursor = dbc.establish_connection('data').cursor()
    
    sql = """
          INSERT INTO sources (name, url, threat_level, description, creation_date, modified_date)
          VALUES (%(name)s,%(url)s,%(threat_level)s,%(description)s,%(creation_date)s,%(modified_date)s);
          """
    val = {'name':name, 'url':url, 'threat_level':threat_level, 'description':description, 'creation_date':datetime.now(), 'modified_date':datetime.now()}
    try:    
        cursor.execute(sql, val)
        sourceId = cursor.fetchone()[0]
        conn.commit()
    except:
        'Trigger Notification?'
        return False
    else:
        return True

def modify_source(source_id:int, attribute:str, new_value:str) -> bool:
    '''
    Function to modify the information of an existing source. Takes as input the id of the source that is being modified, the attribute to be modified
    and the new value that should be saved.
    
    Example: modify_source(1, 'name', 'Google') -> Would change the 'name' of the source with id=1 to 'Google'
    
    Returns a bool value depending on whether the modification was successful. I.e. should return 'True' if successful and 'False' if not.
    
    pass
    '''
    cursor = dbc.establish_connection('data').cursor()
    
    if attribute == 'threat_level':
        new_value = int(new_value) # change new value to int type if the Threat Level is being changed
        
    sql = "UPDATE sources SET " + attribute + " = %(val)s WHERE id = %(id)s;"
    val = {'val':new_value, 'id': source_id}
    try:
        cursor.execute(sql,val)
        conn.commit()
    except:
        return False
    return True

def change_password(user_id:int, new_password:str) -> bool:
    '''
    Function to change the password of a specific user. Takes the user id and new password as input.
    Returns a bool value depending on whether the modification was successful. I.e. should return 'True' if successful and 'False' if not.
    
    Also should trigger an email notification if the password has been changed successfully.
    
    pass
    '''
    cursor = dbc.establish_connection('authentication').cursor()
        
    sql = "UPDATE users SET password = %(val)s WHERE id = %(id)s;"
    val = {'val':new_password, 'id': user_id}
    try:
        cursor.execute(sql,val)
        conn.commit()
    except:
        'Trigger Notification?'
        return False
    else:
        return True
    