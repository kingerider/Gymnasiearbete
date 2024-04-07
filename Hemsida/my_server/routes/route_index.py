from my_server import app
from flask import render_template, session

@app.route('/')
@app.route('/index')
def index():
    session['logged_in'] = False
    return render_template('index.html')