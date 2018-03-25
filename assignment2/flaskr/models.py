import os
import json
import bcrypt
import uuid
from . import db

validfields = ['name','address','email','phonenum','funds']

def searchDB(username):
    result = None
    username = '%' + username + '%'
    query = db.queryDB('SELECT name, address, email, phonenum, funds FROM users \
                       NATURAL JOIN creds WHERE username LIKE ?', [username], one=True)
    if query:
        for index, field in enumerate(validfields):
            result[field] = query[index]

    return result

def updateDB(field, value, user=None):
    if user and field in validfields:
        db.insertDB('UPDATE credentials SET ? = ? WHERE username = ?', (field, value, user))

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
