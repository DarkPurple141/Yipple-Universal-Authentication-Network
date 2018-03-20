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
    if 'username' in session:
        return redirect(url_for("basic.users", account="me"))

    if request.method == "POST":
<<<<<<< HEAD
        # TODO
        user, pw = getFormData(request)

        if user and pw and models.validateUser(user, pw):
            session['username'] = user
            return redirect('/users/me') # {}'.format(user))
        else:
            return "You shall not pass.", 403
=======
        if not all(x in request.form for x in ["username", "password"]):
            return "Bad request", 400

        if not models.validateUser(request.form['username'], request.form['password']):
            return "Incorrect username and/or password, try again.", 403

        session['username'] = request.form['username']

        return redirect(url_for("basic.users", account="me"))
>>>>>>> 1f60d8aa29eb47065190f8c5fd225cd2e26063b4

    return render_template("login.html")

@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("basic.home"))

@app.route('/register', methods=["GET", "POST"])
def register():
<<<<<<< HEAD
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
=======
    if 'username' in session:
        return redirect(url_for("basic.users", account="me"))

    if request.method == "POST":
        if not all(x in request.form for x in ["username", "password"]):
            return "Bad request", 400

        try:
            models.registerUser(request.form['username'], request.form['password'])
        except NameError as e:
            return "User already exists, try again.", 400
        except Exception as e:
            print(e)
            return "We encountered a problem handling your request, try again later.", 500

        return redirect(url_for("basic.login"))
>>>>>>> 1f60d8aa29eb47065190f8c5fd225cd2e26063b4
    return render_template("register.html")

@app.route('/users/<account>')
def users(account):
<<<<<<< HEAD
    # TODO
    if 'username' not in session and not session['username']:
        return 400
    return render_template("users.html", account=session['username'])

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404
=======
    if 'username' not in session:
        return redirect(url_for("basic.login"))
    
    return render_template("users.html", account=session['username'])
>>>>>>> 1f60d8aa29eb47065190f8c5fd225cd2e26063b4
