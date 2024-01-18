
from my_server import app
from flask import render_template, abort, session
from flask_socketio import SocketIO
from my_server.routes.dbhandler import create_connection
from my_server.routes.objects import Player, Field

socket = SocketIO(app)



@app.route('/play_game/<id>')
def play_game(id = None):
    if session['logged_in']:
        conn = create_connection()
        cur = conn.cursor()
        user = cur.execute("SELECT * FROM user WHERE username = ?", (session['username'], )).fetchone()
        level = cur.execute("SELECT * FROM level WHERE id = ?", (id, )).fetchone()
        field = Field(id)
        field.load_from_database()
        player = Player(user[1], level[3])
        return render_template('play_game.html', player = player, field = field)
    abort(401)


@app.route('/edit-game')
def edit_game():
    return render_template('edit_game.html')


