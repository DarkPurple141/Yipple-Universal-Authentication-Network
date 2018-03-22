import os
import json
import bcrypt
import uuid
from . import db

def searchDB(username):
    result = None
    query = db.queryDB('SELECT name, address, email, phonenum, funds FROM creds \
                       JOIN users WHERE username = ?', [username], one=True)

    if query:
        result = {
            'name':       query[0],
            'address':    query[1],
            'email':      query[2],
            'phone':      query[3],
            'funds':      query[4]
        }

    return result


def registerUser(username, password):
    isSuccess = False

    # Check input lengths
    if len(username) == 0 or len(password) == 0:
        return (isSuccess, 'Invalid username or password length')

    # Check username uniqueness
    res = db.queryDB('SELECT * FROM users WHERE username = ?', [username], one=True)
    if res is not None:
        # User already exists inside the database
        return (isSuccess, 'The supplied username is already in use')
    else:
        # Registration successful
        db.insertDB('INSERT INTO users (username, passhash) values (?, ?)', (username, password))
        isSuccess = True
    return (isSuccess, 'Registration successful')

# Returns tuple of (success, session)
# Session is the username in this case.
def validateUser(username, password):
    isSuccess = False

    if len(username) == 0 or len(password) == 0:
        return (isSuccess, None)

    res = db.queryDB('SELECT * FROM users WHERE username = ?', [username], one=True)

    if res is not None:
        if res[2] == password:
            # Login succeeded
            isSuccess = True
            return (isSuccess, username)
        return (isSuccess, username)

    return (isSuccess, None)
