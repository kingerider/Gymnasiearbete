from my_server import app
from flask import render_template

@app.route('/play_game')
def play_game():
    return render_template('play_game.html')