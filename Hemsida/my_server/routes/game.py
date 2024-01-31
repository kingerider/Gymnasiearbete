
from my_server import app
from flask import render_template, abort, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from my_server.routes.dbhandler import create_connection
from my_server.routes.objects import Game, Player, Field

socket = SocketIO(app)

test_game = Game('Shadowrealmen', 'room_-1')

ongoing_games = {
    'room_-1': test_game 
}

#kollar alla id på varje spel och lägger till max + 1 som nytt id, får tillbaka 0 om listan är tom
def set_room_id():
    list_of_roomid = []
    for game in ongoing_games:
        if game.room_id != None:
            list_of_roomid.append(game.room_id)
    if len(list_of_roomid) == 0:
        return 'room_0'
    max = list_of_roomid[0]
    for roomid in list_of_roomid:
        if roomid > max:
            max = roomid
    return f'room_{max + 1}'



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
        level = cur.execute("SELECT title, player_health FROM level WHERE creator_id = ?", (session['id'], )).fetchone()        
        player = Player(session['username'], level[1])
        conn.close()
        if room_id == None:
            field = Field(session['id'])
            field.load_from_database()
            game = Game(level[0], set_room_id())
            game.add_field(field)
            game.add_player(player)
            ongoing_games[game.room_id] = game
        else:
            for game in ongoing_games:
                if game.room_id == room_id:
                    game.add_player(player)
        return render_template('play_game.html', player = player,  game = game)
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
    return render_template('list_game.html', username = session['username'], ongoing_games = ongoing_games)

@app.route('/build_game')
def build_game():
    return render_template('build_game.html')

@app.route('/edit_game')
def edit_game():
    return render_template('edit_game.html')