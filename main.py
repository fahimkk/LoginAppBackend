from flask import Flask, request
import sqlite3
import json

app = Flask(__name__)


def statusJson(status, username=False):
    status_dict = {"status": status}
    if username:
        status_dict["username"] = username
    status_json = json.dumps(status_dict)
    print(status_json)
    return status_json


def addData(username, email, password):
    try:
        conn = sqlite3.connect('loginapp.db')
        c = conn.cursor()
        # check whether the user already signed up or not
        c.execute("select * from credentials where email='{}'".format(email))
        conn.commit()
        exists = c.fetchall()
        if exists:
            return statusJson("exists")
        c.execute("insert into credentials values ('{}','{}','{}')".format(
            username, email, password))
        conn.commit()
        conn.close()
    except Exception as err:
        print("Connecting Database Error: ", err)
        return statusJson("dbError")
    else:
        print("Adding Data Successful")
        return statusJson("success")


def verifyData(email, password):
    try:
        print('verify data')
        print(email, password)
        conn = sqlite3.connect('loginapp.db')
        c = conn.cursor()
        c.execute("SELECT * FROM credentials WHERE email='{}'".format(email))
        conn.commit()
        tup = c.fetchone()
        conn.close()
        print(tup)
    except Exception as err:
        print("Connecting Database Error: ", err)
        return statusJson("dbError")
    else:
        if not tup:
            # Empty tuple- no records found
            print('Please Sign UP')
            return statusJson("nil")
        print('Checking Database')
        # Records found- Compare passwords
        db_password = tup[2]
        if db_password != password:
            print('incorrect password')
            return statusJson("incorrect")
        # Password matches - Return Status and Username
        print("success")
        username = tup[0]
        return statusJson("success", username=username)


@app.route('/', methods=['POST', 'GET'])
def signIn():
    print('Sing in')
    if request.method == 'POST':
        # if data sent as json, ie application/json, the we can't get it
        # by using request.form, we have to use either .data or .get_json()
        # get_json will return a dict
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        print(email, password)
        return verifyData(email, password)


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    print('Welcome to SignUp')
    if request.method == 'POST':
        # if data sent as json, ie application/json, the we can't get it
        # by using request.form, we have to use either .data or .get_json()
        # get_json will return a dict
        data = request.get_json()
        username = data["username"]
        email = data["email"]
        password = data["password"]
        print(email, password)
        return addData(username, email, password)


if __name__ == '__main__':
    app.run(debug=True)
