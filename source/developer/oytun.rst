OYTUN
=======

Methods implemented by me in db_ops.py



.. code-block:: python

   class database:
    def __init__(self, url):
        self.connection = None
        self.url = url



********
Init db
********

.. code-block:: python

    def connect_db(self):
        try:
            self.connection = psycopg2.connect(database = self.url.path[1:],
                                                user = self.url.username,
                                                password = self.url.password,
                                                host = self.url.hostname)
            print("Connected!")
            return self.connection
        except:
            print("Connection Failed")
            return False

****************************************************
Create tables with the queries from SQL_QUERIES.py
****************************************************

.. code-block:: python

    def create_tables(self):
        table_list = ['create_user_table', 'create_location_table', 'create_category_table', 'create_store_table', 'create_product_table', 'create_variant_table', ]
        for create in table_list:
            with self.connection.cursor() as cursor:
                sql = SQL_QUERIES[create]
                cursor.execute(sql,)
            self.connection.commit()
        print("Tables ready.")
        return {"err": None, "msg": "Tables are ready to use."}

***************************************************
Able to sync Users shopify store and our database
***************************************************

.. code-block:: python 

    def sync_products(self, user_id, products):
        print(products)
        sql_get_store_id = "SELECT Id FROM Store WHERE UserId = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql_get_store_id, (user_id,))
                store_id = cursor.fetchone()[0]

            for product in products:
                print(product)
                self.add_product(store_id, product, update_iferror=True)

            return {'err': None, 'msg': 'Sync success.'}
        except:
            self.connection.rollback()
            return {'err': 'Sync failed.'}

***************************************************    
Get user by id
***************************************************

.. code-block:: python

    def get_user(self, id):
        if id != None:
            sql = "SELECT * FROM Account WHERE Id=%s"
            with self.connection.cursor() as cursor:
                cursor.execute(sql,(id,))
                result = cursor.fetchone()
            if result != None:
                return {'err':None, 'msg': 'One user data collected.', 'data':{'id':result[0], 
                                                                        'username':result[1], 
                                                                        'email':result[2],
                                                                        'timestamp':result[3],
                                                                        'password':result[4]}}
            else:
                return {'err':'Id cannot be found.'}

***************************************************    
Create user
***************************************************

.. code-block:: python

    def create_user(self, username, email, password):  
        try:    
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = SQL_QUERIES['create_user']
                cursor.execute(sql, (username, email, password))
                result = cursor.fetchone()
                print(result)
            self.connection.commit()
            print("You have successfully signed up.")
            return {"err": None, "msg": "You have successfully signed up."," user": {"id": result[0], "username": result[1]}}
        except:
            self.connection.rollback()
            print("Username or email has taken")
            return {"err": "Username or email has taken"}     

***************************************************    
Check if user exist
***************************************************

.. code-block:: python

    def check_user(self, username, password):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id, Username, Password FROM Account WHERE Username=%s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()

        if result == None:
            print("User not found.")
            return {'err': 'User not found.' }
        else:
            if result[2] == password:
                print("Login successful.")
                return {'err': None, 'msg': 'Login successful.', 'user': {"id":result[0],"username": result[1]}}
            else:
                print("Wrong password.")
                return {'err': 'Wrong password.'}

***************************************************    
Update users credentials
***************************************************

.. code-block:: python

    def update_user(self, id, username, email):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE Account SET Username =%s WHERE Id=%s"
                cursor.execute(sql, (username, id,))
                self.connection.commit()
                try:
                    with self.connection.cursor() as cursor:
                        sql = "UPDATE Account SET Email =%s WHERE Id=%s"
                        cursor.execute(sql, (email, id,))
                        self.connection.commit()
                        print("Email changed.")
                        return {'err': None, 'msg': 'Email changed.'}
                except:
                    self.connection.rollback()
                    print("Email already exists.")
                    return {'err': 'Email already exists.'}
                print("Username changed.")
                return {'err': None, 'msg': 'Username changed.'}
        except:
            self.connection.rollback()
            try:
                with self.connection.cursor() as cursor:
                    sql = "UPDATE Account SET Email =%s WHERE Id=%s"
                    cursor.execute(sql, (email, id,))
                    self.connection.commit()
                    print("Email changed.")
                    return {'err': None, 'msg': 'Email changed.'}
            except:
                self.connection.rollback()
                print("Email already exists.")
                return {'err': 'Email already exists.'}
            print("Username already exists.")
            return {'err': 'Username already exists.'}        

