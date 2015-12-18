#!/usr/bin/python

from flask import Flask, render_template, request, json
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        if _name and _email and _password:
            conn = mysql.connect()
            cr = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cr.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cr.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message': 'User created successfully!'})
        else:
            return json.dumps({'error': str(data[0])})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cr.close()
        conn.close()

if __name__ == "__main__":
    app.run()
