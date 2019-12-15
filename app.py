from flask import Flask, request, redirect, url_for, render_template, session
import secrets

from shopifycontroller import shopify_controller

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

@app.route('/')
def index():
    if (session.get('user')):
        return render_template('index.html', user=session.get('user'))
    else:
        return render_template('index.html', user=None)



@app.route('/list_products')
def list_products():
    if (session.get('user')):
        products = shopifyctrl.get_products()
        return render_template('list_products', products=products)
    else:
        return redirect(url_for('index'));

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = { 'username': request.form.get('username')}
        return redirect(url_for('index'))
    else:
        return render_template('login.html');

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        print(request.form)
        session['user'] = request.form
    else:
        return render_template('create.html');

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0:5000')