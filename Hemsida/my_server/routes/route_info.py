from my_server import app
from flask import render_template, session

@app.route('/info')
def info():
    return render_template('info.html')