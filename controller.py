# all application config and route logic goes here

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY'] #@todo load from config file
app.jinja_env.undefined = StrictUndefined #prevent silent jinja undefined failure


@app.route('/')
def hello_world():
    print os.environ['FLASK_DEBUG']
    print os.environ['FLASK_SECRET_KEY']
   
    return render_template('index.html')


if __name__ == '__main__':
    
    app.debug = os.environ['FLASK_DEBUG']
    # only show toolbar when debug is true
    if app.debug:
        DebugToolbarExtension(app) 

    # we are setting the host to 0.0.0.0 because we are running in vagrant
    # if using Mac's python would not need to be specified
    app.run(host='0.0.0.0')
