from flask_wtf.csrf import generate_csrf
from flask_wtf import FlaskForm
import os
from flask import url_for
from flask import Flask, request, render_template, redirect, Blueprint, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Set your own secret key
db = SQLAlchemy(app)

main = Blueprint('main', __name__)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(64), unique=True)


def check_login(username, password):
    # Replace this with your own logic to validate the login credentials
    users = {
        "admin": generate_password_hash("admin-password"),
        "user1": generate_password_hash("password1"),
        # Add more usernames and their hashed passwords here.
    }
    if username in users and check_password_hash(users.get(username), password):
        return True
    return False

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            session['username'] = username
            return redirect(url_for('main.create_short_url'))  # Replace '/sl' with url_for function
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@main.route('/', methods=['GET', 'POST'])
def create_short_url():
    if 'username' not in session:
        return redirect(url_for('main.login'))  # Replace '/sl' with url_for function
    
    username = session['username']
    
    if request.method == 'POST':
        original_url = request.form['url']
        short_url = request.form['short_url']
        new_url = URL(original_url=original_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return redirect(url_for('main.create_short_url'))  # Replace '/sl' with url_for function

    urls = URL.query.all()
    base_domain = os.getenv('BASE_DOMAIN', 'localhost')
    csrf_token = generate_csrf()  # generate CSRF token
    return render_template('index.html', username=username, urls=urls,base_domain=base_domain,csrf_token=csrf_token)

@main.route('/<short_url>')
def redirect_to_original_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        return redirect(url.original_url)
    else:
        return 'URL not found', 404

@main.route('/<short_url>/edit', methods=['POST'])
def edit_short_url(short_url):
    new_original_url = request.form['url']
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        url.original_url = new_original_url
        db.session.commit()
        return redirect(url_for('main.create_short_url'))  # Replace '/sl' with url_for function
    else:
        return 'URL not found', 404

@main.route('/<short_url>/delete', methods=['POST'])
def delete_short_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first()
    if url:
        db.session.delete(url)
        db.session.commit()
        return redirect('/sl')
    else:
        return 'URL not found', 404

@main.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main.login'))  # Replace '/sl' with url_for function

app.register_blueprint(main, url_prefix=os.getenv('APP_CONTEXT_PATH', '/sl'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(host='0.0.0.0', debug=True)

