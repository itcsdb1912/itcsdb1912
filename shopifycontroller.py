import shopify
import psycopg2
import os
from urllib.parse import urlparse
result = urlparse("postgres://padrjufxoslazm:66097f7c6a273316c865544b566106405e2d014e3f6f61ea3de5d71d42668c0c@ec2-54-247-178-166.eu-west-1.compute.amazonaws.com:5432/d65tnih23lgdao")
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname

class shopify_controller:
    def __init__(self, config):
        self.config = config


    def connect(self):
        connection = psycopg2.connect(
            database = database,
            user = username,
            password = password,
            host = hostname
        )

        try:
            cur = connection.cursor()
            cur.execute('SELECT 1')
            print("db connected")
        except:
            print("db error")

        shop_url = "https://%s:%s@%s.myshopify.com/admin/api/%s" % \
            (self.config['API_KEY'], self.config['PASSWORD'], self.config['SHOP_NAME'], self.config['API_VERSION'])

        shopify.ShopifyResource.set_site(shop_url)

    def get_products(self):
        if(shopify == None):
            raise Exception("No shopify instance")
        else:
            shop = shopify.Shop.current()
            products = shopify.Product.find()
            return products

    def update_product(self, product_id):
        if(shopify == None):
            raise Exception("No shopify instance")
        else:
            product = shopify.Product.find(product_id)

            if(product == None):
                raise Exception("No such product")
            else:
                # update here
                return True


