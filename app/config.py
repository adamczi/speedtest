import os

SECRET_KEY = os.urandom(24)
DEBUG = True
# THREADS_PER_PAGE = 2
# CSRF_ENABLED = True
# CSRF_SESSION_KEY = "secret"

# Database
host = '172.17.0.2'
port = '5432'
database = 'speed'
userTable = 'users'
dataTable = 'data'
