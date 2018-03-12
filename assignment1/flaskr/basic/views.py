from flask import render_template_string, request, render_template,\
 redirect, url_for, session
from . import app
from .. import models

def getFormData(request):
    data = request.form
    user = data.get('username')
    pw = data.get('password')

    return user, pw

@app.route('/')
def home():
    return render_template("home.html")

"""
- On successful login, you should:
    - Store the logged in username in `session['username']`
    - Redirect to `/users/me`
- On unsuccessful login, you should:
    - Display a 403
"""
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # TODO
        user, pw = getFormData(request)

        if user and pw and models.validateUser(user, pw):
            session['username'] = user
            return redirect('/users/{}'.format(user))
        else:
            return "You shall not pass.", 403

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("basic.home"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            user, pw = getFormData(request)

            if user and pw:
                if models.registerUser(user, pw) == 200:
                    return redirect('/login')
                else:
                    return "Username is taken, Soz.", 400
        except Exception as e:
            return "Server Error", 500

    # occurs if get request
    return render_template("register.html")

@app.route('/users/<account>')
def users(account):
    # TODO
    if 'username' not in session and not session['username']:
        return 400
    return render_template("users.html", account=session['username'])
