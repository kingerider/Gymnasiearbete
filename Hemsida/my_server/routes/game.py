from my_server import app, socket
from flask import render_template, redirect, url_for, abort, flash, session, request
from flask_socketio import emit, join_room, leave_room
from my_server.routes.dbhandler import create_connection
from my_server.routes.objects import Game, Player, Entity
import random
from datetime import datetime
import threading
from threading import Thread
import time

ongoing_games = {
    #'room_-1': test_game 
}

class EnemyThread(Thread):
    def __init__(self, enemy):
        Thread.__init__(self)
        self._stop_event = threading.Event()
        self.enemy = enemy
        self.directions = ['right', 'left', 'up', 'down']
    
    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            self.enemy.move(ongoing_games[self.enemy.room_id])
            time.sleep(0.2)

class Enemy(Entity):
    def __init__(self, id, level_id, posX, posY, dir, room_id):
        super().__init__(posX, posY)
        self.id = id
        self.level_id = level_id
        self.room_id = room_id
        self.direction = dir
        self.thread = EnemyThread(self)
    
    def start_thread(self):
        self.thread.start()
    
    def object_to_dict():
        return dict(type="enemy")

    def move(self, game):
        field_map = game.field_map
        dir = self.thread.directions[random.randint(0, 3)]
        try:
            if self.direction == 'right':
                print('Höger Ja')
                self.direction = dir
                if field_map[int(self.positionX) + 1][(int(self.positionY))] == None:
                    print(f'före: {self.positionX}')
                    self.set_x(int(self.positionX) + 1)
                    print(f'efter: {self.positionX}')
                    field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                    field_map[int(self.positionX) - 1][(int(self.positionY))] = None
                    print("rör sig")
                    print(f'field map: {field_map}')
                elif field_map[int(self.positionX) + 1][(int(self.positionY))]['type'] == 'player':
                    print("skadar")
                    x = int(self.positionX) + 1
                    y = int(self.positionY)
                    players = game.players
                    for player in players:
                        if player.name == field_map[int(x)][(int(y))]['name']:
                            player.damage_taken()
                            field_map[int(x)][(int(y))] = player.object_to_dict()
                            print(f'{player.name} tog skada')
                    # player_taken_damage(game.players, field_map, int(self.positionX) + 1, (int(self.positionY)))
            elif self.direction == 'left':
                print('Vänster Ja')
                self.direction = dir
                if field_map[int(self.positionX) - 1][(int(self.positionY))] == None:
                    print("rör sig")
                    print(f'före: {self.positionX}')
                    self.set_x(int(self.positionX) - 1)
                    print(f'efter: {self.positionX}')
                    field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                    field_map[int(self.positionX) + 1][(int(self.positionY))] = None
                elif field_map[int(self.positionX) - 1][(int(self.positionY))]['type'] == 'player':
                    print("skadar")
                    x = int(self.positionX) - 1
                    y = int(self.positionY)
                    players = game.players
                    for player in players:
                        if player.name == field_map[int(x)][(int(y))]['name']:
                            player.damage_taken()
                            field_map[int(x)][(int(y))] = player.object_to_dict()
                            print(f'{player.name} tog skada')
                    # player_taken_damage(game.players, field_map, int(self.positionX) - 1, (int(self.positionY)))
            elif self.direction == 'up':
                print('Upp ja')
                self.direction = dir
                if field_map[int(self.positionX)][(int(self.positionY) - 1)] == None:
                    print("rör sig")
                    print(f'före: {self.positionY}')
                    self.set_y(int(self.positionY) - 1)
                    print(f'efter: {self.positionY}')
                    field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                    field_map[int(self.positionX)][(int(self.positionY) + 1)] = None
                elif field_map[int(self.positionX)][(int(self.positionY) - 1)]['type'] == 'player':
                    print("skadar")
                    x = int(self.positionX)
                    y = int(self.positionY) - 1
                    players = game.players
                    for player in players:
                        if player.name == field_map[int(x)][(int(y))]['name']:
                            player.damage_taken()
                            field_map[int(x)][(int(y))] = player.object_to_dict()
                            print(f'{player.name} tog skada')
                    # player_taken_damage(game.players, field_map, int(self.positionX), (int(self.positionY) - 1))
            elif self.direction == 'down':
                print('Ner Ja')
                self.direction = dir
                if field_map[int(self.positionX)][(int(self.positionY) + 1)] == None:
                    print("rör sig")
                    print(f'före: {self.positionY}')
                    self.set_y(int(self.positionY) + 1)
                    print(f'efter: {self.positionY}')
                    field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                    field_map[int(self.positionX)][(int(self.positionY) - 1)] = None
                elif field_map[int(self.positionX)][(int(self.positionY) + 1)]['type'] == 'player':
                    print("skadar")
                    x = int(self.positionX)
                    y = int(self.positionY) + 1
                    players = game.players
                    for player in players:
                        if player.name == field_map[int(x)][(int(y))]['name']:
                            player.damage_taken()
                            field_map[int(x)][(int(y))] = player.object_to_dict()
                            print(f'{player.name} tog skada')
                    # player_taken_damage(game.players, field_map, int(self.positionX), (int(self.positionY) + 1))
        except:
            pass
            
        

    def change_direction(self, str):
        self.direction = str

    def moveTo(self, newPosX, newPosY):
        self.set_position(newPosX, newPosY)

