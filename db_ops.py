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
                Id INT AUTO_INCREMENT PRIMARY KEY,\
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
                Id INT AUTO_INCREMENT PRIMARY KEY,\
                StoreName VARCHAR(50) NOT NULL,\
                StoreAddress VARCHAR(100) NOT NULL,\
                CreatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                UserId INT NOT NULL,\
                CONSTRAINT user_store\
                    FOREIGN KEY (UserId)\
                    REFERENCES UserInfo (Id)\
                    ON DELETE CASCADE);"
            self.connection.cursor().execute(sql, )
            self.connection.commit()
            print("Store table created.")
        except:
            print("Store table exists.")
    def create_product_table(self):
        try:
            sql = "CREATE TABLE ProductInfo(\
                Id INT AUTO_INCREMENT PRIMARY KEY,\
                ProductName VARCHAR(50) NOT NULL,\
                ProductCategory VARCHAR(50) NOT NULL,\
                ProductPrice FLOAT NOT NULL,\
                ProductDiscount FLOAT NOT NULL,\
                CreatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                StoreId INT NOT NULL,\
                CONSTRAINT store_product\
                    FOREIGN KEY (StoreId)\
                    REFERENCES StoreInfo (Id)\
                    ON DELETE CASCADE);"
            self.connection.cursor().execute(sql,)
            self.connection.commit()
            print("Product table created")
        except:
            print("Product table exists.")
    def create_variant_table(self):
        try:
            sql = "CREATE TABLE ProductVariantInfo(\
                Id SERIAL PRIMARY KEY,\
                Color VARCHAR(15),\
                Size VARCHAR(10),\
                Material VARCHAR(25),\
                Stock INT NOT NULL,\
                CreatedOn TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\
                ProductId INT NOT NULL,\
                CONSTRAINT product_variant\
                    FOREIGN KEY (ProductId)\
                    REFERENCES ProductInfo (Id)\
                    ON DELETE CASCADE);"
            self.connection.cursor().execute(sql, )
            self.connection.commit()
            print("Variant table created.")
        except:
            print("Variant table exists.")

    def signup(self, email, password):      
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id, AccountPassword FROM UserInfo WHERE Email=%s"
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
    def new_store(self, userid, name, address):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT StoreName FROM StoreInfo WHERE StoreName=%s"
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
        if result == None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO StoreInfo (StoreName, StoreAddress, UserId) \
                    VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, address, userid))
            self.connection.commit()
            print("You have successfully opened a store.")
            return True
        else:
            print("This store name exists. Please pick another name.")
            return False
    def add_product(self, storeid, name, category, price, discount):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT ProductName FROM ProductInfo WHERE ProductName=%s"
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
        if result == None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO ProductInfo (ProductName, ProductCategory, ProductPrice, ProductDiscount, StoreId) \
                    VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, category, price, discount, storeid))
            self.connection.commit()
            print("You have successfully created a product.")
            return True
        else:
            print("This product name exists. Please pick another name.")
            return False
    def add_variant(self, productid, stock, color="default", size="default", material="default"):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM ProductVariantInfo WHERE color=%s AND size=%s AND material=%s"
            cursor.execute(sql, (color,size,material))
            result = cursor.fetchone()
        if result == None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO ProductVariantInfo (Color, Size, Material, Stock, ProductId) \
                    VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (color, size, material, stock, productid))
            self.connection.commit()
            print("You have successfully added a variant.")
            return True
        else:
            print("This product variant exists with the same color, size and material type. Please choose something else.")
            return False

    def change_email(self, id, newemail):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM UserInfo WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            sql = "SELECT Id FROM UserInfo WHERE Email=%s"
            cursor.execute(sql, (newemail,))
            emailexists = cursor.fetchone()
        if result != None:
            if emailexists == None:
                with self.connection.cursor() as cursor:
                    # Create a new record
                    sql = "UPDATE UserInfo SET Email=%s WHERE Id=%s"
                    cursor.execute(sql, (newemail,id))
                self.connection.commit()
                print("Email address successfully updated.")
                return True
            else:
                print("Email address already exists")
                return False
        else:
            print("Id does not exist.")
            return False
    def change_password(self, id, newpassword):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT AccountPassword FROM UserInfo WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "UPDATE UserInfo SET AccountPassword=%s WHERE Id=%s"
                cursor.execute(sql, (newpassword,id))
            self.connection.commit()
            print("Password successfully updated.")
            return True
        else:
            print("Email address does not exist.")
            return False
    def change_storename(self, id, newname):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM StoreInfo WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            sql = "SELECT Id FROM StoreInfo WHERE StoreName=%s"
            cursor.execute(sql, (newname,))
            nameexists = cursor.fetchone()
        if result != None:
            if nameexists == None:
                with self.connection.cursor() as cursor:
                    # Create a new record
                    sql = "UPDATE StoreInfo SET StoreName=%s WHERE Id=%s"
                    cursor.execute(sql, (newname,id))
                self.connection.commit()
                print("Store name successfully updated.")
                return True
            else:
                print("Entered store name already exists.")
                return False
        else:
            print("Id does not exist.")
            return False
    def change_storeaddress(self, id, newaddress):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM StoreInfo WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "UPDATE StoreInfo SET StoreAddress=%s WHERE Id=%s"
                cursor.execute(sql, (newaddress,id))
            self.connection.commit()
            print("Store address successfully updated.")
            return True
        else:
            print("Entered store cannot be found.")
            return False
    def change_productprice(self, id, newprice):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM ProductInfo WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "UPDATE ProductInfo SET ProductPrice=%s WHERE Id=%s"
                cursor.execute(sql, (newprice,id))
            self.connection.commit()
            print("Product price successfully updated.")
            return True
        else:
            print("Entered product cannot be found.")
            return False
    def change_productdiscount(self, id, newdiscount):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM ProductInfo WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "UPDATE ProductInfo SET ProductDiscount=%s WHERE Id=%s"
                cursor.execute(sql, (newdiscount,id))
            self.connection.commit()
            print("Product discount successfully updated.")
            return True
        else:
            print("Entered product cannot be found.")
            return False
    def update_variantstock(self, id, newstock):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM ProductVariantInfo WHERE Id=%s"
            cursor.execute(sql, (id))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "UPDATE ProductVariantInfo SET Stock=%s WHERE Id=%s"
                cursor.execute(sql, (newstock, id))
            self.connection.commit()
            print("Variant stock successfully updated.")
            return True
        else:
            print("Entered variant cannot be found.")
            return False


        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM StoreInfo WHERE UserId=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
        if result == None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM UserInfo WHERE Id=%s"
                cursor.execute(sql, (id))
            self.connection.commit()
            print("User successfully deleted.")
            return True
        else:
            print("Stores belong to the user need to be deleted.")

    def delete_account(self, userid):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM UserInfo WHERE Id=%s"
            cursor.execute(sql, (userid,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM UserInfo WHERE Id=%s"
                cursor.execute(sql, (userid))
            self.connection.commit()
            print("User successfully deleted.")
            return True
        else:
            print("User deletion failed.")
            return False
    def delete_store(self, storeid):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM StoreInfo WHERE Id=%s"
            cursor.execute(sql, (storeid,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM StoreInfo WHERE Id=%s"
                cursor.execute(sql, (storeid))
            self.connection.commit()
            print("Store successfully deleted.")
            return True
        else:
            print("Store deletion failed.")
            return False
    def delete_product(self, productid):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM ProductInfo WHERE Id=%s"
            cursor.execute(sql, (productid,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM ProductInfo WHERE Id=%s"
                cursor.execute(sql, (productid))
            self.connection.commit()
            print("Product successfully deleted.")
            return True
        else:
            print("Product deletion failed.")
            return False
    def delete_variant(self, variantid):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM ProductVariantInfo WHERE Id=%s"
            cursor.execute(sql, (variantid,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM ProductVariantInfo WHERE Id=%s"
                cursor.execute(sql, (variantid))
            self.connection.commit()
            print("Variant successfully deleted.")
            return True
        else:
            print("Variant deletion failed.")
            return False

def test_case():
    db = database()
    db.connect_db()
    db.create_user_table()
    db.create_store_table()
    db.signup('test@sample.com', 'testsecret')
    db.login('test@sample.com', 'testsecret')

    uid = 5
    sid = 8
    pid = 4
    vid = 6

    db.new_store(uid,"Test Store 2", "İTÜ Gümüşsuyu")
    db.new_store(uid,"Test Store 1", "İTÜ Taşkışla")

    db.create_product_table()
    db.create_variant_table()
    db.add_product(sid, "sampletrend", "test", 15.5, 0)

    db.add_variant(pid, 800, color="Blue", size="XL", material="%80 COTTON, %20 ELASTANE")
    #db.delete_variant(vid)

    db.change_email(uid,"changed2@sample.com")
    db.change_storename(sid, "testchangename")
    db.change_storeaddress(sid, "İTÜ Tuzla")
    #db.change_password(uid, "testchanged")
    #db.change_productprice(pid, 322.85)
    #db.change_productdiscount(pid, 0.15)
    db.update_variantstock(vid, 11)
    db.delete_store(sid)

#uid = user, sid = store, pid = product, vid = variant
#You need to check uid, sid, pid and vid to ensure they get the right values as in the database table
#Thats because auto increment continues from the last value
#(e.g. new id can be 9, even if there is no 8. That means id 8 is created before but it is deleted.)

#All above functions are tested.