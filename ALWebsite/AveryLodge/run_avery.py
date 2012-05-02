#!/bin/env python

from __future__ import with_statement
from contextlib import closing
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
        abort, render_template, flash


# Configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# Create application
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    '''
    init_db initializes the database. We use the connect_db function.
    
    The closing() helper function allows us to keep a connection open 
    for the duration of the `with` block.

    The open_resource() method of the application object supports that
    functionality out of the box, so itcan used in the `with` block 
    directly.
    '''
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/documents')
def documents():
    return render_template('documents.html')

@app.route('/executive')
def executive():
    return render_template('executive.html')

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/album')
def album():
    return render_template('album.html')

if __name__ == '__main__':
    app.run()
