from functools import wraps
from flask import flash, redirect, url_for, session, request
import re
import time
from datetime import datetime
from db import db
import pg_simple
# from config import userTable
# from db import db

class Record:
    def __init__(self, key, username, timestamp, download = 0.0, upload = 0.0, \
                 ping = 0.00,):
        self.timestamp = timestamp
        self.download = download
        self.upload = upload
        self.ping = ping
        self.key = str(key)
        self.username = str(username)


# Function for message flashing
def messages(message):
    print(message) # for debugging
    flash(message)

# Function to convert time from Postgres to JS-friendly format (unix time)
def dateToJS(date):
    return int(time.mktime(date.timetuple())) * 1000

# Decorator for data validation and parsing
def validate(func):
    def wrapper(*args):
        arg = args[0]


        # Parse datetime or reject if incorrect (where to place it on a graph?)
        try:
            d = datetime.strptime(arg.timestamp, '%Y-%m-%d,%H:%M:%S')
            if not isinstance(d,datetime):
                return 400
        except (ValueError, TypeError):
            return 400


        # Authentication: check if username exists and correct API key is
        # provided
        providedKey = arg.key
        username = arg.username

        try:
            with pg_simple.PgSimple() as db:
                key = db.fetchone('users',
                                   fields=['api'],
                                   where=('name = %s', [username]))[0][0] # delete the last zero once 24-char API keys are implemented

            if providedKey != key:
                return 401
        except TypeError:
            return 401


        # The speed data validation
        try:
            # 0.0 values in case of an error will still indicate connection
            # and will point out a client-side problem visually on a graph
            # arguments[1][i] = re.findall('([0-9]+\.[0-9]+)', \
            #                              arguments[1][i])
            arg.download = float(re.findall('([0-9]+\.[0-9]+)', arg.download)[0])

            arg.upload = float(re.findall('([0-9]+\.[0-9]+)', arg.upload)[0])

            arg.ping = float(re.findall('([0-9]+\.[0-9]+)', arg.ping)[0])

        except:
            arg.download = arg.upload = arg.ping = 0.0

        return func(arg)
    return wrapper


# Decorator for user authentication
def loggedIn(func):
    @wraps(func)
    def loginCheck(*args):
        if 'username' not in session:
            return redirect(url_for('login'))
        return func(*args)
    return loginCheck
