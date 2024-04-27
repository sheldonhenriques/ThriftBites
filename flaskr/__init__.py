import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash


def create_app(test_config=None):
    # create and configure the app
    users_db = {}
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'your_secret_key'
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if username in users_db:
                flash('Username already exists.')
                return redirect(url_for('register'))

            users_db[username] = generate_password_hash(password)
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user_hashed_password = users_db.get(username)
            if user_hashed_password and check_password_hash(user_hashed_password, password):
                flash('Login successful!')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password.')

        return render_template('login.html')

    @app.route('/')
    def home():
        # Redirects to the registration page
        return redirect(url_for('register'))

    if __name__ == '__main__':
        app.run(debug=True)

    from . import db
    db.init_app(app)

    return app






