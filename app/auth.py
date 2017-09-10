from flask import Blueprint, render_template, session, request, redirect, \
current_app, url_for
from flask_bcrypt import Bcrypt
from utils import alreadyLogged, messages, loggedIn
from db import db
from config import userTable

authentication = Blueprint('authentication',
                           __name__,
                           template_folder='templates/authentication')

# Route to login page
@authentication.route("/login", methods=["POST", "GET"])
@alreadyLogged
def login():
    bcrypt = Bcrypt(current_app)

    if request.method == 'GET':
        return render_template('login.html')

    # Get username from form
    username = request.form['username']

    # Get authentication details
    auths = db.fetchone(userTable,
               fields=['password', 'api'],
               where=('name = %s', [username]))

    try: # Check password salt
        if bcrypt.check_password_hash(auths.password, request.form['password']):
            session['user'] = auths.api # API key in session
            session['username'] = username # username in session
            return redirect(url_for('stats'))

    except (ValueError, TypeError, AttributeError) as e:
        # Non-existent username
        pass

    messages("401")
    return redirect(url_for('authentication.login'))


# Clear session after logout
@authentication.route('/logout')
@loggedIn
def logout():
    session.clear()
    messages("200")
    return redirect(url_for('authentication.login'))


@authentication.route('/')
@loggedIn
def passwordChange():
    bcrypt = Bcrypt(current_app)
    
    if request.method == 'POST': # means someone wants to change password:
        with pg_simple.PgSimple() as db:
            # Fetch current password
            auth = db.fetchone(userTable,
                       fields=['password'],
                       where=('name = %s', [session['username']]))
            # If correct, generate hash for new one and update DB
            if bcrypt.check_password_hash(auth.password,
                                          request.form['oldPassword']):
                np = bcrypt.generate_password_hash(request.form['newPassword'])
                db.update(userTable,
                          data={'password': np},
                          where=('name = %s', [session['username']]))
                db.commit()
                messages('200')
            else: # Invalid old password (hashes mismatch)
                messages('401')
        return redirect(url_for('userPanel'))
