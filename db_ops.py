import pymysql
import json

def connect_db():
    try:
        connection = pymysql.connect(host='sql7.freesqldatabase.com',
                             user='sql7309708',
                             password='FGXydIM8XQ',
                             db='sql7309708',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        print("Connected!")
        return connection
    except:
        print("Connection Failed")
        return False

def create_login_table():
    connection = connect_db()
    with connection.cursor() as cursor:
        sql = "CREATE TABLE LoginInfo(\
            LoginId INT AUTO_INCREMENT,\
            Email VARCHAR(100),\
            AccountPassword VARCHAR(100),\
            PRIMARY KEY (LoginId));"
        cursor.execute(sql)

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
            sql = "INSERT INTO Customers (Email, AccountPassword) VALUES (%s, %s)"
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
        sql = "SELECT AccountPassword FROM LoginInfo WHERE Email=%s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
    if result == None:
        print("Email address not found.")
        return False
    else:
        if result == password:
            print("Login successful.")
            return True
        else:
            print("Wrong password.")
            return False

#signup -> GET: show form, POST: if user exist print FAIL, else: save -> then print OK signed up
#login -> success / fail
