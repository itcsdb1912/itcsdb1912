import psycopg2
import json

def connect_db():
    try:
        connection = psycopg2.connect("host='localhost' port='5432' dbname='test00' user='oytun' password='oytun'")
        print("Connected!")
        return connection
    except:
        print("Connection Failed")
        return False

def create_login_table(tablename):
    connection = connect_db()
    try:
        sql = "CREATE TABLE %s(\
            LoginId SERIAL PRIMARY KEY,\
            Email VARCHAR NOT NULL,\
            AccountPassword VARCHAR NOT NULL );"
        connection.cursor().execute(sql, (tablename,))
        connection.commit()
        print("Table created.")
    except:
        print("Table exists.")
#login table can be created only once.
def signup(email, password):
    connection = connect_db()
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT LoginId, AccountPassword FROM LoginInfo WHERE Email=%s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
    if result == None:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO LoginInfo (Email, AccountPassword) VALUES (%s, %s)"
            cursor.execute(sql, (email, password))
        connection.commit()
        print("You have successfully signed up.")
        return True
    else:
        print("This email address belongs to another account.")
        return False

def login(email, password):
    connection = connect_db()
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT Email, AccountPassword FROM LoginInfo WHERE Email=%s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()

    if result == None:
        print("Email address not found.")
        return False
    else:
        if result[1] == password:
            print("Login successful.")
            return True
        else:
            print("Wrong password.")
            return False

#functions are tested on local.