class Wall(Entity):
    def __init__(self, id, level_id, posX, posY):
        self.id = id
        self.level_id = level_id
        super().__init__(posX, posY)

class Item(Entity):
    def __init__(self, id, level_id, posX, posY, type):
        self.id = id
        self.level_id = level_id
        super().__init__(posX, posY)
        self.type = type

#Erik Change


class Field:
    def __init__(self, id, health, room_id):
        self.id = id
        self.room_id = room_id
        self.health = health
        self.walls = []
        self.enemies = []
        self.items = []

        #self.field = [][]
        #self.field[0][5] = Monster()
        #self.field[0][6] = None
        #self.field[5][6] = Wall()

        #Flytta monster ned ett steg.
        #self.field[1][5] = self.field[0][5]
        #self.field[0][5] = None
    
    def load_from_database(self):
        conn = create_connection()
        cur = conn.cursor()
        directions = ['right', 'left', 'up', 'down']
        fetched_walls = cur.execute("SELECT * FROM wall WHERE level_id = ?", (self.id, )).fetchall()
        for wall in fetched_walls:
            self.walls.append(Wall(wall[0], wall[1], wall[2], wall[3]))
        fetched_enemies = cur.execute("SELECT * FROM enemy WHERE level_id = ?", (self.id, )).fetchall()
        for enemy in fetched_enemies:
            self.enemies.append(Enemy(enemy[0], enemy[1], enemy[2], enemy[3], directions[random.randint(0, 3)], self.room_id))
        fetched_items = cur.execute("SELECT * FROM item WHERE level_id = ?", (self.id, )).fetchall()
        for item in fetched_items:
            self.items.append(Item(item[0], item[1], item[2], item[3], item[4]))
        conn.close()

    def get_monster_pos(self):
        list_of_positions = []
        for enemy in self.enemies:
            list_of_positions.append({
                'x': enemy.positionX,
                'y': enemy.positionY
            })
        return list_of_positions
    
    def start_monsters(self):
        for enemy in self.enemies:
            enemy.start_thread()
    
    def stop_monsters(self):
        for enemy in self.enemies:
            enemy.thread.stop()
    
    def get_wall_pos(self):
        list_of_positions = []
        for wall in self.walls:
            list_of_positions.append({
                'x': wall.positionX,
                'y': wall.positionY
            })
        return list_of_positions
    
    def get_item_pos(self):
        list_of_positions = []
        for item in self.items:
            list_of_positions.append({
                'x': item.positionX,
                'y': item.positionY
            })
        return list_of_positions


