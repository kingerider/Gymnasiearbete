from my_server import app
from flask import render_template, redirect, url_for, abort, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from my_server.routes.dbhandler import create_connection
from my_server.routes.objects import Game, Player, Field
import random

socket = SocketIO(app)

#should not be here later on
tile_size = 20
canvasw = 800
canvasw = 400

def set_room_id():
    list_of_roomid = list(ongoing_games.keys())
    if len(list_of_roomid) == 0:
        return 'room_0'
    max = int(list_of_roomid[0][5:7])
    for roomid in list_of_roomid:
        int_roomid = int(roomid[5:7])
        if int_roomid > max:
            max = int_roomid
    
    return f'room_{max + 1}'

#conn = create_connection()
#cur = conn.cursor()
#test_level = cur.execute("SELECT title, player_health FROM level WHERE creator_id = ?", (3, )).fetchone()
#test_game = Game(3, test_level[0], 'room_-1')
#test_field = Field(test_game.id, test_level[1])
#test_field.load_from_database()
#test_game.add_field(test_field)
#conn.close()


ongoing_games = {
    #'room_-1': test_game 
}

#kollar alla id på varje spel och lägger till max + 1 som nytt id, får tillbaka 0 om listan är tom

@app.route('/play_game/create/<level_id>')
def play_game_create(level_id = None):
    if session['logged_in']:
        #Skapar ett nytt spel som läggs in i ongoing_games och går till playgame
        conn = create_connection()
        cur = conn.cursor()
        level = cur.execute("SELECT title, player_health FROM level WHERE id = ?", (level_id, )).fetchone()
        field = Field(level_id, level[1])
        field.load_from_database()
        game = Game(level_id, level[0], set_room_id())
        game.add_field(field)
        ongoing_games[game.room_id] = game
        conn.close()
            
        return redirect(url_for('play_game_join', room_id = game.room_id))
    abort(401)

@app.route('/play_game/join/<room_id>')
def play_game_join(room_id = None):
    if session['logged_in']:
        game = ongoing_games.get(room_id)
        player = Player(session['username'], game.field.health)
        game.add_player(player)
        return render_template('play_game.html', game = game)

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
    print(ongoing_games)
    ongoing_games.pop(data['room'], None)
    print(ongoing_games.pop(data['room'], None))
    print(ongoing_games)
    #send_message_to_room({
    #    'heading': 'Info',
    #    'message': f'User {data["username"]} has left the room.',
    #   'room': data['room']
    #})
    emit('navigate_to', f'/memberarea')

#Hämtar data från servern för att sidan ska kunna uppdatera
@socket.on('update_canvas')
def update_game(data):
    game = ongoing_games[data['room']]
    emit('update', {
        'player1' : game.players[0],
        'player2' : game.players[1],
        'field_map' : game.field_map 
    }, to=data['room'])
    

#Ändrar lokala spelarens position i servern
@socket.on('player_move')
def player_move(data):
    game = ongoing_games[data['room']]
    if data['move'] == 'right':
        game.players[data['player_id']].moveTo(game.players[data['player_id']].positionX + 1, game.players[data['player_id']].positionY)
    elif data['move'] == 'left': 
        game.players[data['player_id']].moveTo(game.players[data['player_id']].positionX - 1, game.players[data['player_id']].positionY)
    elif data['move'] == 'up': 
        game.players[data['player_id']].moveTo(game.players[data['player_id']].positionX, game.players[data['player_id']].positionY - 1)
    elif data['move'] == 'down': 
        game.players[data['player_id']].moveTo(game.players[data['player_id']].positionX, game.players[data['player_id']].positionY + 1)

@socket.on('monster_move')
def monster_move(data):

    game = ongoing_games[data['room']]
    monsters = game.field.get_monster_pos()
    positions = game.field_map
    #Fix monster get array
    #Fix wall get array.size
    #Fix monster can go outside canvas
    #Fix so player, monster and items have direction
    #bullet go in direction that player direction facing, on wall hit get destroyed, on monster hit die

    for monsterPosition in monsters:

        #movementChoose 1 = left , 2 , 3 , 4
        movementChoose = 0
        checkForWalls = True


        #how close is player, if player is within 5 tiles don't do random action
        #if(5*tileSize > (playerX - monsterArray[j].getX()) and -5*tileSize < (playerX - monsterArray[j].getX()) && 5*tileSize > (playerY - monsterArray[j].getY()) && -5*tileSize < (playerY - monsterArray[j].getY())){
        #movementChoose = 1;
        if(False):
            pass
        else:
            movementChoose = random.randint(1, 4)
            
        #movementChoose 1 = left , 2 , 3 , 4
        if movementChoose == 1:
            
            #Check walls
            for wallPosition in wallArray.size:
                if monsterPosition.getX() == wallPosition.getX()-1 and monsterPosition.getY() == wallPosition.getY():
                    checkForWalls = False
            if checkForWalls:
                monsterPosition.setX(monsterPosition.getX() - tile_size)
        elif movementChoose == 2:
            #Check walls
            for wallPosition in wallArray.size:
                if monsterPosition.getX() == wallPosition.getX()+1 and monsterPosition.getY() == wallPosition.getY():
                    checkForWalls = False
            if checkForWalls:
                monsterPosition.setX(monsterPosition.getX()+1)
        elif movementChoose == 3:
            #Check walls
            for wallPosition in wallArray.size:
                if monsterPosition.getY() == wallPosition.getY()-1 and monsterPosition.getX() == wallPosition.getX():
                    checkForWalls = False
            if checkForWalls:
                monsterPosition.setY(monsterPosition.getY() - 1)
        elif movementChoose == 4:
            #Check walls
            for wallPosition in wallArray.size:
                if monsterPosition.getY() == wallPosition.getY()+1 and monsterPosition.getX() == wallPosition.getX():
                    checkForWalls = False
            if checkForWalls:
                monsterPosition.setY(monsterPosition.getY()+1)


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