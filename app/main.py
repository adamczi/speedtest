# import sys
from flask import Flask, render_template, session, send_file, url_for, \
request, abort, redirect

# parsing values from DB
import json
import datetime
from decimal import *

# from psycopg2 import DataError
from config import SECRET_KEY, DEBUG
from utils import messages, validate, loggedIn, Record, whoLoggedIn
from query import query, cache
import os
import re
import tempfile
import csv
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


# just a mainpage
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
                    username = request.json.get('username'),
                    ip = request.json.get('ip'),
                    provider = request.json.get('provider'))

    # print record.timestamp, record.download, record.upload, record.ping, record.key, record.username

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
                   "api": record.key,
                   "ip": record.ip,
                   "provider": record.provider})
        db.commit()
    return 201


# This route shows his/her graph to the logged in user
@app.route("/stats")
@loggedIn
def stats():
    if cache.get('results') is None and 'refresh' not in session:
        query(session['user'])

    c = cache.get('results')

    return render_template('stats.html', downs = c[0], ups = c[1], pings = c[2],
                           username = session['username'])


# To do: passwd change etc, data and account removal
# To do: leaflet map with geolocalised IP
@app.route('/user/<username>')
@whoLoggedIn
def userPanel():
    c = cache.get('results')
    return render_template('userPanel.html', records = c, loggedIn = True,
                           username = session['username'])


@app.route('/user/download')
@loggedIn
def downloadTable():
    if cache.get('results') is None and 'refresh' not in session:
        query(session['user'])
    c = cache.get('results')

    with tempfile.NamedTemporaryFile(suffix=".csv") as tmp:
        for i in range(len(c[0])):
            row = ",".join([str(c[0][i][0]),
                            str(c[0][i][1]),
                            str(c[1][i][1]),
                            str(c[2][i][1]),
                            str(c[3][i][1]),
                            str(c[4][i][1])])
            tmp.write(row+'\n')
        return send_file(tmp.name, as_attachment=True, attachment_filename='survey.csv')


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