***************************************************    
Change password
***************************************************

.. code-block:: python

    def change_password(self, id, oldpassword, newpassword):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Password FROM Account WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
        if result != None and result[0] == oldpassword:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "UPDATE Account SET Password=%s WHERE Id=%s"
                cursor.execute(sql, (newpassword,id))
            self.connection.commit()
            print("Password successfully updated.")
            return {'err': None, 'msg': 'Password successfully updated.'}
        elif result == None:
            print("User does not exist.")
            return {'err': 'User does not exist.'}
        else:
            print("Password does not match.")
            return {'err': 'Password does not match.'}

***************************************************    
Delete user's account
***************************************************

.. code-block:: python

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
    

***************************************************
Get store with provided id
***************************************************

.. code-block:: python

    def get_store(self, userid, id=None):

        if id != None:
            sql = "SELECT * FROM Store WHERE Id=%s AND UserId=%s"
            with self.connection.cursor() as cursor:
                cursor.execute(sql,(id,userid))
                result = cursor.fetchone()
            if result != None:
                
                return {'err':None, 'msg': 'One store data collected.', 'data':{'id':result[0], 
                                                                        'apikey':result[1], 
                                                                        'password':result[2],
                                                                        'storename':result[3],
                                                                        'isactivated':result[4],
                                                                        'timestamp':result[5],
                                                                        'locationid':result[6],
                                                                        'userid':result[7]}}
            else:
                return {'err':'Id cannot be found.'}
                
        else:
            sql = "SELECT * FROM Store WHERE UserId=%s"
            with self.connection.cursor() as cursor:
                cursor.execute(sql,(userid,))
                result = cursor.fetchall()
            message = {'err':None, 'msg': 'All store data collected.', 'data': []}
            for store in result:
                message['data'].append({'id':store[0], 
                                            'apikey':store[1], 
                                            'password':store[2],
                                            'storename':store[3],
                                            'isactivated':store[4],
                                            'timestamp':store[5],
                                            'locationid':store[6],
                                            'userid':store[7],
                                            })
            return message

***************************************************    
Create a store in db
***************************************************

.. code-block:: python

    def new_store(self, userid, name, locationid, apikey='default', password='default'):
        with self.connection.cursor() as cursor:
            try:
                # Create a new record
                sql = SQL_QUERIES['new_store']
                cursor.execute(sql, (name, locationid, userid, apikey, password))
                self.connection.commit()
                print("You have successfully opened a store.")
                return {'err': None, 'msg': 'Store is opened.'}
            except:
                self.connection.rollback()
                print("This store name exists. Please pick another name.")
                return {'err': 'Store name exists.'}            

***************************************************    
Update store's info
***************************************************

.. code-block:: python

    def update_store(self, id, name, locationid, apikey, password):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM Store WHERE Id=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            sql = "SELECT Id FROM Store WHERE StoreName=%s"
            cursor.execute(sql, (name,))
            nameexists = cursor.fetchone()
        if result != None:
            if nameexists == None:
                with self.connection.cursor() as cursor:
                    # Create a new record
                    sql = "UPDATE Store SET LocationId=%s, StoreName=%s, ApiKey=%s, Password=%s WHERE Id=%s"
                    cursor.execute(sql, (locationid, name, apikey, password, id,))
                self.connection.commit()
                print("Store successfully updated.")
                return {'err': None, 'msg': 'Store successfully updated.'}
            else:
                print("Store name already exists")
                return {'err': 'Store name already exists.'}
            
        else:
            print("Store does not exist.")
            return {'err': 'Store does not exist.'}

***************************************************    
Delete the store
***************************************************

.. code-block:: python

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
    

***************************************************
Activate store
***************************************************

.. code-block:: python

    def activate_store(self, userid, storeid):
        sql = "SELECT * FROM Store WHERE UserId=%s AND IsActivated=1"
        with self.connection.cursor() as cursor:
            cursor.execute(sql,(userid,))
            result = cursor.fetchone()
        if result == None:
            sql = "UPDATE Store SET IsActivated=1  WHERE Id=%s"
            with self.connection.cursor() as cursor:
                cursor.execute(sql,(storeid,))
                self.connection.commit()
            return {'err': None, 'msg': 'Store is activated.'}
        else:
            return {'err': 'There is another active store.'}

