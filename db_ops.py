#import psycopg2 if db is postgres
import pymysql # if db is mysql
import json
from datetime import datetime

class database:
    def __init__(self):
        self.connection = None
    def connect_db(self):
        try:
            #self.connection = psycopg2.connect("host='remotemysql.com' dbname='Y2twfztOBJ' user='Y2twfztOBJ' password='sDi9LakvoN'")
            self.connection = pymysql.connect(host='remotemysql.com',
                    user='Y2twfztOBJ',
                    password='sDi9LakvoN',
                    db='Y2twfztOBJ')
            print("Connected!")
            return self.connection
        except:
            print("Connection Failed")
            return False
    
    def create_user_table(self):
        try:
            sql = "CREATE TABLE UserInfo(\
                UserId SERIAL PRIMARY KEY,\
                Email VARCHAR(50) NOT NULL,\
                CreatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                AccountPassword VARCHAR(25) NOT NULL );"
            self.connection.cursor().execute(sql,)
            self.connection.commit()
            print("User table created.")
        except:
            print("User table exists.")
    def create_store_table(self):
        try:
            sql = "CREATE TABLE StoreInfo(\
                StoreId SERIAL PRIMARY KEY,\
                StoreName VARCHAR(50) NOT NULL,\
                StoreAddress VARCHAR(100) NOT NULL,\
                CreatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                UserId INT REFERENCES UserInfo(UserId));"
            self.connection.cursor().execute(sql, )
            self.connection.commit()
            print("Store table created.")
        except:
            print("Store table exists.")
    def create_product_table(self):
        try:
            sql = "CREATE TABLE ProductInfo(\
                ProductId SERIAL PRIMARY KEY,\
                ProductName VARCHAR(50) NOT NULL,\
                ProductCategory VARCHAR(50) NOT NULL,\
                ProductPrice FLOAT NOT NULL,\
                ProductDiscount FLOAT NOT NULL,\
                CreatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                StoreId INT REFERENCES StoreInfo(StoreId));"
            self.connection.cursor().execute(sql,)
            self.connection.commit()
            print("Product table created")
        except:
            print("Product table exists.")
    def create_variant_table(self):
        try:
            sql = "CREATE TABLE ProductVariantInfo(\
                ProductVariantId SERIAL PRIMARY KEY,\
                Color VARCHAR(15),\
                Size CHAR,\
                Material VARCHAR(25),\
                Stock INT NOT NULL,\
                CreatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                ProductId INT REFERENCES ProductInfo(ProductId));"
            self.connection.cursor().execute(sql, )
            self.connection.commit()
            print("Variant table created.")
        except:
            print("Variant table exists.")

    def signup(self, email, password):      
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT UserId, AccountPassword FROM UserInfo WHERE Email=%s"
            cursor.execute(sql, (email,))
            result = cursor.fetchone()
        if result == None:
            with self.connection.cursor() as cursor:
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
    def add_product(self, name, category, price, discount, storename):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT ProductName FROM ProductInfo WHERE ProductName=%s"
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
        if result == None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO ProductInfo (ProductName, ProductCategory, ProductPrice, ProductDiscount, StoreId) \
                    VALUES (%s, %s, %s, %s, (SELECT StoreId from StoreInfo WHERE StoreName = %s))"
                cursor.execute(sql, (name, category, price, discount, storename))
            self.connection.commit()
            print("You have successfully created a product.")
            return True
        else:
            print("This product name exists. Please pick another name.")
            return False

#db = database()
#db.connect_db()
#db.create_user_table()
#db.create_store_table()
#db.signup('sample@sample.com', 'testsecret')
#db.login('sample@sample.com', 'testsecret')

#db.new_store("Test Store 2", "İTÜ Gümüşsuyu", "sample@sample.com")
#db.add_product("sampletrend", "test", 15.5, 0, "Test Store 2")
#db.create_product_table()
#db.create_variant_table()



#All functions are tested.