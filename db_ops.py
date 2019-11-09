import psycopg2
import json
class database:
    def __init__(self):
        self.connection = None

    def connect_db(self):
        try:
            self.connection = psycopg2.connect("host='localhost' port='5432' dbname='test00' user='oytun' password='oytun'")
            print("Connected!")
            return self.connection
        except:
            print("Connection Failed")
            return False
    def create_user_table(self):
        try:
            sql = "CREATE TABLE UserInfo(\
                UserId SERIAL PRIMARY KEY,\
                Email VARCHAR NOT NULL,\
                AccountPassword VARCHAR NOT NULL );"
            self.connection.cursor().execute(sql,)
            self.connection.commit()
            print("Table created.")
        except:
            print("Table exists.")
    def signup(self, email, password):      
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT UserId, AccountPassword FROM UserInfo WHERE Email=%s"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
        if result == None:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO UserInfo (Email, AccountPassword) VALUES (%s, %s)"
                cursor.execute(sql, (email, password))
            self.connection.commit()
            print("You have successfully signed up.")
            return True
        else:
            print("This email address belongs to another account.")
            return False
    def login(self, email, password):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Email, AccountPassword FROM UserInfo WHERE Email=%s"
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
    def create_store_table(self):
        try:
            sql = "CREATE TABLE StoreInfo(\
                StoreId SERIAL PRIMARY KEY,\
                StoreName VARCHAR NOT NULL,\
                StoreAddress VARCHAR NOT NULL,\
                UserId INT REFERENCES UserInfo(UserId));"
            self.connection.cursor().execute(sql, )
            self.connection.commit()
            print("Table created.")
        except:
            print("Table exists.")
    def new_store(self, name, address, email):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT StoreName FROM StoreInfo WHERE StoreName=%s"
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
        if result == None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO StoreInfo (StoreName, StoreAddress, UserId) \
                    VALUES (%s, %s, (SELECT UserId from UserInfo WHERE Email = %s))"
                cursor.execute(sql, (name, address, email))
            self.connection.commit()
            print("You have successfully opened a store.")
            return True
        else:
            print("This store name exists. Please pick another name.")
            return False

#db = database()
#db.connect_db()
#db.new_store("Test Store 3", "İTÜ Taşkışla", "sample@sample.com")

#All functions are tested.