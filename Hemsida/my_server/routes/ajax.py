from my_server import app
from flask import request
import json
from my_server.routes.dbhandler import create_connection
from my_server.routes import ongoing_games
from datetime import datetime

@app.route('/ajax-create-level', methods = ['POST'])
def ajax_edit_level():
    data = request.get_json()
    conn = create_connection()
    cur = conn.cursor()
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')
    username_id = cur.execute("SELECT id FROM user WHERE username LIKE ?", (data['username'],)).fetchone()[0]
    # cur.execute("INSERT INTO level (creator_id, title, player_health, description, date) VALUES (?, ?, ?, ?, ?)", (username_id, data['title'], 3, data['description'], formatted_date))
    cur.execute("INSERT INTO level (creator_id, title, player_health, description, date, play_count) VALUES (?, ?, ?, ?, ?, ?)", (username_id, data['title'], data['hearts'], data['description'], formatted_date, 0))
    level_id = cur.execute("SELECT MAX(id) FROM level").fetchone()[0]
    
    for i in range(len(data['wallX_Positions'])): #len(data[x]) is as long as len(data[y])
        cur.execute("INSERT INTO wall (level_id, x_coordinate, y_coordinate) VALUES (?, ?, ?)", (level_id, data['wallX_Positions'][i], data['wallY_Positions'][i],))
    for i in range(len(data['monsterX_Positions'])): 
        cur.execute("INSERT INTO enemy (level_id, x_coordinate, y_coordinate) VALUES (?, ?, ?)", (level_id, data['monsterX_Positions'][i], data['monsterY_Positions'][i],))
    
    conn.commit()
    conn.close()

    return json.dumps({
        'msg': 'Level added',
        'success': True,
    })

@app.route('/ajax-edit-level', methods = ['POST'])
def ajax_create_level():
    data = request.get_json()
    conn = create_connection()
    cur = conn.cursor()
    now = datetime.now()

    formatted_date = now.strftime('%Y-%m-%d')
    cur.execute("UPDATE level SET title == ?, player_health == ?, description == ?, date == ? WHERE id == ?", (data['title'], data['hearts'], data['description'], formatted_date, data['level_id'], ))
    level_id = cur.execute("SELECT MAX(id) FROM level").fetchone()[0]

    cur.execute("DELETE FROM wall WHERE level_id == ?", (data['level_id'],))
    cur.execute("DELETE FROM enemy WHERE level_id == ?", (data['level_id'],))

    for i in range(len(data['wallX_Positions'])): #len(data[x]) is as long as len(data[y])
        cur.execute("INSERT INTO wall (level_id, x_coordinate, y_coordinate) VALUES (?, ?, ?)", (data['level_id'], data['wallX_Positions'][i], data['wallY_Positions'][i],))
    for i in range(len(data['monsterX_Positions'])): 
        cur.execute("INSERT INTO enemy (level_id, x_coordinate, y_coordinate) VALUES (?, ?, ?)", (data['level_id'], data['monsterX_Positions'][i], data['monsterY_Positions'][i],))
    
    conn.commit() 
    conn.close()

    return json.dumps({
        'msg': 'level edited',
        'success': True,
    })

@app.route('/ajax-get-data-level', methods = ['POST'])
def ajax_get_data_level():
    data = request.get_json()
    conn = create_connection()
    cur = conn.cursor()    
    wall_x_y = cur.execute("SELECT x_coordinate, y_coordinate FROM wall WHERE level_id == ?", (data['level_id'], )).fetchall()
    wall_x = [x[0] for x in wall_x_y]
    wall_y = [y[1] for y in wall_x_y]
    monster_x_y = cur.execute("SELECT x_coordinate, y_coordinate FROM enemy WHERE level_id == ?", (data['level_id'], )).fetchall()
    monster_x = [x[0] for x in monster_x_y]
    monster_y = [y[0] for y in monster_x_y]
    title_description_hearts = cur.execute("SELECT title, description, player_health FROM level WHERE id == ?", (data['level_id'], )).fetchall()[0]
    title = title_description_hearts[0]
    description = title_description_hearts[1]
    hearts = title_description_hearts[2]
    conn.close()
    return json.dumps({
        'msg': 'sql data',
        'success': True,
        'wallX': wall_x,
        'wallY': wall_y,
        'monsterX': monster_x,
        'monsterY': monster_y,
        'title': title,
        'description': description,
        'hearts': hearts
    })

@app.route('/ajax-add-played-game', methods= ['POST'])
def ajax_add_played_game():
    data = request.get_json()
    conn = create_connection()
    cur = conn.cursor()
    player1count = cur.execute("SELECT games_played FROM user WHERE username = ?", (data['player1'], )).fetchone()[0]
    player1count += 1
    cur.execute("UPDATE user SET games_played = ? WHERE username = ?", (player1count, data['player1']))
    conn.commit()
    player2count = cur.execute("SELECT games_played FROM user WHERE username = ?", (data['player2'], )).fetchone()[0]
    player2count += 1
    cur.execute("UPDATE user SET games_played = ? WHERE username = ?", (player2count, data['player2']))
    conn.commit()
    conn.close()
    return json.dumps({
        'msg': 'game started successfully',
        'success': True
    })

@app.route('/ajax-win-game', methods = ['POST'])
def ajax_win_game():
    data = request.get_json()
    game = ongoing_games[data['room']]
    if game.players[0].name == data['winner']:
        game.players[0].win()
    elif game.players[1].name == data['winner']:
        game.players[1].win()
    return json.dumps({
        'msg': 'game ended successfully',
        'success': True
    })

@app.route('/ajax-lose-game', methods = ['POST'])
def ajax_lose_game():
    data = request.get_json()
    game = ongoing_games[data['room']]
    if game.players[0].name == data['loser']:
        game.players[0].lose()
    elif game.players[1].name == data['loser']:
        game.players[1].lose()
    return json.dumps({
        'msg': 'game ended successfully',
        'success': True
    })