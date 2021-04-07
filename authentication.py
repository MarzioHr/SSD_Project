import dbconnection
from argon2 import PasswordHasher  # Argon2 lib to hash password
from datetime import datetime
  
# set DB cursor
mycursor = dbconnection.conn.cursor()

# set Argon2 password hasher object
ph = PasswordHasher()

def hashPswd(password:str) -> str:
    """
    Uses Argon2 to hash password and returns hash as string.
    Takes clear text password string as input.
    """
    hash = ph.hash(password)
    return hash

def userExists(user:str) -> bool:
    """
    Function to check if a username already exists in the database.
    Returns True if username exists.
    Returns False if username does not exist.
    """
    mycursor.execute("SELECT username FROM users WHERE username = %(username)s", {'username': user})
    userResult = mycursor.fetchall()
    if userResult:
        return True
    return False

def newUser(user:str, password:str, email:str,  firstName:str, lastName:str, dateOfBirth:datetime, userRole:str, status:int) -> bool:
    """
    Function to signup new user with given info in the system.
    The passed password is passed through the hash function prior to being saved in the database.
    Returns True if signup was successful and False if not.
  
    Includes validation on entered password strength. Password must inlude both letters and numbers, as well as be atleast 8 characters long.
    """
    if userExists(user) == False:
        if (any(map(str.isdigit, password))==True) and (any(map(str.isalpha, password))==True) and (len(password)>=8):
            mycursor.execute("SELECT username FROM users WHERE username = %(username)s", {'username': user})
            mycursor.fetchall()
            hashedPass = hashPswd(password)
            sql = "INSERT INTO logins (username, password, email, first_name, last_name,  dob, user_role, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (user, hashedPass, email, firstName, lastName, dateOfBirth, userRole, status)
            mycursor.execute(sql, val)
            dbconnection.mydb.commit()
            print("\nUser created successfully. Please login with your credentials.")
            return True
        else:
            print("\nError: Please ensure that the password is atleast 8 characters long and includes both letters and numbers.")
            return False
    else:
        print("\nError: User exists already.")
        return False

def existingUser(user:str, password:str) -> tuple:
    """
    Function to authenticate existing user against the database.
    Takes username and cleartext password as input. Password is then hashed and compared against the database records.
  
    If successful, returns authenticated user as tuple: (user id, username, first name, last name)
    """
    if user != "":
        mycursor.execute("SELECT id, username, password, first_name, last_name FROM users WHERE username = %(val)s", {'val':user})
        userResult = mycursor.fetchall()
        if userResult:
            if ph.verify(row[2], password) == True:
                print("\nLogin Successful. WELCOME TO THE DUTCH NCSC DIGITAL FORENSIC SYSTEM, %s!" % row[3])
                return (row[0],row[1],row[3],row[4])
            else:
                print("\nLogin Error: Invalid user")
        else:
            print("\nLogin Error: Invalid user")        
    else:
        print("\nLogin Error: Invalid user")
        
    #Test 