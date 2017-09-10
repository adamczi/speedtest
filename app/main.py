# import sys
from flask import Flask, render_template, session, send_file, url_for, \
request, abort, redirect

# parsing values from DB
import json
import datetime
from decimal import *

from psycopg2 import DataError
from config import SECRET_KEY, DEBUG
from utils import messages, validate, loggedIn, dateToJS, Record, whoLoggedIn
from db import db
import os
import re
import psycopg2
import pg_simple

# App start
app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG


# Blueprints
from auth import authentication
app.register_blueprint(authentication)

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# just a random mainpage
@app.route("/")
def itWorks():
    return "aXQgd29ya3Mh=="


# The API route to call from your script
@app.route("/api", methods=["POST"])
def getValues():
    record = Record(timestamp = request.json.get('timestamp'),
                    download = request.json.get('download'),
                    upload = request.json.get('upload'),
                    ping = request.json.get('ping'),
                    key = request.json.get('api'),
                    username = request.json.get('username'))

    print record.timestamp, record.download, record.upload, record.ping, record.key, record.username

    # Save into the DB
    result = saveToDatabase(record)

    # Return the response code depending on result
    if result:
        return '',result
    else:
        return 404


# Funtion which saves the data
@validate
def saveToDatabase(record):
    with pg_simple.PgSimple() as db:
        db.insert("data",
                  {"datetime": record.timestamp,
                   "download": record.download,
                   "upload": record.upload,
                   "ping": record.ping,
                   "api": record.key})
        db.commit()
    return 201

# This route shows his/her graph to the logged in user
@app.route("/stats")
@loggedIn
def stats():
    with pg_simple.PgSimple() as db:
        statistics = db.fetchall('data',
                                 fields=['datetime','download','upload','ping'],
                                 where=('api = %s', [session['user']]),
                                 order=['datetime', 'ASC'])

    # Convert the dump to JS-friendly format
    ups = []
    downs = []
    pings = []
    for record in statistics:
        date = dateToJS(record[0]) # TO DO: timezone correction (currently GMT)
        down = float(record[1])
        up = float(record[2])
        pi = float(record[3])

        # Three different series of data
        downs.append([date, down])
        ups.append([date, up])
        pings.append([date, pi])

    return render_template('stats.html',
                           ups = ups, downs = downs, pings = pings,
                           username = session['username'])


# To do: user panel with statistics, passwd change etc
@app.route('/user/<username>')
@whoLoggedIn
def userPanel():

    return render_template('userPanel.html', username = session['username'])


@app.route('/manual')
def manual():
    if 'username' in session:
        loggedIn = True
        username = session['username']
    else:
        loggedIn = False
        username = None

    return render_template('manual.html',
                           loggedIn = loggedIn,
                           username = username)

# Redirect to custom page in case of invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# inactive test routing
# @app.route('/index')
# # @loggedIn
# def index():
#     return render_template('index.html')
