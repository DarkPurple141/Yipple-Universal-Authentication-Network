#!/usr/bin/env python

import os
import json
import bcrypt
import uuid

class KomradeConfig:
    def __init__(self, name):
        self.config_file = os.path.join(os.path.dirname(__file__), "../" + name + ".json")

        if not os.path.exists(self.config_file):
            open(self.config_file, "w").write("{}")

    def read(self):
        return json.loads(open(self.config_file, "r").read())

    def write(self, data):
        with open(self.config_file, 'w') as fh:
            fh.write(json.dumps(data))


def registerUser(username, password):
    """
    - On successful registration, you should:
        - Redirect to the login page
    - On unsuccessful registration, you should:
        - Notify the user that username is taken with a 400 return code if that is the case
        - Notify the user of a general failure with a 500 return code
    """
    komrade = KomradeConfig("user")

    # Implement me

    data = komrade.read()

    # if user already exists do x
    if username in data:
        return 400 # ????
    # else proceed as normal for valid registration
    else:
        data[username] = {
            'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            'id'      : str(uuid.uuid4())
        }
        komrade.write(data)

    return 200


def validateUser(username, password):
    """
    Checks whether {username} is valid.
    """
    komrade = KomradeConfig("user")
    data = komrade.read()

    if username not in data:
        return False

    # Implement me

    return bcrypt.hashpw(password.encode('utf-8'), stored_pw) == stored_pw
