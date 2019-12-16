from flask import Flask, request, redirect, url_for, render_template, session
import secrets

from shopifycontroller import shopify_controller
from db_ops import database

app = Flask(__name__)

# session related
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.config["SESSION_TYPE"] = "redis"

shopifyconfig = {
    'API_KEY':'89845d72235b041b2768eefada433d19',
    'PASSWORD':'be009fcef7485dd88d70d1ec24215749',
    'API_VERSION':'2019-10',
    'SHOP_NAME':'havuz-pool'
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
            user_id = user.id    
            store_name = request.form.get("store_name")
            store_address = request.form.get("store_address")
            store_api_key = request.form.get("store_api_key")
            store_password = request.form.get("store_password")

            db.new_store(user_id, store_name, store_address, store_api_key, store_password)
            return redirect(url_for("account"))
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
            user_id = user.id    
            name = request.form.get("store_name")
            address = request.form.get("store_address")
            api_key = request.form.get("store_api_key")
            password = request.form.get("store_password")

            db.update_store(store_id, user_id, name, address, api_key, password)
            return redirect(url_for("account"))
        else:
            return redirect(url_for("index"))
            
@app.route('/product/<int:product_id>')
def product(product_id):
    print(product_id)
    user = session.get('user')
    if (user):
        p = shopifyctrl.get_product(int(product_id))
        return render_template('product.html', product=p, user=user)
    else:
        return redirect(url_for('index'));


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

@app.route('/account')
def user():
    user = session.get('user')
    if (user):
        return render_template('account.html', user=user, stores=None)
    else:
        return redirect(url_for("index"))

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