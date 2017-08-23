from functools import wraps
from flask import flash, redirect, url_for, session, request
import re
import time
# from config import userTable
# from db import db

# Function for message flashing
def messages(message):
    print(message)
    flash(message)
    return


# Decorator for data validation and parsing
def validate(func):
    def wrapper(*args):
        values = re.findall('(\.*[0-9]+\.[0-9]+)', args[1])
        for i in xrange(3):
            values[i] = values[i][1:] if values[i].startswith('.') else values[i]
        return func(args[0], values, args[2])
    return wrapper


# Decorator for user authentication
def loggedIn(func):
    @wraps(func)
    def loginCheck(*args):
        if 'username' not in session:
            return redirect(url_for('login'))
        return func(*args)
    return loginCheck

def dateToJS(date):
    """Converts a datetime object to the number of milliseconds since the unix epoch."""
    return int(time.mktime(date.timetuple())) * 1000