***************************************************    
Deactivate store
***************************************************

.. code-block:: python

    def deactivate_store(self, userid):
        sql = "UPDATE Store SET IsActivated=-1  WHERE IsActivated=1 AND UserId=%s"
        with self.connection.cursor() as cursor:
            cursor.execute(sql,(userid,))
            self.connection.commit()
        return {'err':None, 'msg': 'Store deactivated.'}

***************************************************
Get user's active store
***************************************************

.. code-block:: python

    def get_active_store(self, userid):
        sql = "SELECT * FROM Store WHERE UserId=%s AND IsActivated=1"
        with self.connection.cursor() as cursor:
            cursor.execute(sql,(userid,))
            result = cursor.fetchone()
        if result != None:
            return {'err':None, 'msg': 'Active store data collected.', 'data':{'id':result[0], 
                                                                        'apikey':result[1], 
                                                                        'password':result[2],
                                                                        'storename':result[3],
                                                                        'isactivated':result[4],
                                                                        'timestamp':result[5],
                                                                        'locationid':result[6],
                                                                        'userid':result[7]}}
        else:
            return  {'err':'There is no active store.'}
    
***************************************************    
Function to add a spesific shopify product, also used in sync_products function
***************************************************

.. code-block:: python

    def add_product(self, store_id, product, update_iferror=False):
        # insert to variants with saved product_id
        print("check1")
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                

                sql_add_product = SQL_QUERIES['add_product']
                
                cursor.execute(sql_add_product, (str(product.id),
                                    product.title,
                                    product.images[0].src,
                                    product.variants[0].price,
                                    product.body_html,
                                    store_id,))
            print("check2")
            self.connection.commit()
            for variant in product.variants:
                self.add_variant(variant)
            print("You have successfully synced a product.")
            return {'err':None,'msg':'You have successfully created a product.'}
        except:
            print("check3")
            self.connection.rollback()
            message = {'err':'This product exists.'}
            if update_iferror==True:
                self.update_product(store_id, product)
                print("Product updated instead of being added.")
                message['msg'] = 'Product updated instead of being added.'
            print("This product exists.")
            return message
            
***************************************************    
add information about a shopify product variant attribute
***************************************************

.. code-block:: python

    def add_variant(self, variant):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = SQL_QUERIES['add_variant']
                cursor.execute(sql, (str(variant.id), 
                                    variant.option1, 
                                    variant.option2, 
                                    variant.option3,
                                    variant.inventory_quantity, 
                                    variant.sku,
                                    variant.compare_at_price,
                                    str(variant.product_id),))
            self.connection.commit()
            print("You have successfully added a variant.")
            return {'err':None,'msg':'You have successfully added a variant.'}
        except:
            self.connection.rollback()
            print("Variant id exists.")
            return {'err':'Variant id exists.'}
            
***************************************************    
update information about a shopify product
***************************************************

.. code-block:: python

   def update_product(self, store_id, product):
        print("check4")
        with self.connection.cursor() as cursor:
            sql = "UPDATE Product \
                SET ProductName=%s, ProductPrice=%s,ProductDescription=%s,StoreId=%s WHERE Id=%s"
            cursor.execute(sql, (product.title, 
                                product.variants[0].price, 
                                product.body_html, 
                                store_id, 
                                str(product.id),))


            print("check5")
            self.connection.commit()
            for variant in product.variants:
                self.update_variant(product.id, variant)
            print("Product attributes changed.")
            return {'err': None, 'msg': 'Product attributes changed.'}
            
***************************************************    
update information about a shopify product variant attribute
***************************************************

.. code-block:: python

    def update_variant(self, product_id, variant):
        with self.connection.cursor() as cursor:
            sql = "UPDATE ProductVariant \
                SET Option1=%s, Option2=%s,Option3=%s,Stock=%s,Sku=%s, CompareAtPrice=%s, ProductId=%s WHERE Id=%s"
            print("################3")

            cursor.execute(sql, (variant.option1, 
                                variant.option2, 
                                variant.option3,
                                variant.inventory_quantity, 
                                variant.sku,
                                variant.compare_at_price,
                                str(product_id), 
                                str(variant.id),))
            self.connection.commit()
            print("Product Variant attributes changed.")
            return {'err': None, 'msg': 'Product Variant attributes changed.'}
            
