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

    data = komrade.read()

    # if user already exists do x
    if username in data:
        return 400 # ????
    # else proceed as normal for valid registration
    else:
        """
        try:
            data[username] = {
                'password': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                'id'      : uuid.uuid4()
            }
        except Exception as e:
            print(e)
        """
        data[username] = {
            'password': password,
            'id'      : str(uuid.uuid4())
        }
        komrade.write(data)

    return 200


def validateUser(username, password):
    """
    Checks whether {username} is valid.
    pw_hash = bcrypt.generate_password_hash(‘hunter2’).decode(‘utf-8’)
    bcrypt.check_password_hash(pw_hash, 'hunter2')
    """
    komrade = KomradeConfig("user")
    data = komrade.read()
    # bcrypt.checkpw('Jeff'.encode('utf-8'),)

    if username in data and data[username]['password'] == password:
        return True

    return False
