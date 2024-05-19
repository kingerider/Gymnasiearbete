from my_server import app
from flask import render_template, redirect, url_for, abort, flash, session, request
from my_server.routes.dbhandler import create_connection
from my_server.routes.route_login import user_logged_in
from my_server.routes.objects import Game, Player, Field
from my_server.routes import ongoing_games
import json

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

#Skapar ett nytt spel som läggs in i ongoing_games och går till play_game_join
@app.route('/play_game/create/<level_id>')
def play_game_create(level_id = None):
    user_logged_in()
    conn = create_connection()
    cur = conn.cursor()
    level = cur.execute("SELECT title, player_health FROM level WHERE id = ?", (level_id, )).fetchone()
    game = Game(level_id, level[0], set_room_id())
    field = Field(level_id, level[1], game.room_id)
    field.load_from_database()
    game.add_field(field)
    game.set_host(session['username'])
    ongoing_games[game.room_id] = game
    conn.close()   
    return redirect(url_for('play_game_join', room_id = game.room_id))

#Skickar spelaren till playgame och tar med game
@app.route('/play_game/join/<room_id>')
def play_game_join(room_id = None):
    user_logged_in()
    game = ongoing_games[room_id]
    if len(game.players) == 0:
        player = Player(session['username'], game.field.health, "right", int(canvasw/tile_size)/8, int(canvash/tile_size)/2)
        game.add_player(player)
    elif len(game.players) == 2:
        flash("Game is full", "warning")
        return redirect(url_for("list_games"))
    else:
        player = Player(session['username'], game.field.health, "left", int(canvasw/tile_size) - (int(canvasw/tile_size)/8) - 1, int(canvash/tile_size)/2)
        game.add_player(player)
        game.place_objects_field()
    return render_template('play_game.html', game = game.get_game_info())

@app.route('/list_levels', methods=['POST', 'GET'])
def list_levels():
    user_logged_in()
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

        list_levels_data = list_levels_j(levels)
        user_id_name = cur.execute("SELECT user.id, user.username FROM user").fetchall()
        conn.close()
        return render_template('list_level.html', levels = levels, user_id_name = user_id_name, levels_data=json.dumps(list_levels_data))
    else:
        user_logged_in()
        conn = create_connection()
        cur = conn.cursor()
        user_id_name = cur.execute("SELECT user.id, user.username FROM user").fetchall()
        levels = cur.execute("SELECT * FROM level").fetchall()
        list_levels_data = list_levels_j(levels)
        conn.close()
        
        return render_template('list_level.html', levels = levels, user_id_name = user_id_name, levels_data=json.dumps(list_levels_data))


def list_levels_j(user_levels):
    conn = create_connection()
    cur = conn.cursor()

    list_user_levels_data = []
    for level in user_levels:
        level_id = level[0]
        wall_x_y = cur.execute("SELECT x_coordinate, y_coordinate FROM wall WHERE level_id == ?", (level[0], )).fetchall()
        wall_x = [x[0] for x in wall_x_y]
        wall_y = [y[1] for y in wall_x_y]
        monster_x_y = cur.execute("SELECT x_coordinate, y_coordinate FROM enemy WHERE level_id == ?", (level[0], )).fetchall()
        monster_x = [x[0] for x in monster_x_y]
        monster_y = [y[1] for y in monster_x_y]

        #Might be needed in the future, for listing 
        #title_description_hearts = cur.execute("SELECT title, description, player_health FROM level WHERE id == ?", (level[0], )).fetchall()[0]
        #title = title_description_hearts[0]
        #description = title_description_hearts[1]
        #hearts = title_description_hearts[2]
        #'title': title,
        #'description': description,
        #'hearts': hearts

        user_levels_data = {
            'levelId': level_id,
            'wallX': wall_x,
            'wallY': wall_y,
            'monsterX': monster_x,
            'monsterY': monster_y
        }
        list_user_levels_data.append(user_levels_data)
    conn.close()
    return list_user_levels_data

@app.route('/list_games')
def list_games():
    user_logged_in()
    available_games = []
    for key in ongoing_games.keys():
        if len(ongoing_games[key].players) == 1:
            available_games.append(ongoing_games[key])
    return render_template('list_game.html', username = session['username'], ongoing_games = available_games)

@app.route('/build_game')
def build_game():
    user_logged_in()
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
    
@app.route('/edit_game/<level_id>')
def edit_game(level_id = None):
    user_logged_in()
    return render_template('edit_game.html', level_id = level_id)