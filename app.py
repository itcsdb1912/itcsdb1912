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
        return redirect(url_for('index'));

@app.route('/product/<int:product_id>')
def product(product_id):
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
    return render_template('account.html')
    
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