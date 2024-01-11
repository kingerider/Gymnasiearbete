from my_server import app
from flask import render_template, session

@app.route('/memberarea')
def memberarea():
    if session['logged_in']:
        return render_template('memberarea.html')