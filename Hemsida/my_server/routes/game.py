from my_server import app, socket
from flask import render_template, redirect, url_for, abort, flash, session, request
from flask_socketio import emit, join_room, leave_room
from my_server.routes.dbhandler import create_connection
from my_server.routes.objects import Game, Player, Field
import random
from datetime import datetime

import threading

monster_start = {}

def startit():
    t = threading.Timer(0.2, startit)
    t.start()
    monster_start['thread'] = t
    monster_move(monster_start['room'])


#should not be here later on
tile_size = 20
canvasw = 800
canvash = 440

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
        print(ongoing_games)
        ongoing_games[game.room_id] = game
        print(ongoing_games)
        conn.close()
            
        return redirect(url_for('play_game_join', room_id = game.room_id))
    abort(401)

clients = []

#Skickar spelaren till playgame och tar med game
@app.route('/play_game/join/<room_id>')
def play_game_join(room_id = None):
    print("HERE JOIN")

    if session['logged_in']:
        game = ongoing_games[room_id]
        if len(game.players) == 0:
            player = Player(session['username'], game.field.health, "right", int(canvasw/tile_size)/8, int(canvash/tile_size)/2)
            game.add_player(player)
        else:
            player = Player(session['username'], game.field.health, "left", int(canvasw/tile_size) - (int(canvasw/tile_size)/8), int(canvash/tile_size)/2)
            game.add_player(player)
            game.place_objects_field()
        return render_template('play_game.html', game = game.get_game_info())

#SKA TESTA ATT GÖRA EN KLIENTLISTA OCH SE OM MAN KAN ANVÄNDA DEN FÖR ATT FÅ LOKAL KLIENT

@socket.on("connect")
def handle_connect():
    print("Client connected!")

@socket.on('disconnect')
def handle_disconnect():
    print("Client disconnected!")

@socket.on('join')
def handle_join_room(data):
    print('JOIN JOIN JOY')
    print('JOIN JOIN JOY')
    print('JOIN JOIN JOY')
    print('JOIN JOIN JOY')
    print('JOIN JOIN JOY')
    join_room(data['room'])
    print(f'session: {session["username"]}')
    #print('%s connected' % (request.namespace.socket.sessid))
    #clients.append(request.namespace)
    #ongoing_games[data['room']].ongoing_players += 1

    # if ongoing_games[data['room']].:
    #HÄR SKA DET FIXAS MED SOCKETIO
    if len(ongoing_games[data['room']].players) == 2:
        #startit(data['room'])
        monster_start['room'] = data
        startit()
        emit('message_from_server', {
            'message': f'start_game',
            'game': ongoing_games[data['room']].get_game_info(),
            #'username': session['username']
        }, to=data['room'])
    else:
        emit('message_from_server', {
            'message': 'Första gick med i rummet',
            'game': None,
            #'username': session['username']
        }, to=data['room'])


    #send_message_to_room({
    #    'heading': 'Info',
    #    'message': f'User {data["username"]} has joined the room.',
    #    'room': data['room']
    #})
    #emit('navigate_to', f'/play_game/{data["role"]}/{data["room"]}')

@socket.on('leave')
def on_leave(data):
    leave_room(data['room'])
    print(ongoing_games)
    ongoing_games.pop(data['room'], None)
    print(ongoing_games.pop(data['room'], None))
    print(ongoing_games)
    monster_start['thread'].cancel()
    #send_message_to_room({
    #    'heading': 'Info',
    #    'message': f'User {data["username"]} has left the room.',
    #   'room': data['room']
    #})
    #print("%s disconnected" % (request.namespace.socket.sessid))
    #clients.remove(request.namespace)
    emit('navigate_to', f'/memberarea')
    
@socket.on('clientlist')
def get_clients_in_room(data):
    #clients = socket.server.manager.rooms[data['room']]
    clients = socket.server.manager.get_participants(data['room'])
    print('clients:' + clients)
    
    #return {'clients': clients}

#Hämtar data från servern för att sidan ska kunna uppdatera
@socket.on('update_canvas')
def update_game(data):
    print("Update_game, update_canvas")
    print("Ass hair")
   # print('Is game ongoing:')
    #print(ongoing_games)
    #print('What is data:')
    #print(data)
   # print('What does game.fieldmap contain')
    #print(ongoing_games[data['room']].field_map)
    print("Ass hair")
    print("Ass hair")
   
    game = ongoing_games[data['room']]

    emit('update', {
        'field_map' : game.field_map,
        'width': canvasw,
        'height': canvash,
        'tile_size': tile_size 
    }, to=data['room'])
    

