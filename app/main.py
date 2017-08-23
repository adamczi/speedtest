# import sys

# parsing values from DB
import json
import datetime
from decimal import *

from flask import Flask, render_template, session, send_file, url_for, \
request, abort, redirect
from config import key_secret, userTable
from utils import messages, validate, loggedIn, dateToJS
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
@app.route("/record/<timestamp>/<speedData>")
def getValues(timestamp, speedData):
    key = request.headers.get('api')
    # key = '1'
    # save into the DB
    print timestamp
    print speedData
    result = saveToDatabase(timestamp, speedData, key)
    if result:
        return "thanks "+result+"!"
    else:
        return '401'


# Funtion which saves the data
@validate
def saveToDatabase(timestamp, speedData, key):
    # save to Postgres
    # insert into data values(1, (SELECT to_timestamp('07/08/2017,18:00:40',
    # 'DD-MM-YYYY,hh24:mi:ss')::timestamp without time zone),
    # 26.756, 23.4, 2.53);
    with pg_simple.PgSimple() as db:
        user = db.fetchone('users',
                           fields=['name'],
                           where=('api = %s', [key]))[0]
        if user:
            db.insert("data",
                      {"datetime": timestamp,
                       "download": float(speedData[0]),
                       "upload": float(speedData[1]),
                       "ping": float(speedData[2]),
                       "api": key})
            db.commit()
        return user


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

    # messages(statistics)

    # Convert the dump to JS-friendly format
    ups = []
    downs = []
    pings = []
    for record in statistics:
        date = dateToJS(record[0]) # TO DO: timezone
        down = float(record[1])
        up = float(record[2])
        pi = float(record[3])

        # Three different series of data
        downs.append([date, down])
        ups.append([date, up])
        pings.append([date, pi])

    return render_template('stats.html', ups = ups, downs = downs, pings = pings)


@app.route('/index')
@loggedIn
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # user = str(sys.argv[1])
    # passwd = str(sys.argv[2])
    app.secret_key = key_secret
    app.run(host='0.0.0.0', debug=True, port=80)
