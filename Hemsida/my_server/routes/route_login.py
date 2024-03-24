from my_server import app
from flask import render_template, redirect, url_for, flash, session
from my_server.routes.dbhandler import create_connection
from my_server.routes.forms import LoginForm
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()


    #https://hyperskill.org/learn/step/27151
    #https://popsql.com/learn-sql/sql-server/how-to-query-date-and-time-in-sql-server
    #UPDATE level SET date = (SELECT date("now")) WHERE date = 0

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data.encode('utf-8')
        conn = create_connection()
        cur = conn.cursor()
        try:
            user = cur.execute("SELECT * FROM user WHERE username = ?", (username, )).fetchone()
            time = cur.execute("SELECT datetime('now')").fetchone
            print("hello: ")
            print(time)

            if bcrypt.check_password_hash(user[2], password):
                session['logged_in'] = True
                session['username'] = user[1]
                session['id'] = user[0]
                flash(f"Välkommen {session['username']}", "success")
                conn.close()
                return redirect(url_for('memberarea'))
            conn.close()
        except:
            flash("username not found", "warning")
    return render_template('login.html', form = form)
        
@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    session.pop('author_id', None)
    flash('Du loggades ut', 'success')
    return redirect(url_for('index'))