#Ändrar lokala spelarens position i servern
@socket.on('player_move')
def player_move(data):
    game = ongoing_games[data['room']]
    positions = game.field_map
    if data['move'] == 'right':
        try:
            moved_player = game.players[data['player_id']]#.moveTo(game.players[data['player_id']].positionX + 1, game.players[data['player_id']].positionY)
            x = moved_player.positionX
            y = moved_player.positionY
            dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
            positions[int(x + 1)][(int(y))] = dict_moved_player
            positions[int(x)][(int(y))] = None
            moved_player.positionX += 1
        except:
            print("Ajabaja, kan inte röra dig dära lillen")
    elif data['move'] == 'left': 
        #game.players[data['player_id']].moveTo(game.players[data['player_id']].positionX - 1, game.players[data['player_id']].positionY)
        try:
            moved_player = game.players[data['player_id']]#.moveTo(game.players[data['player_id']].positionX + 1, game.players[data['player_id']].positionY)
            x = moved_player.positionX
            y = moved_player.positionY
            dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
            positions[int(x - 1)][(int(y))] = dict_moved_player
            positions[int(x)][(int(y))] = None
            moved_player.positionX -= 1
        except:
            print("Ajabaja, kan inte röra dig dära lillen")
    elif data['move'] == 'up': 
        #game.players[data['player_id']].moveTo(game.players[data['player_id']].positionX, game.players[data['player_id']].positionY - 1)
        try:
            moved_player = game.players[data['player_id']]#.moveTo(game.players[data['player_id']].positionX + 1, game.players[data['player_id']].positionY)
            x = moved_player.positionX
            y = moved_player.positionY
            dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
            positions[int(x)][(int(y - 1))] = dict_moved_player
            positions[int(x)][(int(y))] = None
            moved_player.positionY -= 1
        except:
            print("Ajabaja, kan inte röra dig dära lillen")
    elif data['move'] == 'down': 
        try:
            #game.players[data['player_id']].moveTo(game.players[data['player_id']].positionX, game.players[data['player_id']].positionY + 1)
            moved_player = game.players[data['player_id']]#.moveTo(game.players[data['player_id']].positionX + 1, game.players[data['player_id']].positionY)
            x = moved_player.positionX
            y = moved_player.positionY
            dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
            positions[int(x)][(int(y + 1))] = dict_moved_player
            positions[int(x)][(int(y))] = None
            moved_player.positionY += 1
        except:
            print("Ajabaja, kan inte röra dig dära lillen")
    #ongoing_games[data['room']].field_map = positions

def monster_move(data):

    game = ongoing_games[data['room']]
    monsters = game.field.enemies
    positions = game.field_map

    for monster in monsters:

        movementChoose = 0
        x = monster.positionX
        y = monster.positionY
        dict_monster = dict(type="enemy")
        #how close is player, if player is within 5 tiles don't do random action
        #if(5*tileSize > (playerX - monsterArray[j].getX()) and -5*tileSize < (playerX - monsterArray[j].getX()) && 5*tileSize > (playerY - monsterArray[j].getY()) && -5*tileSize < (playerY - monsterArray[j].getY())){
        #movementChoose = 1;
        if(False):
            pass
        else:
            movementChoose = random.randint(1, 4)
        #Left
        if movementChoose == 1:
            #Check if movement available
            try:
                if positions[int(x - 1)][(int(y))] == None:
                    positions[int(x - 1)][(int(y))] = dict_monster
                    positions[int(x)][(int(y))] = None
                    monster.positionX -= 1
            except:
                print("Ajabaja, kan inte röra dig dära lillen")

        #Right
        elif movementChoose == 2:
            #Check if movement available
            try:
                if positions[int(x + 1)][(int(y))] == None:
                    positions[int(x + 1)][(int(y))] = dict_monster
                    positions[int(x)][(int(y))] = None
                    monster.positionX += 1
            except:
                print("Ajabaja, kan inte röra dig dära lillen")
        #Up
        elif movementChoose == 3:
            #Check if movement available
            try:
                if positions[int(x)][(int(y - 1))] == None:
                    positions[int(x)][(int(y - 1))] = dict_monster
                    positions[int(x)][(int(y))] = None
                    monster.positionY -= 1
            except:
                print("Ajabaja, kan inte röra dig dära lillen")
        #Down
        elif movementChoose == 4:
            #Check if movement available
            try:
                if positions[int(x)][(int(y + 1))] == None:
                    positions[int(x)][(int(y + 1))] = dict_monster
                    positions[int(x)][(int(y))] = None
                    monster.positionY += 1
            except:
                print("Ajabaja, kan inte röra dig dära lillen")



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

@app.route('/edit_game/<level_id>')
def edit_game(level_id = None):
    return render_template('edit_game.html', id = level_id)

@app.route('/save_level/<status>/<title>/<player_health>/<description>')
def save_level(status = None, title = None, player_health = None, description = None):
    now = datetime.now()
    date = now.strftime('%Y-%m-%d %H h')
    conn = create_connection()
    cur = conn.cursor()
    if status == 'build':
        cur.execute("INSERT INTO level (creator_id, title, player_health, description, date) VALUES (?, ?, ?, ?, ?)", (session['id'], title, player_health, description, date))
        conn.commit()
    elif status == 'edit':
        cur.execute("UPDATE level SET title = ?, player_health = ?, description = ?, date = ?", (title, player_health, description, date))
        conn.commit()
    conn.close()
    flash("Banan har sparats", 'success')
    return redirect(url_for('list_levels'))