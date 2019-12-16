from flask import Flask, request, redirect, url_for, render_template, session
import secrets

from shopifycontroller import shopify_controller
from db_ops import database

app = Flask(__name__)

# session related
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.config["SESSION_TYPE"] = "redis"

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
        products = shopifyctrl.get_products()
        db.sync_products_with(products)

        return redirect(url_for("account"))
    else:
        return redirect(url_for("index"))
@app.route('/drop_tables')
def drop_tables():
    return render_template("index.html")

@app.route('/list_products')
def list_products():
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
            store_name = request.form.get("store_name")
            store_address = request.form.get("store_address")
            store_api_key = request.form.get("store_api_key")
            store_password = request.form.get("store_password")

            db.new_store(user_id, store_name, store_address, store_api_key, store_password)
            return redirect(url_for("account"))
        else:
            return redirect(url_for("index"))

@app.route('/delete_store/<int:store_id>')
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
            store = db.get_store(store_id)
            return render_template('store', user=user, store=store)
        else:
            return redirect(url_for("index"))
    else:
        if(user):
            user_id = user["id"]    
            name = request.form.get("store_name")
            address = request.form.get("store_address")
            api_key = request.form.get("store_api_key")
            password = request.form.get("store_password")

            db.update_store(store_id, user_id, name, address, api_key, password)
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
            name = request.form.get("title")
            price = request.form.get("price")
            stock = request.form.get("stock")

            result = db.update_product(product_id)
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
            result = db.get.store()
            print(result)
            stores = None
            return render_template('account.html', user=user, stores=stores)
        else:
            return redirect(url_for("index"))
    else:
        username = request.form.get("username")
        email = request.form.get("email")

        result = db.update_user(user["id"], username, email)

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