# def startit():
#     t = threading.Timer(0.2, startit)
#     t.start()
#     for key in thread_start.keys():
#         thread_start[key] = {'threadmonster': t, 'room': key}
#         monster_move(thread_start[key])
    

# def startbullet():
#     t = threading.Timer(0.05, startbullet)
#     t.start()
#     for key in thread_start.keys():
#         if ongoing_games[key].projectiles[0] != None or ongoing_games[key].projectiles[1] != None:
#             thread_start[key]['threadbullet'] = t
#             projectile_move(thread_start[key])


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

#kollar alla id på varje spel och lägger till max + 1 som nytt id, får tillbaka 0 om listan är tom

@app.route('/play_game/create/<level_id>')
def play_game_create(level_id = None):
    if session['logged_in']:
        #Skapar ett nytt spel som läggs in i ongoing_games och går till play_game_join
        conn = create_connection()
        cur = conn.cursor()
        level = cur.execute("SELECT title, player_health FROM level WHERE id = ?", (level_id, )).fetchone()
        game = Game(level_id, level[0], set_room_id())
        field = Field(level_id, level[1], game.room_id)
        field.load_from_database()
        game.add_field(field)
        game.set_host(session['username'])
        print(ongoing_games)
        ongoing_games[game.room_id] = game
        print(ongoing_games)
        conn.close()   
        return redirect(url_for('play_game_join', room_id = game.room_id))
    abort(401)

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
    abort(401)

clients = []

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
    clients.append({'name': session['username'], 'room': data['room']})
    #print('%s connected' % (request.namespace.socket.sessid))
    #clients.append(request.namespace)
    #ongoing_games[data['room']].ongoing_players += 1

    game = ongoing_games[data['room']]
    print(clients)
    # if ongoing_games[data['room']].:
    #HÄR SKA DET FIXAS MED SOCKETIO
    if len(ongoing_games[data['room']].players) == 2:
        #Level play count++
        game = ongoing_games[data['room']]
        conn = create_connection()
        cur = conn.cursor()
        play_count = cur.execute("SELECT play_count FROM level WHERE id == ?", (game.id,)).fetchone()[0]
        print(play_count)
        print(play_count)
        print(play_count)
        print(play_count)
        print(play_count)
        print(play_count)
        print(play_count)
        print(play_count)

        print(play_count)
        play_count = int(play_count+1)
        print(play_count)
        cur.execute("UPDATE level SET play_count = ? WHERE id == ?", (play_count, game.id, ))
        conn.commit()
        conn.close()
    if len(game.players) == 2:

        #startit(data['room'])
        # threading.Thread(target=monster_move, args=(data, )).start()
        # startit()
        game.field.start_monsters()
        emit('message_from_server', {
            'message': f'start_game',
            'game': game.get_game_info()
            #'username': session['username']
        }, to=data['room'])
    else:
        emit('message_from_server', {
            'message': 'Första gick med i rummet',
            'game': None,
            #'username': session['username']
        }, to=data['room'])
    #emit('navigate_to', f'/play_game/{data["role"]}/{data["room"]}')
