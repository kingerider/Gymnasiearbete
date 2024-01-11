from my_server import app
from flask import render_template, redirect, url_for, flash, request, session
from my_server.routes.forms import RegistrationForm
from my_server.routes.dbhandler import create_connection
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        conn = create_connection()
        cur = conn.cursor()
        user = cur.execute("SELECT * FROM users WHERE namn = ?", (username, )).fetchone()

        if bcrypt.check_password_hash(user[2], password):
            session['logged_in'] = True
            session['username'] = username
            session['user'] = user
            flash(f"Välkommen {session['username']}", "success")
            conn.close()
            return redirect(url_for('member_area'))
        conn.close()
    return render_template('login.html', form = form)
        
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    session.pop('author_id', None)
    flash('Du loggades ut', 'success')
    return redirect(url_for('index'))