import pymysql
import json
import pandas as pd

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
def create_table():
    connection = connect_db()
    with connection.cursor() as cursor:
        sql = "CREATE TABLE LoginInfo(\
            LoginId INT AUTO_INCREMENT,\
            Email VARCHAR(100),\
            AccountPassword VARCHAR(100),\
            PRIMARY KEY (member_id));"
        cursor.execute(sql)

def signup(username, password):
    connection = connect_db()
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT LoginId, AccountPassword FROM LoginInfo WHERE Email=%s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        print(result)
        
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO Customers (Email, AccountPassword) VALUES (%s, %s)"
        cursor.execute(sql, (username, password))
    connection.commit()
    return True
#signup -> GET: show form, POST: if user exist print FAIL, else: save -> then print OK signed up
#login -> success / fail