# @socket.on('add_played_game')
# def add_played_game(data):
#     print('Nu spelas det')
#     print(f'Är {data["player1"]} och {data["player2"]} i farten nu igen...')
#     print(f'Är {data["player1"]} och {data["player2"]} i farten nu igen...')
#     print(f'Är {data["player1"]} och {data["player2"]} i farten nu igen...')
#     print(f'Är {data["player1"]} och {data["player2"]} i farten nu igen...')
#     print(f'Är {data["player1"]} och {data["player2"]} i farten nu igen...')
#     print(f'Är {data["player1"]} och {data["player2"]} i farten nu igen...')
#     print(f'Är {data["player1"]} och {data["player2"]} i farten nu igen...')
#     conn = create_connection()
#     cur = conn.cursor()
#     player1count = cur.execute("SELECT games_played FROM user WHERE username = ?", (data['player1'], )).fetchone()[0]
#     player1count += 1
#     cur.execute("UPDATE user SET games_played = ? WHERE username = ?", (player1count, data['player1']))
#     conn.commit()
#     player2count = cur.execute("SELECT games_played FROM user WHERE username = ?", (data['player2'], )).fetchone()[0]
#     player2count += 1
#     cur.execute("UPDATE user SET games_played = ? WHERE username = ?", (player2count, data['player2']))
#     conn.commit()
#     conn.close()

# @socket.on('end_game')
# def end_game(data):
#     print('spelet slut')
#     print(f'{data["winner"]} vann, {data["loser"]} förlorade')
#     print(f'{data["winner"]} vann, {data["loser"]} förlorade')
#     print(f'{data["winner"]} vann, {data["loser"]} förlorade')
#     print(f'{data["winner"]} vann, {data["loser"]} förlorade')
#     print(f'{data["winner"]} vann, {data["loser"]} förlorade')
#     print(f'{data["winner"]} vann, {data["loser"]} förlorade')
#     print(f'{data["winner"]} vann, {data["loser"]} förlorade')
#     conn = create_connection()
#     cur = conn.cursor()
#     winner = cur.execute("SELECT wins FROM user WHERE username = ?", (data['winner'], )).fetchone()[0]
#     winner += 1
#     cur.execute("UPDATE user SET wins = ? WHERE username = ?", (winner, data['winner']))
#     conn.commit()
#     loser = cur.execute("SELECT wins FROM user WHERE username = ?", (data['loser'], )).fetchone()[0]
#     loser += 1
#     cur.execute("UPDATE user SET wins = ? WHERE username = ?", (loser, data['loser']))
#     conn.commit()
#     conn.close()

@socket.on('leave')
def on_leave(data):
    leave_room(data['room'])
    ongoing_games[data['room']].field.stop_monsters()
    print(ongoing_games)
    for client in clients:
        if client['room'] == data['room'] and client['name'] == session['username']:
            clients.remove(client)
    print(ongoing_games)
    emit('navigate_to', f'/memberarea')


#Hämtar data från servern för att sidan ska kunna uppdatera
@socket.on('update_canvas')
def update_game(data):
#     print("Update_game, update_canvas")
#     print("Ass hair")
#    # print('Is game ongoing:')
#     #print(ongoing_games)
#     #print('What is data:')
#     #print(data)
#    # print('What does game.fieldmap contain')
#     #print(ongoing_games[data['room']].field_map)
#     print("Ass hair")
#     print("Ass hair")
   
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
                moved_player.positionX += 1
        elif data['move'] == 'left': 
                moved_player = game.players[data['player_id']]
                moved_player.direction = data['move']
                x = moved_player.positionX
                y = moved_player.positionY
                dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
                positions[int(x - 1)][(int(y))] = dict_moved_player
                positions[int(x)][(int(y))] = None
                moved_player.positionX -= 1
        elif data['move'] == 'up': 
            
                moved_player = game.players[data['player_id']]
                moved_player.direction = data['move']
                x = moved_player.positionX
                y = moved_player.positionY
                dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
                positions[int(x)][(int(y - 1))] = dict_moved_player
                positions[int(x)][(int(y))] = None
                moved_player.positionY -= 1
        elif data['move'] == 'down': 
                moved_player = game.players[data['player_id']]
                moved_player.direction = data['move']
                x = moved_player.positionX
                y = moved_player.positionY
                dict_moved_player = dict(type = "player", name = moved_player.name, direction = data['move'], health = moved_player.health)
                positions[int(x)][(int(y + 1))] = dict_moved_player
                positions[int(x)][(int(y))] = None
                moved_player.positionY += 1
    except:
        print("Ajabaja, kan inte röra dig dära lillen")






