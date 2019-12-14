from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)

@app.route('/')
def index():
    if request.cookies:
        check()
    else:
        return render_template('index.html')


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
    app.run(debug=True,host='0.0.0.0')