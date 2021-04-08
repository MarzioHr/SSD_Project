# import psycopg2 # Postgresql connector library


# #conn = psycopg2.connect("dbname=suppliers user=postgres password=postgres")

# conn = psycopg2.connect(
#     host="localhost",
#     database="authentication",
#     user="postgres",
#     password="LifQMP%m3%VTXW9C")

#  # Temp code for Verify connection
# mycursor = mydb.cursor()
  
# mycursor.execute("show columns in logins;")
  
# myresult = mycursor.fetchall()
  
# for x in myresult:
#     print(x)

import stdiomask

password_clear = input("Please enter clear password: ")
password = stdiomask.getpass()

authentication.py 

#   if user != "":
#     if userExists(user) == True:
#       hashedPass = hashPswd(password)
#       mycursor.execute("SELECT * FROM logins")
#       passResult = mycursor.fetchall()
#       for row in passResult:
#         if row[1] == user:
#           try: 
#             if ph.verify(row[2], password) == True:
#               print("\nLogin Successful. WELCOME TO THE DUTCH ICSC DIGITAL FORENSIC SYSTEM, %s!" % row[3])
#               return (row[0],row[1],row[3],row[4])
#             else:
#               print("\nLogin Error: Password does not match our records")
#           except:
#             print("\nLogin Error: Password does not match our records")
#     else:
#       print("\nLogin Error: User does not exist")
#   else:
#     print("\nLogin Error: Please enter a username")