# def monster_move(data):

#         game = ongoing_games[data['room']]
#         monsters = game.field.enemies
#         positions = game.field_map
#         players = game.players

#         for monster in monsters:

#             movementChoose = 0
#             x = monster.positionX
#             y = monster.positionY
#             dict_monster = dict(type="enemy")
#             #how close is player, if player is within 5 tiles don't do random action
#             #if(5*tileSize > (playerX - monsterArray[j].getX()) and -5*tileSize < (playerX - monsterArray[j].getX()) && 5*tileSize > (playerY - monsterArray[j].getY()) && -5*tileSize < (playerY - monsterArray[j].getY())){
#             #movementChoose = 1;
#             if(False):
#                 pass
#             else:
#                 movementChoose = random.randint(1, 4)
#             #Left
#             if movementChoose == 1:
#                 #Check if movement available
#                 try:
#                     if positions[int(x - 1)][(int(y))] == None:
#                         positions[int(x - 1)][(int(y))] = dict_monster
#                         positions[int(x)][(int(y))] = None
#                         monster.positionX -= 1
#                     elif positions[int(x - 1)][(int(y))]['type'] == 'player':
#                         player_taken_damage(players, positions, x, y)
#                         # for player in players:
#                         #     if player.name == positions[int(x - 1)][(int(y))]['name']:
#                         #         player.damage_taken()
#                         #         print(f'{player.name} tog skada')
#                 except:
#                     print("Ajabaja, kan inte röra dig dära lillen")

#             #Right
#             elif movementChoose == 2:
#                 #Check if movement available
#                 try:
#                     if positions[int(x + 1)][(int(y))] == None:
#                         positions[int(x + 1)][(int(y))] = dict_monster
#                         positions[int(x)][(int(y))] = None
#                         monster.positionX += 1
#                     elif positions[int(x + 1)][(int(y))]['type'] == 'player':
#                         player_taken_damage(players, positions, x, y)
#                         # for player in players:
#                         #     if player.name == positions[int(x + 1)][(int(y))]['name']:
#                         #         player.damage_taken()
#                         #         print(f'{player.name} tog skada')
#                 except:
#                     print("Ajabaja, kan inte röra dig dära lillen")
#             #Up
#             elif movementChoose == 3:
#                 #Check if movement available
#                 try:
#                     if positions[int(x)][(int(y - 1))] == None:
#                         positions[int(x)][(int(y - 1))] = dict_monster
#                         positions[int(x)][(int(y))] = None
#                         monster.positionY -= 1
#                     elif positions[int(x)][(int(y - 1))]['type'] == 'player':
#                         player_taken_damage(players, positions, x, y)
#                         # for player in players:
#                         #     if player.name == positions[int(x)][(int(y - 1))]['name']:
#                         #         player.damage_taken()
#                         #         print(f'{player.name} tog skada')
#                 except:
#                     print("Ajabaja, kan inte röra dig dära lillen")
#             #Down
#             elif movementChoose == 4:
#                 #Check if movement available
#                 try:
#                     if positions[int(x)][(int(y + 1))] == None:
#                         positions[int(x)][(int(y + 1))] = dict_monster
#                         positions[int(x)][(int(y))] = None
#                         monster.positionY += 1
#                     elif positions[int(x)][(int(y + 1))]['type'] == 'player':
#                         player_taken_damage(players, positions, x, y)
#                         # for player in players:
#                         #     if player.name == positions[int(x)][(int(y + 1))]['name']:
#                         #         player.damage_taken()
#                         #         print(f'{player.name} tog skada')
#                 except:
#                     print("Ajabaja, kan inte röra dig dära lillen")

