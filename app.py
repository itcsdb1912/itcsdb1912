from flask import Flask, request, redirect, url_for, render_template, session
from flask_session import Session
from validator_collection import validators, checkers, errors
import os
import redis
import shopify
import secrets

from shopifycontroller import shopify_controller
from db_ops import database


redis_url = os.environ.get('REDISTOGO_URL', "redis://redistogo:63fe48bb2ffdf60819e7231401fe283c@porgy.redistogo.com:11781/")

redis_db = redis.from_url(redis_url)

app = Flask(__name__)


# session related
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_REDIS"] = redis_db


shopifyconfig = {
    'API_KEY':'3ec8f9e2dbc135965075c70c0ee75e01',
    'PASSWORD':'9b090a0649866192112b7bc40c0e359e',
    'API_VERSION':'2019-10',
    'SHOP_NAME':'testandrest'
}
shopifyctrl = shopify_controller(shopifyconfig)
shopifyctrl.connect()

db = database()
db.connect_db()
db.create_tables()

@app.route('/')
def index():
    user = session.get('user')
    
    if(db.has_user()):
        if(user):
            return render_template('index.html', user=user)
        else:
            return render_template('login.html')
    else:
        return render_template('create.html')

@app.route('/sync')
def sync():
    user = session.get("user")
    
    if(user):
        user_id = user["id"]
        products = shopifyctrl.get_products()

        
        result = db.sync_products(user_id, products)
        stores = db.get_store(user_id)

        if(result["err"]):
            return render_template("account.html", user=user, err="Sync Failed", stores=stores)
        else:
            
            return redirect(url_for("account"), user=user, stores=stores)
    else:
        return redirect(url_for("index"))
        
@app.route('/drop_tables')
def drop_tables():
    return render_template("index.html")

@app.route('/products')
def products():
    user = session.get('user')
    if (user):
        products = shopifyctrl.get_products()
        return render_template('list_products.html', products=products, user=user)
    else:
        return redirect(url_for('index'))

@app.route('/store',  methods=["GET", "POST"])
def store():
    user = session.get('user')

    if (request.method == "GET"):
        if(user):
            return render_template('store.html', user=user)
        else:
            return redirect(url_for('index'))
    else:
        if(user):
            user_id = user["id"]    
            try:
                store_name = validators.string(request.form.get("store_name"))
                store_address = validators.string(request.form.get("store_address"))
                store_api_key = validators.string(request.form.get("store_api_key"))
                store_password = validators.string(request.form.get("store_password"))
            except:
                return render_template("store.html", err="datas not valid")

            result = db.new_store(user_id, store_name, store_address, store_api_key, store_password)
            if(result["err"]):
                return render_template("store.html", err=result["err"])
            else:
                return redirect(url_for("account"))
        else:
            return redirect(url_for("index"))

@app.route('/store/<int:store_id>/delete')
def delete_store(store_id):
    user = session.get("user")

    if(user):
        if(store_id):
            db.delete_store(store_id)

            return redirect(url_for("account"))
        else:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

@app.route('/store/<int:store_id>',  methods=["GET", "POST"])
def store_with_id(store_id):
    user = session.get('user')

    if (request.method == "GET"):
        if(user):
            result = db.get_store(store_id)
            store = result["data"]
            print(store)
            return render_template('store.html', user=user, store=store)
        else:
            return redirect(url_for("index"))
    else:
        if(user):
            user_id = user["id"]
            try:
                store_name = validators.string(request.form.get("store_name"))
                store_address = validators.string(request.form.get("store_address"))
                store_api_key = validators.numeric(request.form.get("store_api_key"))
                store_password = validators.numeric(request.form.get("store_password"))
            except:
                return redirect(url_for("account"), err="Datas not valid")

            db.update_store(user_id, store_name, store_address, store_api_key, store_password)
            return redirect(url_for("account"))
        else:
            return redirect(url_for("index"))
            
@app.route('/product/<int:product_id>', methods=["GET", "POST"])
def product(product_id):
    print(product_id)
    user = session.get('user')

    if(request.method == "GET"):
        if (user):
            p = shopifyctrl.get_product(int(product_id))
            return render_template('product.html', product=p, user=user)
        else:
            return redirect(url_for('index'))
    else:
        if(user):
            try:
                title = validators.string(request.form.get("title"))
                price = validators.float(request.form.get("price"))
                stock = validators.integer(request.form.get("stock"))
            except:
                return redirect(url_for("index", err="datas not valid"))
            product = shopifyctrl.get_product(int(product_id))
            product.title = title
            product.price = price
            product.variants[0].inventory_quantity = stock
            product.save()
            result = db.update_product(product_id, product)

            return redirect(url_for("product/"+product_id))
        else:
            return redirect(url_for('index'))

@app.route('/change_password', methods=["GET", "POST"])
def change_password():
    user = session.get("user")

    if(user):
        if(request.method == "GET"):
            return render_template("change_password.html", user=user)
        else:
            old_password = request.form.get("old_password")
            new_password = request.form.get("new_password")

            result = db.change_password(user["id"], old_password, new_password)

            if (result["err"]):
                return render_template("change_password.html", err=result["err"], user=user)
            else:
                return redirect(url_for('account'))
    else:
        return redirect(url_for("index"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        result = db.check_user(username, password)

        if(result['err']):
            return render_template('login.html', err=result['err'])
        else:
            session['user'] = result['user']
            return render_template('index.html', user=session.get('user'))
    else:
        return render_template('login.html');

@app.route('/logout')
def logout():
    if(session.get('user')):
        session.clear()
    return redirect(url_for('index'))

@app.route('/account', methods=["GET", "POST"])
def account():
    user = session.get('user')

    if(request.method == "GET"):
        if (user):
            user_id = user["id"]
            store_result = db.get_store(user_id)
            stores = store_result["data"]
            
            user_result = db.get_user(user_id)
            user_data = user_result["data"]

            print(user_data)

            return render_template('account.html', user=user_data, stores=stores)
        else:
            return redirect(url_for("index"))
    else:
        username = request.form.get("username")
        email = request.form.get("email")

        user_result = db.get_user(user["id"])
        user_data = user_result["data"]

        result = db.update_user(user_data["id"], username, email)

        return redirect(url_for("account"))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        #TODO: Validation
        result = db.create_user(username, email, password)
        if(result['err']):
            return render_template("create.html", err=result["err"])
        else:
            session['user'] = request.form
            return redirect(url_for("index"))
    else:
        return render_template('create.html');

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0:5000')