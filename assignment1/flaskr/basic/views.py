from flask import render_template_string, request, render_template, redirect, url_for, session
from . import app
from .. import models

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO
        user = request.form.get('username')
        pw   = request.form.get('password')
        print(user, pw)
        session['username'] = request.data
        return "login request received", 400

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()

    return redirect(url_for("basic.home"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # TODO
        print (request.data)
        data = request.body
        user = data.username
        pw = data.password

        if user and pw:
            if registerUser(user, pw) == 200:
                return redirect('/login')
            else:
                return "Username is taken, Soz.", 400

        return "Registration Error occurred", 500

    return render_template("register.html")

@app.route('/users/<account>')
def users(account):
    # TODO
    if 'user' not in session:
        return 400
    return render_template("users.html", account=account)