class BulletThread(Thread):

    def __init__(self, bullet):
        Thread.__init__(self)
        self._stop_event = threading.Event()
        self.bullet = bullet
    
    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            self.bullet.move(ongoing_games[self.bullet.room_id])
            time.sleep(0.05)

class Projectile(Entity):
    def __init__(self, posX, posY, dir, id, ri):
        super().__init__(posX, posY)
        self.direction = dir
        self.player_id = id
        self.room_id = ri
        self.thread = BulletThread(self)
        self.thread.start()
        
    def object_to_dict(self):
        return dict(type = 'projectile', player_id = self.player_id, direction = self.direction)

    def move(self, game):
        field_map = game.field_map
        if self.direction == 'right':
            try:
                if field_map[int(self.positionX) + 1][(int(self.positionY))] == None:
                    try:
                        self.set_x(int(self.positionX) + 1)
                        field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                        field_map[int(self.positionX) - 1][(int(self.positionY))] = None
                    except:
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        print(field_map)
                elif field_map[int(self.positionX) + 1][(int(self.positionY))]['type'] == 'player':
                    if game.players[0].name == field_map[int(self.positionX) + 1][(int(self.positionY))]['name']:
                        game.players[0].damage_taken()
                        field_map[int(game.players[0].positionX)][(int(game.players[0].positionY))] = game.players[0].object_to_dict()
                        print("Health:")
                        print(game.players[0].health)
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        # print(field_map)
                    elif game.players[1].name == field_map[int(self.positionX) + 1][(int(self.positionY))]['name']:
                        game.players[1].damage_taken()
                        field_map[int(game.players[1].positionX)][(int(game.players[1].positionY))] = game.players[1].object_to_dict()
                        print("Health:")
                        print(game.players[1].health)
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        # print(field_map)
                else:
                    self.thread.stop()
                    game.projectiles[self.player_id] = None
                    field_map[int(self.positionX)][(int(self.positionY))] = None
                    print(field_map)
            except:
                self.thread.stop()
                game.projectiles[self.player_id] = None
                field_map[int(self.positionX)][(int(self.positionY))] = None
        elif self.direction == 'left':
            try:
                if field_map[int(self.positionX) - 1][(int(self.positionY))] == None:
                    try:
                        self.set_x(int(self.positionX) - 1)
                        field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                        field_map[int(self.positionX) + 1][(int(self.positionY))] = None
                    except:
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        print(field_map)
                elif field_map[int(self.positionX) - 1][(int(self.positionY))]['type'] == 'player':
                    if game.players[0].name == field_map[int(self.positionX) - 1][(int(self.positionY))]['name']:
                        game.players[0].damage_taken()
                        field_map[int(game.players[0].positionX)][(int(game.players[0].positionY))] = game.players[0].object_to_dict()
                        print("Health:")
                        print(game.players[0].health)
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        print(field_map)
                    elif game.players[1].name == field_map[int(self.positionX) + 1][(int(self.positionY))]['name']:
                        game.players[1].damage_taken()
                        field_map[int(game.players[1].positionX)][(int(game.players[1].positionY))] = game.players[1].object_to_dict()
                        print("Health:")
                        print(game.players[1].health)
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        print(field_map)
                else:
                    self.thread.stop()
                    game.projectiles[self.player_id] = None
                    field_map[int(self.positionX)][(int(self.positionY))] = None
                    print(field_map)
            except:
                self.thread.stop()
                game.projectiles[self.player_id] = None
                field_map[int(self.positionX)][(int(self.positionY))] = None
        elif self.direction == 'up':
            try:
                if field_map[int(self.positionX)][(int(self.positionY) -1)] == None:
                    try:
                        self.set_y(int(self.positionY) - 1)
                        field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                        field_map[int(self.positionX)][(int(self.positionY)) + 1] = None
                    except:
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        print(field_map)
                elif field_map[int(self.positionX)][(int(self.positionY) - 1)]['type'] == 'player':
                    if game.players[0].name == field_map[int(self.positionX)][(int(self.positionY) - 1)]['name']:
                        game.players[0].damage_taken()
                        field_map[int(game.players[0].positionX)][(int(game.players[0].positionY))] = game.players[0].object_to_dict()
                        print("Health:")
                        print(game.players[0].health)
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        print(field_map)
                    elif game.players[1].name == field_map[int(self.positionX)][(int(self.positionY) - 1)]['name']:
                        game.players[1].damage_taken()
                        field_map[int(game.players[1].positionX)][(int(game.players[1].positionY))] = game.players[1].object_to_dict()
                        print("Health:")
                        print(game.players[1].health)
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        print(field_map)
                else:
                    self.thread.stop()
                    game.projectiles[self.player_id] = None
                    field_map[int(self.positionX)][(int(self.positionY))] = None
                    print(field_map)
            except:
                self.thread.stop()
                game.projectiles[self.player_id] = None
                field_map[int(self.positionX)][(int(self.positionY))] = None
        elif self.direction == 'down':
            try:
                if field_map[int(self.positionX)][(int(self.positionY) + 1)] == None:
                    try:
                        self.set_y(int(self.positionY) + 1)
                        field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                        field_map[int(self.positionX)][(int(self.positionY)) - 1] = None
                    except:
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        print(field_map)
                elif field_map[int(self.positionX)][(int(self.positionY) + 1)]['type'] == 'player':
                    if game.players[0].name == field_map[int(self.positionX)][(int(self.positionY) + 1)]['name']:
                        game.players[0].damage_taken()
                        field_map[int(game.players[0].positionX)][(int(game.players[0].positionY))] = game.players[0].object_to_dict()
                        print("Health:")
                        print(game.players[0].health)
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        print(field_map)
                    elif game.players[1].name == field_map[int(self.positionX) + 1][(int(self.positionY))]['name']:
                        game.players[1].damage_taken()
                        field_map[int(game.players[1].positionX)][(int(game.players[1].positionY))] = game.players[1].object_to_dict()
                        print("Health:")
                        print(game.players[1].health)
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                        print(field_map)
                else:
                    self.thread.stop()
                    game.projectiles[self.player_id] = None
                    field_map[int(self.positionX)][(int(self.positionY))] = None
                    print(field_map)
            except:
                self.thread.stop()
                game.projectiles[self.player_id] = None
                field_map[int(self.positionX)][(int(self.positionY))] = None

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
            
