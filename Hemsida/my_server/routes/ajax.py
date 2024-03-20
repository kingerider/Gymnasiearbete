from my_server import app
from flask import request
import json
from my_server.routes.dbhandler import create_connection
from my_server.routes.game import ongoing_games
from datetime import datetime


# @app.route('/ajax_get_positions', methods = ['POST'])
# def ajax_get_positions():
#     data = request.get_json()
#     game = ongoing_games[data['id']]
#     walls = game.field.get_wall_pos()
#     monsters = game.field.get_monster_pos()
#     items = game.field.get_item_pos()
#     print(f'Walls: {walls}')
#     print(f'Monsters: {monsters}')
#     print(f'Items: {items}')
#     try:
#         return json.dumps({
#             'msg': 'Positions recieved',
#             'success': True,
#             'walls': walls,
#             'monsters': monsters,
#             'items': items
#         })
#     except:
#         return json.dumps({
#             'msg': 'Something went wrong',
#             'success': False
#         })

@app.route('/ajax-search-level', methods = ['POST'])
def ajax_search_level():
    data = request.get_json()
    conn = create_connection()
    cur = conn.cursor()
    levels = cur.execute("SELECT * FROM level WHERE title LIKE ?", (data['input'],)).fetchall()
    conn.close()
    print(levels)
    return json.dumps({
        'msg': 'levels gathered',
        'success': True,
        'levels': levels
    })

@app.route('/ajax-create-level', methods = ['POST'])
def ajax_edit_level():
    data = request.get_json()
    print("data:")
    print(data)
    conn = create_connection()
    cur = conn.cursor()
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')
    username_id = cur.execute("SELECT id FROM user WHERE username LIKE ?", (data['username'],)).fetchone()[0]
    # cur.execute("INSERT INTO level (creator_id, title, player_health, description, date) VALUES (?, ?, ?, ?, ?)", (username_id, data['title'], 3, data['description'], formatted_date))
    cur.execute("INSERT INTO level (creator_id, title, player_health, description, date, play_count) VALUES (?, ?, ?, ?, ?, ?)", (username_id, data['title'], 3, data['description'], formatted_date, 0))
    level_id = cur.execute("SELECT MAX(id) FROM level").fetchone()[0]
    
  
    for i in range(len(data['wallX_Positions'])): #len(data[x]) is as long as len(data[y])
        cur.execute("INSERT INTO wall (level_id, x_coordinate, y_coordinate) VALUES (?, ?, ?)", (level_id, data['wallX_Positions'][i], data['wallY_Positions'][i],))
    for i in range(len(data['monsterX_Positions'])): 
        cur.execute("INSERT INTO enemy (level_id, x_coordinate, y_coordinate) VALUES (?, ?, ?)", (level_id, data['monsterX_Positions'][i], data['monsterY_Positions'][i],))
    
    conn.commit()
    conn.close()

    return json.dumps({
        'msg': 'level added',
        'success': True,
    })

@app.route('/ajax-edit-level', methods = ['POST'])
def ajax_create_level():
    data = request.get_json()
    print("data:")
    print(data)
    conn = create_connection()
    cur = conn.cursor()
    now = datetime.now()

    formatted_date = now.strftime('%Y-%m-%d')
    cur.execute("UPDATE level SET title == ?, player_health == ?, description == ?, date == ? WHERE id == ?", (data['title'], 3, data['description'], formatted_date, data['level_id'], ))
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
    print("data:")
    print(data)
    conn = create_connection()
    cur = conn.cursor()    
    wall_x = cur.execute("SELECT x_coordinate FROM wall WHERE level_id == ?", (data['level_id'], )).fetchall()
    wall_x = [x[0] for x in wall_x]
    wall_y = cur.execute("SELECT y_coordinate FROM wall WHERE level_id == ?", (data['level_id'], )).fetchall()
    wall_y = [y[0] for y in wall_y]
    monster_x = cur.execute("SELECT x_coordinate FROM enemy WHERE level_id == ?", (data['level_id'], )).fetchall()
    monster_x = [x[0] for x in monster_x]
    monster_y = cur.execute("SELECT y_coordinate FROM enemy WHERE level_id == ?", (data['level_id'], )).fetchall()
    monster_y = [y[0] for y in monster_y]
    title = cur.execute("SELECT title FROM level WHERE id == ?", (data['level_id'], )).fetchone()[0]
    description = cur.execute("SELECT description FROM level WHERE id == ?", (data['level_id'], )).fetchone()[0]
    conn.commit()
    conn.close()
    #print(levels)
    return json.dumps({
        'msg': 'sql data',
        'success': True,
        'wallX': wall_x,
        'wallY': wall_y,
        'monsterX': monster_x,
        'monsterY': monster_y,
        'title': title,
        'description': description
    })
