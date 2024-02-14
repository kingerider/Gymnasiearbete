from my_server import app
from flask import render_template, redirect, url_for, flash, request, session
from my_server.routes.forms import SignUpForm
from my_server.routes.dbhandler import create_connection
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data.encode('utf-8')
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, bcrypt.generate_password_hash(password)))
        conn.commit()
        session['logged_in'] = True
        session['username'] = username
        flash(f"Välkommen {session['username']}", "success")
        conn.close()
        return redirect(url_for('index'))
    return render_template('sign_up.html', form = form)
        