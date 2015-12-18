#!/usr/bin/python

from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

conn = mysql.connect()
cr = conn.cursor()


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    _hashed_password = generate_password_hash(_password)
    cr.callproc('sp_createUser', (_name, _email, _hashed_password))
    data = cr.fetchall()

    if len(data) is 0:
        conn.commit()
        return json.dumps({'message': 'User created successfully!'})
    else:
        return json.dumps({'error': str(data[0])})


if __name__ == "__main__":
    app.run()
