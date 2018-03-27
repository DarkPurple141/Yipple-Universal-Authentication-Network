from flask import Flask, render_template_string, request, render_template, \
    redirect, url_for, session
from flask_session import Session

from . import app
from .. import models
import os

def isAuthenticated(user):
    return 'username' in session and session['username'] == user

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
    username = account
    if not isAuthenticated(username) and not isAuthenticated('admin'):
        return render_template('error_page.html'), 404

    if username == 'me':
        if 'username' in session:
            username = session['username']
            # valid me session
            query = models.searchDB(username) # no check req'd.
            return render_template("users.html", username=username, query=query, search=username)
        else:
            return render_template("users.html", username=None), 403


    # TODO: Implement the ability to edit and view credentials for
    # the creds database.
    if request.method == 'GET':
        # TODO: Display credentials if user belongs to current session, or if user is admin.
        # Deny access otherwise and display '404 not found' on the page
        response = render_template("users.html", username=username, query=username, search=username)
    else:
        # POST
        # TODO: Update The Credentials
        # Two types of users can edit credentials for <account>
        # 1. Regular Users that have sessions == <account>
        # 2. Administrators.
        response = render_template("users.html", username=username, query=username, search=username)

    return response

@app.route('/admin', methods=["GET", "POST"])
def admin():
    response = None
    if not isAuthenticated('admin'):
        return render_template('error_page.html'), 403

    searchedUser = request.args.get('user')

    if request.method == 'GET':
        # The administration panel must distinguish between users that are administrators
        # as well as regular users.
        # It should also be able to search for a user via a get parameter called user.
        query = None

        if searchedUser:
            query = models.searchDB(searchedUser)

        response = render_template("admin.html", query=query, username="admin", search=searchedUser)

    elif request.method == 'POST':
        # TODO: You must also implement a post method in order update a searched users credentials.
        # It must return a page that denies a regular user
        # access and display '403 permission denied'
        update = {}
        for key in request.form:
            update[key] = request.form.get(key)

        models.updateDB(update, searchedUser)

        response = render_template("admin.html", query=update, username="admin", search=searchedUser)

    return response
