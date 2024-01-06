from my_server import app
from flask import render_template, request, redirect, url_for, abort, flash
from my_server.databasehandler import create_connection
import json


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and  request.form['sort_name'] != '':
        sort_name = request.form['sort_name']
        sql = f'SELECT * FROM users WHERE name LIKE "{sort_name}%"'
    else:
        sql = 'SELECT * FROM users'
    conn = create_connection()
    cur = conn.cursor()
    #user = cur.execute(sql).fetchone()
    #print(user)
    users = cur.execute(sql).fetchall()
    conn.close()

    return render_template('index.html', users = users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        name = request.form['name']
        password = request.form['password']
            
        conn = create_connection()
        cur = conn.cursor()

        sql = f'SELECT id FROM users WHERE name = "{name}" AND password = {password}'
        id = cur.execute(sql).fetchone()
        print(id)
        print('Hello')
        print('Helloo')
        conn.close()
        return redirect(url_for('memberarea', id = id))
    else:
        return render_template('login.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        conn = create_connection()
        cur = conn.cursor()
        sql = 'INSERT INTO users (name, password) VALUES (?, ?)'
        cur.execute (sql, (name, password))
        conn.commit()

        sql = 'SELECT MAX(id) FROM users'
        id = cur.execute(sql).fetchone()[0]
        print(id)
        print('Hello')
        print('Hello')
        conn.close()
        
        return redirect(url_for('memberarea', id = id))
    else:
        return render_template('sign_up.html')


@app.route('/memberarea/<id>', methods=['GET', 'POST'])
def memberarea(id = None):
    conn = create_connection()
    cur = conn.cursor()
    sql = 'SELECT * FROM users'
    users = cur.execute(sql).fetchall()
    conn.close
    flash('You are now logged in', category='info')

    return render_template('memberarea.html', users = users, id = id)


@app.route('/user/exist', methods=['GET', 'POST'])
def user_exist():
    print("create user_exist")
    person = request.get_json()
    print(person['name'])
    print(person)
    print(person)
    print(person)

    conn = create_connection()
    cur = conn.cursor()
    sql = 'SELECT * FROM users'
    users = cur.execute(sql).fetchall()

    create_user = True
    for user in users:
        if person['name'] == user[1] and person['password'] == user[2]:
            create_user = False

    conn.close()


    if create_user:
        pass
        print("hello")
        print("hello")
        return json.dumps({
            'msg' : 'User added succesfully',
            'success' : True
        })
    else:
        print("hello")
        print("hello")
        print("hello")
        print("hello")

        return json.dumps({
            'msg' : 'Error, user already exists',
            'success' : False
        })

@app.errorhandler(404)
def not_found_error(error):
	return render_template('errors/404.html'), 404

@app.errorhandler(401)
def not_found_error(error):
	return render_template('errors/401.html'), 401

    