from my_server import socket
from my_server.routes import ongoing_games
from my_server.routes.dbhandler import create_connection
from my_server.routes.objects import Projectile
from flask import session
from flask_socketio import join_room, leave_room, emit

tile_size = 20
canvasw = 800
canvash = 440

clients = []

@socket.on("connect")
def handle_connect():
    print("Client connected!")

@socket.on('disconnect')
def handle_disconnect():
    print("Client disconnected!")

@socket.on('join')
def handle_join_room(data):
    join_room(data['room'])
    clients.append({'name': session['username'], 'room': data['room']})

    game = ongoing_games[data['room']]
    if len(game.players) == 2:
        game = ongoing_games[data['room']]
        conn = create_connection()
        cur = conn.cursor()
        play_count = cur.execute("SELECT play_count FROM level WHERE id == ?", (game.id,)).fetchone()[0]
        play_count = int(play_count+1)
        cur.execute("UPDATE level SET play_count = ? WHERE id == ?", (play_count, game.id, ))
        conn.commit()
        conn.close()
        game.field.start_monsters()
        emit('message_from_server', {
            'message': f'start_game',
            'game': game.get_game_info()
        }, to=data['room'])
    else:
        emit('message_from_server', {
            'message': 'Första gick med i rummet',
            'game': None,
        }, to=data['room'])

@socket.on('leave')
def on_leave(data):
    leave_room(data['room'])
    game = ongoing_games[data['room']]
    if len(game.players) == 1:
        game.players.append(None)
    game.field.stop_monsters()
    if game.projectiles[0] != None:
        game.projectiles[0].thread.stop()
    if game.projectiles[1] != None:
        game.projectiles[1].thread.stop()
    for client in clients:
        if client['room'] == data['room'] and client['name'] == session['username']:
            clients.remove(client)
    emit('navigate_to', f'/memberarea')


#Hämtar data från servern för att sidan ska kunna uppdatera
@socket.on('update_canvas')
def update_game(data):
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
    try:
        if data['move'] == 'right':
                moved_player = game.players[data['player_id']]
                moved_player.direction = data['move']
                x = moved_player.positionX
                y = moved_player.positionY
                dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
                positions[int(x + 1)][(int(y))] = dict_moved_player
                positions[int(x)][(int(y))] = None
                moved_player.set_x(int(x) + 1)
        elif data['move'] == 'left': 
                moved_player = game.players[data['player_id']]
                moved_player.direction = data['move']
                x = moved_player.positionX
                y = moved_player.positionY
                dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
                positions[int(x - 1)][(int(y))] = dict_moved_player
                positions[int(x)][(int(y))] = None
                moved_player.set_x(int(x) - 1)
        elif data['move'] == 'up': 
                moved_player = game.players[data['player_id']]
                moved_player.direction = data['move']
                x = moved_player.positionX
                y = moved_player.positionY
                dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
                positions[int(x)][(int(y - 1))] = dict_moved_player
                positions[int(x)][(int(y))] = None
                moved_player.set_y(int(y) - 1)
        elif data['move'] == 'down': 
                moved_player = game.players[data['player_id']]
                moved_player.direction = data['move']
                x = moved_player.positionX
                y = moved_player.positionY
                dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
                positions[int(x)][(int(y + 1))] = dict_moved_player
                positions[int(x)][(int(y))] = None
                moved_player.set_y(int(y) + 1)
    except:
        print("Ajabaja, kan inte röra dig dära lillen")

#Skapar skott
@socket.on('shoot_projectile')
def shoot_projectile(data): 
    game = ongoing_games[data['room']]
    if game.projectiles[data['player_id']] == None:
        positions = game.field_map
        player = game.players[data['player_id']]
        if player.direction == 'right':
            try:
                if positions[int(player.positionX) + 1][(int(player.positionY))] == None:
                    game.projectiles[data['player_id']] = Projectile(int(player.positionX) + 1, int(player.positionY), player.direction, data['player_id'], data['room'])
                elif positions[int(player.positionX) + 1][(int(player.positionY))]['type'] == 'player':
                    if data['player_id'] == 0:
                        game.players[1].damage_taken()
                    else:
                        game.players[0].damage_taken()
            except:
                print('Du kan inte skjuta där!')
        elif player.direction == 'left':
            try:
                if positions[int(player.positionX) - 1][(int(player.positionY))] == None:
                    game.projectiles[data['player_id']] = Projectile(int(player.positionX) - 1, int(player.positionY), player.direction, data['player_id'], data['room'])
                elif positions[int(player.positionX) - 1][(int(player.positionY))]['type'] == 'player':
                    if data['player_id'] == 0:
                        game.players[1].damage_taken()
                    else:
                        game.players[0].damage_taken()
            except:
                print('Du kan inte skjuta där!')
        elif player.direction == 'up':
            try:
                if positions[int(player.positionX)][(int(player.positionY) - 1)] == None:
                    game.projectiles[data['player_id']] = Projectile(int(player.positionX), int(player.positionY) - 1, player.direction, data['player_id'], data['room'])
                elif positions[int(player.positionX)][(int(player.positionY) - 1)]['type'] == 'player':
                    if data['player_id'] == 0:
                        game.players[1].damage_taken()
                    else:
                        game.players[0].damage_taken()
            except:
                print('Du kan inte skjuta där!')
        elif player.direction == 'down':
            try:
                if positions[int(player.positionX)][(int(player.positionY) + 1)] == None:
                    game.projectiles[data['player_id']] = Projectile(int(player.positionX), int(player.positionY) + 1, player.direction, data['player_id'], data['room'])
                elif positions[int(player.positionX)][(int(player.positionY) + 1)]['type'] == 'player':
                    if data['player_id'] == 0:
                        game.players[1].damage_taken()
                    else:
                        game.players[0].damage_taken()
            except:
                print('Du kan inte skjuta där!')