***************************************************    
make a shopify product accessible or if id is None, access all  shopify products
***************************************************

.. code-block:: python

   def get_product(self, storeid, id=None ):
        
        if id != None:
            sql = "SELECT * FROM Product WHERE StoreId=%s AND Id=%s"
            with self.connection.cursor() as cursor:
                cursor.execute(sql,(storeid,str(id),))
                result = cursor.fetchone()
            if result != None:
                return {'err':None, 'msg': 'One Product data collected.', 'data':{'id':result[0], 
                                                                        'title':result[1], 
                                                                        'price':result[2],
                                                                        'description':result[3],
                                                                        'timestamp':result[4],
                                                                        'image':result[5],
                                                                        'categoryid':result[6],
                                                                        'storeid':result[7]}}
            else:
                return {'err':'Id cannot be found.'}
                
        else:
            sql = "SELECT * FROM Product WHERE StoreId=%s"
            with self.connection.cursor() as cursor:
                cursor.execute(sql,(storeid,))
                result = cursor.fetchall()
            message = {'err':None, 'msg': 'All Product data collected.', 'data': []}
            for product in result:
                message['data'].append({'id':product[0], 
                                        'title':product[1], 
                                        'price':product[2],
                                        'description':product[3],
                                        'timestamp':product[4],
                                        'image':product[5],
                                        'categoryid':product[6],
                                        'storeid':product[7]})
            return message
            
***************************************************    
delete store and its all relevant information
***************************************************

.. code-block:: python

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
            
***************************************************    
delete a shopify product and all information about its variants
***************************************************

.. code-block:: python

    def delete_product(self, productid):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM Product WHERE Id=%s"
            cursor.execute(sql, (str(productid),))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM Product WHERE Id=%s"
                cursor.execute(sql, (str(productid),))
            self.connection.commit()
            print("Product successfully deleted.")
            return True
        else:
            print("Product deletion failed.")
            return False
            
***************************************************    
delete information about a shopify product variant attribute
***************************************************

.. code-block:: python

    def delete_variant(self, variantid):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM ProductVariant WHERE Id=%s"
            cursor.execute(sql, (variantid,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM ProductVariant WHERE Id=%s"
                cursor.execute(sql, (variantid,))
            self.connection.commit()
            print("Variant successfully deleted.")
            return True
        else:
            print("Variant deletion failed.")
            return False
            
***************************************************    
delete a store location information if the store does not exist any more
***************************************************

.. code-block:: python
    def delete_location(self,locationid):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Id FROM Location WHERE Id=%s"
            cursor.execute(sql, (locationid,))
            result = cursor.fetchone()
        if result != None:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "DELETE FROM Location WHERE Id=%s"
                cursor.execute(sql, (locationid,))
            self.connection.commit()
            print("Variant successfully deleted.")
            return True
        else:
            print("Variant deletion failed.")
            return False
            
***************************************************    
Utility method to be able to recreate all the tables from scratch
***************************************************

.. code-block:: python

   def drop_tables(self):
        table_list = ['ProductVariant' ]
        for table in table_list:
            with self.connection.cursor() as cursor:
                sql = "DROP TABLE " + table + " CASCADE"
                cursor.execute(sql,())
            self.connection.commit()
        print("Tables deleted.")
        return {"err": None, "msg": "Tables are dropped, please create again to continue."} 
        
***************************************************    
Utility method to be able to show data in a table
***************************************************

.. code-block:: python

    def get_data(self, tablename):
        with self.connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM " + tablename
            cursor.execute(sql, )
            result = cursor.fetchall()
            print(result)
            
***************************************************    
Utility method to check if a user exists in database
***************************************************

.. code-block:: python

    def has_user(self):
        sql_query = "SELECT Id FROM Account"
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query,)
            result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True
            
***************************************************    
Utility method to check if all tables exist
***************************************************

.. code-block:: python

    def get_tablenames(self):
        sql = SQL_QUERIES["get_tables"]
        with self.connection.cursor() as cursor:
            cursor.execute(sql, ())
            result = cursor.fetchall()
            print(result)
            
***************************************************    
Utility method to check which information exists in a table
***************************************************

.. code-block:: python

    def get_colnames(self, tablename):
        sql = "SELECT COLUMNS FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (tablename,))
            result = cursor.fetchall()
            print(result)
