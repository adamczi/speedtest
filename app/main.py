# import sys
from flask import Flask, render_template, session, send_file, url_for, \
request, abort, redirect
from config import key_secret, userTable
from utils import messages, validate, loggedIn
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
    #     db.insert("users",
    #               {"name": 'marcin',
    #                "password": 'asdf',
    #                "api": '1'})
    #     db.commit()
    return "aXQgd29ya3Mh=="


# route to login page
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    # Get username from form
    username = request.form['username']

    # Get password from db
    password = db.fetchone(userTable,
               fields=['password'],
               where=('name = %s', [username]))[0]
    try:
        # if bcrypt.check_password_hash(password, request.form['password']):
        if password == request.form['password']:
            session['username'] = request.form['username']
            return redirect(url_for('stats'))

    except TypeError as e:
       pass

    messages("401")
    return redirect(url_for('login'))


@app.route('/logout')
@loggedIn
def logout():
    session.clear()
    return 'Logged out'


# the API route to call from your script
@app.route("/record/<timestamp>/<speedData>")
def getValues(timestamp, speedData):

    # save into the DB
    saveToDatabase(timestamp, speedData)

    return "it works!"


# Funtion which saves the data
@validate
def saveToDatabase(timestamp, speedData):
    # save to Postgres
    # insert into data values(1, (SELECT to_timestamp('07/08/2017,18:00:40',
    # 'DD-MM-YYYY,hh24:mi:ss')::timestamp without time zone),
    # 26.756, 23.4, 2.53);

    with pg_simple.PgSimple() as db:
        db.insert("data",
                  {"date": timestamp,
                   "download": float(speedData[0]),
                   "upload": float(speedData[1]),
                   "ping": float(speedData[2])})
        db.commit()
    return


@app.route("/stats")
@loggedIn
def stats():
    return render_template('stats.html')


@app.route('/index')
@loggedIn
def index():
    return send_file('./static/index.html')

if __name__ == '__main__':
    # user = str(sys.argv[1])
    # passwd = str(sys.argv[2])
    app.secret_key = key_secret
    app.run(host='0.0.0.0', debug=True, port=80)
