import shopify
import psycopg2
import os

class shopify_controller:
    def __init__(self, config):
        self.config = config


    def connect(self):
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

    def get_product(self, product_id):
        if(shopify == None):
            raise Exception("No shopify instance")
        else:
            shop = shopify.Shop.current()
            p = shopify.Product.find(product_id)
            return p

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


