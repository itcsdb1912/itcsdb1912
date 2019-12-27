OYTUN
=======

Methods implemented by me in db_ops.py

    
**********************************************************************************
Function to add a spesific shopify product, also used in sync_products function
**********************************************************************************

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
            
***********************************************************
add information about a shopify product variant attribute
***********************************************************

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
            
***************************************************************
update information about a shopify product variant attribute
***************************************************************

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
            
*********************************************************************************
make a shopify product accessible or if id is None, access all  shopify products
*********************************************************************************

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
            
*****************************************************************
delete a shopify product and all information about its variants
*****************************************************************

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
            
***************************************************************
delete information about a shopify product variant attribute
***************************************************************

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
            
**************************************************************************
delete a store location information if the store does not exist any more
**************************************************************************

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
            
******************************************************************
Utility method to be able to recreate all the tables from scratch
******************************************************************

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
            
*****************************************************  
Utility method to check if a user exists in database
*****************************************************

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
            
**************************************************************
Utility method to check which information exists in a table
**************************************************************

.. code-block:: python

    def get_colnames(self, tablename):
        sql = "SELECT COLUMNS FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (tablename,))
            result = cursor.fetchall()
            print(result)
