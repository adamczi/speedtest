import sys
from flask import Flask, render_template, send_file, flash, session, url_for
from config import key_secret
from models import pool
import re
import psycopg2, pg_simple
from datetime import datetime


## App start
app = Flask(__name__)
app.config.from_object(__name__)

# Function for message flashing
def messages(message):
    print(message)
    flash(message)
    return

# Wrapper for data validation and parsing
def validate(func):
    def wrapper(*args):
        # try:
        values = re.findall('(\.*[0-9]+\.[0-9]+)',args[1])
        for i in xrange(3):
            values[i] = values[i][1:] if values[i].startswith('.') else values[i]
        # except Exception as e:
        return func(args[0],values)
    return wrapper


# just a random mainpage
@app.route("/")
def itWorks():
    return "aXQgd29ya3Mh=="


# route to login page
@app.route("/login")
def login():
    return render_template('login.html')

# @app.route("/postlogin", methods=["GET", "POST"])
# def postlogin():
#     if request.method = "POST":


# the API route to call from your script
@app.route("/record/<timestamp>/<speedData>")
def getValues(timestamp, speedData):
    # parse the values

    # createGraph(speedData)

    # save into the DB
    saveToDatabase(timestamp, speedData)

    # immediately load new up to date values
    # loadToGraph()

    return "It works!"


# Funtion which saves the data
@validate
def saveToDatabase(timestamp, speedData):
    # save to Postgres
    # insert into data values(1, (SELECT to_timestamp('07/08/2017,18:00:40', 'DD-MM-YYYY,hh24:mi:ss')::timestamp without time zone), 26.756, 23.4, 2.53);
    print timestamp
    print speedData
    with pg_simple.PgSimple() as db:
        db.insert("data",
                  {"date": timestamp,
                   "download": float(speedData[0]),
                   "upload": float(speedData[1]),
                   "ping": float(speedData[2])})
        db.commit()
    return

# Function which loads data for given user and passes it to draw the graph
def loadToGraph():
    # load from postgres, jsonify and pass to html
    return

# random graph shows up here
@app.route('/index')
def index():
    return send_file('./static/index.html')

if __name__ == '__main__':
    # user = str(sys.argv[1])
    # passwd = str(sys.argv[2])
    app.secret_key = key_secret
    app.run(host='0.0.0.0', debug=True, port=80)
