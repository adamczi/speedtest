from functools import wraps
from flask import flash, redirect, url_for, session, request
import re
import time
from datetime import datetime, timedelta
from db import db
import pg_simple


# A class for storing data of each record request
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
    print(message) # This one is for debugging
    flash(message)


# Function to convert time from Postgres to JS-friendly format (UNIX time)
def dateToJS(date):
    return int(time.mktime(date.timetuple())) * 1000


# Decorator for data validation and parsing
def validate(func):
    def wrapper(*args):
        arg = args[0] # Get the Record object since wrapper acquires a tuple

        # Authentication: check if username exists and correct API key is
        # provided
        providedKey = arg.key
        username = arg.username
        try:
            with pg_simple.PgSimple() as db:
                key = db.fetchone('users',
                                   fields=['api'],
                                   where=('name = %s', [username]))[0][0] # delete the last zero once 24-char API keys are implemented
                latest = db.fetchone('data',
                                     fields=['datetime'],
                                     where=('api = %s', [key]),
                                     order=['datetime', 'DESC'])[0]
            if providedKey != key:
                return 401
                
        except TypeError:
            return 401


        # Parse datetime or completely reject request if incorrect (because
        # where would you place it on a graph?)
        try:
            d = datetime.strptime(arg.timestamp, '%Y-%m-%d,%H:%M:%S')
            if not isinstance(d,datetime):
                return 400
            if d-latest < timedelta(minutes=15):
                return 403
        except (ValueError, TypeError):
            return 400


        # The speed data validation
        # 0.0 values in case of an error will still indicate connection
        # and point out a client-side problem with speedtest visually on a graph

        # These ones are separate so in case one breaks the rest is still saved
        try:
            arg.download = float(re.findall('([0-9]+\.[0-9]+)', \
                                            arg.download)[0])
        except:
            arg.download = 0.0

        try:
            arg.upload = float(re.findall('([0-9]+\.[0-9]+)', arg.upload)[0])
        except:
            arg.upload = 0.0

        try:
            arg.ping = float(re.findall('([0-9]+\.[0-9]+)', arg.ping)[0])
        except:
            arg.ping = 0.0

        return func(arg)
    return wrapper


# Decorator for user authentication
def loggedIn(func):
    @wraps(func)
    def loginCheck(*args):
        if 'user' not in session:
            return redirect(url_for('login'))
        return func(*args)
    return loginCheck

def alreadyLogged(func):
    @wraps(func)
    def loginCheck(*args):
        if 'user' in session:
            return redirect(url_for('stats'))
        return func(*args)
    return loginCheck


# Decorator for user authentication when accessing user panel
# The panel is available only to current logged in user
def whoLoggedIn(func):
    @wraps(func)
    def loginCheck(username, *args):
        if 'username' not in session or username != session['username']:
            return redirect(url_for('stats'))
        return func(*args)
    return loginCheck
