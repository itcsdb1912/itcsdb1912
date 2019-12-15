from flask import Flask, request, redirect, url_for, render_template
from shopifycontroller import shopify_controller
app = Flask(__name__)

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
    try:
        products = shopifyctrl.get_products()
        product_names = ''

        for p in products:
            product_names += '///////////// ' + p.title
        return product_names
    except Exception as e:
        return 'err'

@app.route('/create_user', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        return create_user(request.form)
    else:
        return show_create_user_page()

@app.route('/list')
def list():
    return 'I think it works.'


def create_user(user):
    print(user["password"])
    return render_template('show_user.html', u=user)
    
def show_create_user_page():
    return render_template('create_user.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0:5000')