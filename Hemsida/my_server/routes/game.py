
from my_server import app
from flask import render_template, abort, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from my_server.routes.dbhandler import create_connection
from my_server.routes.objects import Player, Field

socket = SocketIO(app)

@app.route('/play_game')
def test():
    return render_template('play_game.html')

@app.route('/play_game/<id>')
def play_game(id = None):
    if session['logged_in']:
        conn = create_connection()
        cur = conn.cursor()
        user = cur.execute("SELECT * FROM user WHERE username = ?", (session['username'], )).fetchone()
        level = cur.execute("SELECT * FROM level WHERE id = ?", (id, )).fetchone()
        field = Field(id)
        player = Player(user[1], level[3])
        host = True
        field.load_from_database()
        field.place_player(player, host)
        return render_template('play_game.html', player = player, field = field)
    abort(401)

@socket.on('join')
def on_join(data):
    join_room(data['room'])
    send_message_to_room({
        'heading': 'Info',
        'message': f'User {data["username"]} has joined the room.',
        'room': data['room']
    })

@socket.on('leave')
def on_leave(data):
    leave_room(data['room'])
    send_message_to_room({
        'heading': 'Info',
        'message': f'User {data["username"]} has left the room.',
        'room': data['room']
    })


@socket.on('send_message_to_room')
def send_message_to_room(data):
    emit('message_from_server', {
        'heading': data['heading'],
        'message': data['message']
    }, to=data['room'])

@app.route('/list_games')
def list_games():
    return render_template('list_game.html', username = session['username'])


@app.route('/edit-game')
def edit_game():
    return render_template('edit_game.html')


