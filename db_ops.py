import psycopg2 
#if db is postgres
#import pymysql 
# if db is mysql
from urllib.parse import urlparse
from SQL_QUERIES import SQL_QUERIES

class database:
    def __init__(self):
        self.connection = None
        self.url = urlparse("postgres://padrjufxoslazm:66097f7c6a273316c865544b566106405e2d014e3f6f61ea3de5d71d42668c0c@ec2-54-247-178-166.eu-west-1.compute.amazonaws.com:5432/d65tnih23lgdao")
    def connect_db(self):
        try:
            self.connection = psycopg2.connect(database = self.url.path[1:],
                                                user = self.url.username,
                                                password = self.url.password,
                                                host = self.url.hostname)
            #self.connection = pymysql.connect(host='remotemysql.com',user='Y2twfztOBJ',password='sDi9LakvoN',db='Y2twfztOBJ')
            print("Connected!")
            return self.connection
        except:
            print("Connection Failed")
            return False


    def create_user(self, username, email, password):      
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id, Password FROM Account WHERE Username=%s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
        if result == None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Account (Username, Email, Password) VALUES (%s, %s, %s)"
                cursor.execute(sql, (username, email, password))
                user = cursor.fetchone()
                print(user)
            self.connection.commit()
            print("You have successfully signed up.")
            return {"err": None, "msg": "You have successfully signed up."}
        else:
            print("Username has taken")
            return {"err": "Username has taken"}
            
    def check_user(self, username, password):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Username, Password FROM Account WHERE Username=%s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()

        if result == None:
            print("User not found.")
            return {'err': 'User not found.' }
        else:
            if result[1] == password:
                print("Login successful.")
                return {'err': None, 'msg': 'Login successful.', 'user': {"username": result[0]}}
            else:
                print("Wrong password.")
                return {'err': 'Wrong password.'}

    def new_store(self, userid, name, address):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT StoreName FROM Store WHERE StoreName=%s"
            cursor.execute(sql, (name,))
            result = cursor.fetchone()
        if result == None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO Store (StoreName, Address, Id) \
                    VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, address, userid))
            self.connection.commit()
            print("You have successfully opened a store.")
            return True
        else:
            print("This store name exists. Please pick another name.")
            return False
    def add_product(self, storeid, product):
        with self.connection.cursor() as cursor:

            # insert to products
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO ProductInfo"
            # save product_id

            # insert to variants with saved product_id

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
            sql = "SELECT Id FROM Account WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            sql = "SELECT Id FROM Account WHERE Email=%s"
            cursor.execute(sql, (newemail,))
            emailexists = cursor.fetchone()
        if result != None:
            if emailexists == None:
                with self.connection.cursor() as cursor:
                    # Create a new record
                    sql = "UPDATE Account SET Email=%s WHERE Id=%s"
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
            sql = "SELECT Password FROM Account WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "UPDATE Account SET Password=%s WHERE Id=%s"
                cursor.execute(sql, (newpassword,id))
            self.connection.commit()
            print("Password successfully updated.")
            return True
        else:
            print("Email address does not exist.")
            return False
    def update_store(self, id, name, address):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM Store WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            sql = "SELECT Id FROM Store WHERE StoreName=%s"
            cursor.execute(sql, (name,))
            nameexists = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                    # Create a new record
                    sql = "UPDATE Store SET StoreAddress=%s StoreName=%s WHERE Id=%s"
                    cursor.execute(sql, (name, address, id))
            self.connection.commit()
            print("Store name successfully updated.")
            return True
        else:
            print("Store does not exist.")
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
            cursor.execute(sql, (id,))
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

    def delete_account(self, userid):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM Account WHERE Id=%s"
            cursor.execute(sql, (userid,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM Account WHERE Id=%s"
                cursor.execute(sql, (userid,))
            self.connection.commit()
            print("User successfully deleted.")
            return True
        else:
            print("User deletion failed.")
            return False
    def delete_store(self, storeid):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM Store WHERE Id=%s"
            cursor.execute(sql, (storeid,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM Store WHERE Id=%s"
                cursor.execute(sql, (storeid,))
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
                cursor.execute(sql, (productid,))
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
                cursor.execute(sql, (variantid,))
            self.connection.commit()
            print("Variant successfully deleted.")
            return True
        else:
            print("Variant deletion failed.")
            return False

    def get_data(self):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM Account"
            cursor.execute(sql, ())
            result = cursor.fetchall()
            print(result)

    # INITIALIZING DB AND SOME UTILITY METHODS

    def create_tables(self):
        self.create_user_table()
        self.create_store_table()
        self.create_product_table()
        self.create_variant_table()

    def has_user(self):
        sql_query = "SELECT Id FROM Account"
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query,)
            result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True

    def drop_tables(self):
        sql_query = "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query,)
        return True
    
    def create_user_table(self):
        sql = SQL_QUERIES["create_user_table"]
        self.connection.cursor().execute(sql,)
        self.connection.commit()
        print("User table ready.")

    def create_store_table(self):
        
        sql = SQL_QUERIES["create_store_table"]
        self.connection.cursor().execute(sql, )
        self.connection.commit()
        print("Store table ready.")

    def create_product_table(self):
    
        sql = SQL_QUERIES["create_product_table"]
        self.connection.cursor().execute(sql,)
        self.connection.commit()
        print("Product table ready")

    def create_variant_table(self):
        
        sql = SQL_QUERIES["create_variant_table"]
        self.connection.cursor().execute(sql, )
        self.connection.commit()
        print("Variant table ready.")
def test_case():
    db = database()
    db.connect_db()
    db.create_user_table()
    db.create_store_table()
    db.signup('test@sample.com', 'testsecret')
    db.login('test@sample.com', 'testsecret')

    uid = 1
    sid = 2
    pid = 3
    vid = 5

    db.new_store(uid,"Test Store 2", "İTÜ Gümüşsuyu")
    db.new_store(uid,"Test Store 1", "İTÜ Taşkışla")

    db.create_product_table()
    db.create_variant_table()
    db.add_product(sid, "sampletrend", "test", 15.5, 0)

    db.add_variant(pid, 800, color="Yellow", size="XL")

    db.change_email(uid,"changed2@sample.com")
    db.change_Name(sid, "testchangename")
    db.change_storeaddress(sid, "İTÜ Tuzla")
    db.change_password(uid, "testchanged")
    db.change_productprice(pid, 322.85)
    db.change_productdiscount(pid, 0.15)
    db.update_variantstock(vid, 11)

    #db.delete_store(sid)
    #db.delete_variant(vid)
    #db.delete_account(uid)
    #db.delete_product(pid)

#test_case()

db = database()
db.connect_db()
db.get_data()

#uid = user, sid = store, pid = product, vid = variant
#You need to check uid, sid, pid and vid to ensure they get the right values as in the database table
#Thats because auto increment continues from the last value
#(e.g. new id can be 9, even if there is no 8. That means id 8 is created before but it is deleted.)

#All above functions are tested.