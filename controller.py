# all application config and route logic goes here

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.login import (LoginManager, login_user, logout_user, login_required,
                             current_user)
from model import User, connect_to_db, db, add_user

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY'] #@todo load from config file
app.jinja_env.undefined = StrictUndefined #prevent silent jinja undefined failure

#login functions provided by Flask-login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """Flask-login required, get logged in user object."""

    # remember that user ids in Flask-Login are always unicode strings, 
    # so a conversion to an integer is necessary before we can send the id to Flask-SQLAlchemy.
    return User.query.get(int(user_id))


@app.route('/')
def index():
    """The homepage."""
   
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    """Process login form data and handle authentication."""

    user_name = request.form.get('user_name')
    password = request.form.get('password')
    user = User.query.filter_by(user_name=user_name, password=password).first()

    if user:
        login_user(user)
        return redirect('/business')
    else:
        flash('Error, {} and password did not match a registered user'.format(user_name))
        return redirect('/')


@app.route('/logout')
def logout():
    """Logout current user."""

    logout_user()
    return redirect('/')


@app.route('/register', methods=['POST'])
def register():
    """Register new user and login."""
    
    # @todo validate form data in javascript
    user_name = request.form.get('register_user_name')
    password = request.form.get('register_password')
    first_name = request.form.get('register_first_name')
    last_name = request.form.get('register_last_name')
    email = request.form.get('register_email')
    
    # ensure username is unique (case insensitive)
    user = User.query.filter(User.user_name.ilike(user_name)).first()

    if user:
        flash('{} is already in use. Please select another'.format(user_name))
        return redirect('/')
    else:
        new_user = add_user(user_name=user_name, password=password, 
                            first_name=first_name, last_name=last_name, email=email)
        login_user(new_user)
        return redirect('/business')


@app.route('/business')
def show_business():
    """For logged in user, show information about their business."""

    return render_template('business.html')



if __name__ == '__main__':

    app.debug = os.environ['FLASK_DEBUG']
    # only show toolbar when debug is true
    if app.debug:
        DebugToolbarExtension(app) 

    connect_to_db(app)

    # we are setting the host to 0.0.0.0 because we are running in vagrant
    # if using Mac's python would not need to be specified
    app.run(host='0.0.0.0')
