
from my_server import app
from flask import render_template, abort, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from my_server.routes.dbhandler import create_connection
from my_server.routes.objects import Game, Player, Field

socket = SocketIO(app)

ongoing_games = []

#kollar alla id på varje spel och lägger till max + 1 som nytt id, får tillbaka 0 om listan är tom
def set_room_id():
    list_of_roomid = []
    for game in ongoing_games:
        if game.room_id != None:
            list_of_roomid.append(game.room_id)
    if len(list_of_roomid) == 0:
        return 0
    max = list_of_roomid[0]
    for roomid in list_of_roomid:
        if roomid > max:
            max = roomid
    return max + 1



@app.route('/play_game')
def test():
    return render_template('play_game.html')

#@app.route('/play_game')
@app.route('/play_game/<room_id>')
def play_game(room_id = None):
    if session['logged_in']:
        #om ingen room_id finns ska användaren skapa ett spel, annars ska den gå med ett spel
        conn = create_connection()
        cur = conn.cursor()
        user = cur.execute("SELECT * FROM user WHERE username = ?", (session['username'], )).fetchone()
        level = cur.execute("SELECT * FROM level WHERE creator_id = ?", (session['id'], )).fetchone()
        player = Player(user[1], level[3])
        if room_id == None:
            field = Field(session['id'], level[2])
            field.load_from_database()
            game = Game(set_room_id())
            game.add_field(field)
            game.add_player(player)
            ongoing_games.append(game)
        else:
            for game in ongoing_games:
                if game.room_id == room_id:
                    game.add_player(player)
        if game.start_game():
            return render_template('play_game.html', player = player,  game = game)
        return render_template('waitinglobby.html')
        
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
    cur = create_connection().cursor()
    return render_template('list_game.html', username = session['username'])


@app.route('/edit-game')
def edit_game():
    return render_template('edit_game.html')