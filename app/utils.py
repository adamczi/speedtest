from functools import wraps
from flask import flash, redirect, url_for, session, request
import re
import time
from datetime import datetime
# from config import userTable
# from db import db

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

        arguments = list(args)

        try:
            # parse datetime and check api key length
            d = datetime.strptime(arguments[0], '%Y-%m-%d,%H:%M:%S')
            if not isinstance(d,datetime) or len(arguments[2]) != 24:
                return 400

        except (ValueError, TypeError):
            return 400

        try:
            # parse up/down/ping values to a list of three
            # this is separate in case of error in speedtest - 0,0,0 values
            # will still indicate connection and will point out a problem
            arguments[1] = re.findall('(*[0-9]+\.[0-9]+)', arguments[1])
            arguments[1].extend([0] * (3 - len(arguments[1])))
            arguments[1] = arguments[1][:3]
        except:
            arguments[1] = [0.0,0.0,0.0]

        return func(*arguments)
    return wrapper


# Decorator for user authentication
def loggedIn(func):
    @wraps(func)
    def loginCheck(*args):
        if 'username' not in session:
            return redirect(url_for('login'))
        return func(*args)
    return loginCheck
