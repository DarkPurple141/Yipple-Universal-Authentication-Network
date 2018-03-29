from flask import Flask, render_template_string, request, render_template, \
    redirect, url_for, session
from flask_session import Session

from . import app
from .. import models
import os

def isAuthenticated(user):
    return 'username' in session and session['username'] == user

def prepDBQuery():
    update = {}
    for key in request.form:
        update[key] = request.form.get(key)

    return update

@app.route('/')
def home():
    username = None
    if 'username' in session:
        username = session['username']
    return render_template("home.html", username=username)

@app.route('/login', methods=["GET", "POST"])
def login():
    username = None
    password = None

    if request.method == "POST":
        # Implement me
        if 'username' in request.form:
            username = request.form.get('username')

        if 'password' in request.form:
            password = request.form.get('password')

        if username is not None and password is not None:

            succ, sess = models.validateUser(username, password)

            if succ is True:
                session['username'] = request.form.get('username')

                # Craft the session
                return redirect('/')
            else:
                return "Login request failed", 400
        else:

            return "login request received", 400

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("basic.home"))

@app.route('/register', methods=["GET", "POST"])
def register():
    username = None
    password = None
    result = False

    if request.method == "POST":
        if 'username' in request.form:
            username = request.form.get('username')

        if 'password' in request.form:
            password = request.form.get('password')

        if username is not None and password is not None:
            succ, status = models.registerUser(username, password)

            if succ is not False:
                return status, 200
            else:
                return status, 400
        return "User registration failed, either username or password is empty.", 400

    return render_template("register.html")

@app.route('/users/<account>', methods=["GET", "POST"])
def users(account):

    if account == 'me':
        if 'username' in session:
            username = session['username']
            # valid me session
            query = models.searchDB(username) # no check req'd.
            response = render_template("users.html", username=username, query=query, search=username)
        else:
            response = render_template("users.html", username=None), 403
    else:
        if not isAuthenticated(account) and not isAuthenticated('admin'):
            return render_template('error_page.html'), 403

        username = account
        loggedin = session['username']
        # trying to access account if here user is auth'd
        if request.method == 'GET':
            query = models.searchDB(username)
            response = render_template("users.html", username=loggedin, query=query, search=username)
        elif request.method == 'POST':
            update = prepDBQuery()
            models.updateDB(update, username)
            response = render_template("users.html", username=username, query=username, search=username)

    return response

@app.route('/admin', methods=["GET", "POST"])
def admin():
    response = None
    if not isAuthenticated('admin'):
        return render_template('error_page.html'), 403

    searchedUser = request.args.get('search')

    if request.method == 'GET':
        # The administration panel must distinguish between users that are administrators
        # as well as regular users.
        # It should also be able to search for a user via a get parameter called user.
        query = None

        if searchedUser:
            query = models.searchDB(searchedUser)

        response = render_template("admin.html", query=query, username="admin", search=searchedUser)

    elif request.method == 'POST':

        update = prepDBQuery()

        models.updateDB(update, searchedUser)

        response = render_template("admin.html", query=update, username="admin", search=searchedUser)

    return response