@app.route('/list_games')
def list_games():
    available_games = []
    for key in ongoing_games.keys():
        if len(ongoing_games[key].players) == 1:
            available_games.append(ongoing_games[key])
    return render_template('list_game.html', username = session['username'], ongoing_games = available_games)

@app.route('/list_levels')
def list_levels():
    conn = create_connection()
    cur = conn.cursor()
    levels = cur.execute("SELECT * FROM level").fetchall()
    return render_template('list_level.html', levels = levels)

@app.route('/build_game')
def build_game():
    conn = create_connection()
    cur = conn.cursor()    
    total_levels = cur.execute("SELECT COUNT(id) FROM level WHERE creator_id == ?", ((session['id']), )).fetchone()[0]
    conn.close()
    print("Hello")
    print(total_levels)
    print(total_levels)
    print(total_levels)
    print(total_levels)
    print(total_levels)
    print(total_levels)
    print(total_levels)
    print(total_levels)
    print(total_levels)
    print(total_levels)
    print(total_levels)
    print(total_levels)
    print(total_levels)

    maps_you_can_create = 3

    if total_levels >= maps_you_can_create: #You can only create two maps
        flash(f"Hello {session['username']}, you can only create {maps_you_can_create} maps because of server overload", "info")
        return redirect(url_for('profile'))
    else:
        return render_template('build_game.html')

@app.route('/edit_game/<level_id>')
def edit_game(level_id = None):
    return render_template('edit_game.html', level_id = level_id)
