from my_server import app, socket
from flask import render_template, redirect, url_for, abort, flash, session, request
from flask_socketio import emit, join_room, leave_room
from my_server.routes.dbhandler import create_connection
from my_server.routes.objects import Game, Player, Field, Projectile
from my_server.routes import ongoing_games


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
        #print(ongoing_games)
        ongoing_games[game.room_id] = game
        #print(ongoing_games)
        conn.close()   
        return redirect(url_for('play_game_join', room_id = game.room_id))
    else:
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

@socket.on('leave')
def on_leave(data):
    leave_room(data['room'])
    game = ongoing_games[data['room']]
    if len(game.players) == 1:
        game.players.append(None)
    game.field.stop_monsters()
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

@app.route('/list_levels', methods=['POST', 'GET'])
def list_levels():
    if session['logged_in']:
        if request.method == 'POST':

            data = request.form['sort_level']
          
            conn = create_connection()
            cur = conn.cursor()
            if data == 'Popular':
                levels = cur.execute("SELECT * FROM level ORDER BY play_count DESC").fetchall()
            elif data == 'Least Popular':
                levels = cur.execute("SELECT * FROM level ORDER BY play_count ASC").fetchall()
            elif data == 'Newest':
                levels = cur.execute("SELECT * FROM level ORDER BY date DESC").fetchall()
            elif data == 'Oldest':
                levels = cur.execute("SELECT * FROM level ORDER BY date ASC").fetchall()
            else:
                abort(404)
                
            user_id_name = cur.execute("SELECT user.id, user.username FROM user").fetchall()
            conn.close()
            return render_template('list_level.html', levels = levels, user_id_name = user_id_name)
        else:
            conn = create_connection()
            cur = conn.cursor()
            levels = cur.execute("SELECT * FROM level").fetchall()
            user_id_name = cur.execute("SELECT user.id, user.username FROM user").fetchall()
            conn.close()
            return render_template('list_level.html', levels = levels, user_id_name = user_id_name)
    else:
        abort(401)

@app.route('/build_game')
def build_game():
    if session['logged_in']:
        conn = create_connection()
        cur = conn.cursor()    
        total_levels = cur.execute("SELECT COUNT(id) FROM level WHERE creator_id == ?", ((session['id']), )).fetchone()[0]
        conn.close()

        maps_you_can_create = 3

        if total_levels >= maps_you_can_create: #You can only create two maps
            flash(f"Hello {session['username']}, you can only create {maps_you_can_create} maps because of server overload", "info")
            return redirect(url_for('profile'))
        else:
            return render_template('build_game.html')
    else:
        abort(401)
@app.route('/edit_game/<level_id>')
def edit_game(level_id = None):
    if session['logged_in']:
        return render_template('edit_game.html', level_id = level_id)
    else:
        abort(401)