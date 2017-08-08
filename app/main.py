from flask import Flask, render_template, send_file
from config import key_secret
import re
import psycopg2
from datetime import datetime


## App start
app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/")
# just a random mainpage
def itWorks():
    return "It works!"


@app.route("/record/<speedData>")
# is the API route to call from your script
def getValues(speedData):
    # parse the values
    values = re.findall('([0-9]+\.[0-9]+)',speedData)
    createGraph(values)

    # save into the DB
    saveToDatabase(values)

    # immediately load new up to date values
    loadToGraph()

    return "It works!"


def createGraph(speedData):
    with open("report.txt", "a") as f:
        f.write(str(datetime.now())+';'+';'.join(speedData)+'\n')
    print '\nThe time is',datetime.now()
    print 'Current data is:',speedData,'\n'
    return


def saveToDatabase(speedData):
    # save to Postgres
    return


def loadToGraph():
    # load from postgres, jsonify and pass to html
    return


@app.route('/index')
# is where the graph shows up
def index():
    return send_file('./static/index.html')

if __name__ == '__main__':
    app.secret_key = key_secret
    app.run(host='0.0.0.0', debug=True, port=80)
