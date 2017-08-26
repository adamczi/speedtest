# import sys

# parsing values from DB
import json
import datetime
from decimal import *

from flask import Flask, render_template, session, send_file, url_for, \
request, abort, redirect
from psycopg2 import DataError
from config import key_secret, userTable
from utils import messages, validate, loggedIn, dateToJS, Record
from db import pool, db
import os
import re
import psycopg2
import pg_simple
from flask_bcrypt import Bcrypt


# App start
app = Flask(__name__)
app.config.from_object(__name__)
bcrypt = Bcrypt(app)


# just a random mainpage
@app.route("/")
def itWorks():
    # with pg_simple.PgSimple() as db:
    #     pw = bcrypt.generate_password_hash('dddd')
    #     db.insert("users",
    #               {"name": 'adam',
    #                "password": pw,
    #                "api": '3'})
    #     db.commit()
    return "aXQgd29ya3Mh=="


# route to login page
@app.route("/login", methods=["POST", "GET"])
def login():
    # print session['username']
    if request.method == 'GET':
        # session.clear()
        return render_template('login.html')
    # Get username from form
    username = request.form['username']

    # Get password from db
    password = db.fetchone(userTable,
               fields=['password'],
               where=('name = %s', [username]))[0]
    try:
        if bcrypt.check_password_hash(password, request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('stats'))

    except TypeError as e:
        # Non-existent username
        pass
    except ValueError:
        # Wrong salt, so wrong password
        pass

    messages("401")
    return redirect(url_for('login'))


@app.route('/logout')
@loggedIn
def logout():
    session.clear()
    # TO DO: can access pages after logout with back button
    return redirect(url_for('login'))


# the API route to call from your script
@app.route("/api", methods=["POST"])
def getValues():
    # key = request.headers.get('api')
    record = Record(timestamp = request.json.get('timestamp'),
                    download = request.json.get('download'),
                    upload = request.json.get('upload'),
                    ping = request.json.get('ping'),
                    key = request.json.get('api'),
                    username = request.json.get('username'))

    print record.timestamp, record.download, record.upload, record.ping, record.key, record.username

    # speedData = [download, upload, ping]
    # save into the DB
    result = saveToDatabase(record)
    if result:
        return '',result
    else:
        return 404


# Funtion which saves the data
@validate
def saveToDatabase(record):
    # save to Postgres
    # insert into data values(1, (SELECT to_timestamp('07/08/2017,18:00:40',
    # 'DD-MM-YYYY,hh24:mi:ss')::timestamp without time zone),
    # 26.756, 23.4, 2.53);
    # try:
    with pg_simple.PgSimple() as db:
        # if user:
        db.insert("data",
                  {"datetime": record.timestamp,
                   "download": record.download,
                   "upload": record.upload,
                   "ping": record.ping,
                   "api": record.key})
        db.commit()
    return 201

@app.route("/stats")
@loggedIn
def stats():
    with pg_simple.PgSimple() as db:
        api = db.fetchone('users',
                           fields=['api'],
                           where=('name = %s', [session['username']]))[0]

        statistics = db.fetchall('data',
                                 fields=['datetime','download','upload','ping'],
                                 where=('api = %s', [api]),
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
                           ups = ups, downs = downs, pings = pings)


@app.route('/index')
@loggedIn
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # user = str(sys.argv[1])
    # passwd = str(sys.argv[2])
    app.secret_key = key_secret
    app.run(host='0.0.0.0', debug=True, port=80)
