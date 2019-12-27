Serhat
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
    
