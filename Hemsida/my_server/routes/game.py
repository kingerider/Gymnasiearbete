
from my_server import app
from flask import render_template, redirect, url_for, abort, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from my_server.routes.dbhandler import create_connection
from my_server.routes.objects import Game, Player, Field

socket = SocketIO(app)

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

conn = create_connection()
cur = conn.cursor()
test_level = cur.execute("SELECT title, player_health FROM level WHERE creator_id = ?", (3, )).fetchone()
test_game = Game(3, test_level[0], 'room_-1')
test_field = Field(test_game.id, test_level[1])
test_field.load_from_database()
test_game.add_field(test_field)
conn.close()


ongoing_games = {
    'room_-1': test_game 
}

#kollar alla id på varje spel och lägger till max + 1 som nytt id, får tillbaka 0 om listan är tom



@app.route('/play_game')
def test():
    return render_template('play_game.html')

@app.route('/play_game/create/<level_id>')
def play_game_create(level_id = None):
    if session['logged_in']:
        #om ingen room_id finns ska användaren skapa ett spel, annars ska den gå med ett spel
        conn = create_connection()
        cur = conn.cursor()
        level = cur.execute("SELECT title, player_health FROM level WHERE id = ?", (level_id, )).fetchone()
        player = Player(session['username'], level[1])
        field = Field(level_id)
        field.load_from_database()
        game = Game(level_id, level[0], set_room_id())
        game.add_field(field)
        game.add_player(player)
        ongoing_games[game.room_id] = game
        conn.close()
            
        return render_template('play_game.html', player_1 = player,  game = game)
    abort(401)

@app.route('/play_game/join/<room_id>')
def play_game_join(room_id = None):
    if session['logged_in']:
        game = ongoing_games.get(room_id)
        player = Player(session['username'], game.field.health)
        game.add_player(player)
        return render_template('play_game.html', player_2 = player)

@socket.on('join')
def handle_join_room(data):
    join_room(data['room'])
    #send_message_to_room({
    #    'heading': 'Info',
    #    'message': f'User {data["username"]} has joined the room.',
    #    'room': data['room']
    #})
    emit('navigate_to', f'/play_game/{data["role"]}/{data["room"]}')

@socket.on('leave')
def on_leave(data):
    leave_room(data['room'])
    #send_message_to_room({
    #    'heading': 'Info',
    #    'message': f'User {data["username"]} has left the room.',
    #   'room': data['room']
    #})
    emit('navigate_to', f'/memberarea')


#@socket.on('send_message_to_room')
#def send_message_to_room(data):
#    emit('message_from_server', {
#        'heading': data['heading'],
#        'message': data['message']
#    }, to=data['room'])

@app.route('/list_games')
def list_games():
    return render_template('list_game.html', username = session['username'], ongoing_games = ongoing_games)

@app.route('/list_levels')
def list_levels():
    conn = create_connection()
    cur = conn.cursor()
    levels = cur.execute("SELECT * FROM level").fetchall()
    return render_template('list_level.html', levels = levels)

@app.route('/build_game')
def build_game():
    return render_template('build_game.html')

@app.route('/edit_game')
def edit_game():
    return render_template('edit_game.html')