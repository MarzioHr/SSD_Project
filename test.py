import psycopg2 # Postgresql connector library


#conn = psycopg2.connect("dbname=suppliers user=postgres password=postgres")

conn = psycopg2.connect(
    host="localhost",
    database="authentication",
    user="postgres",
    password="LifQMP%m3%VTXW9C")

 # Temp code for Verify connection
mycursor = mydb.cursor()
  
mycursor.execute("show columns in logins;")
  
myresult = mycursor.fetchall()
  
for x in myresult:
    print(x)