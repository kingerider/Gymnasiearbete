from my_server import app
from flask import request
import json
from my_server.routes.dbhandler import create_connection
from my_server.routes.game import ongoing_games

@app.route('/ajax_get_positions', methods = ['POST'])
def ajax_get_positions():
    data = request.get_json()
    game = ongoing_games[data['id']]
    walls = game.field.get_wall_pos()
    monsters = game.field.get_monster_pos()
    items = game.field.get_item_pos()
    print(f'Walls: {walls}')
    print(f'Monsters: {monsters}')
    print(f'Items: {items}')
    try:
        return json.dumps({
            'msg': 'Positions recieved',
            'success': True,
            'walls': walls,
            'monsters': monsters,
            'items': items
        })
    except:
        return json.dumps({
            'msg': 'Something went wrong',
            'success': False
        })

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
def ajax_create_level():
    data = request.get_json()
    print("Hello")
    print(data)
    print(data['title'])
    print(data['discription'])
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO level (title, discription) VALUES (?, ?)", (data['title'], data['discription'],))
    for i in range(len(data['wallXPositions'])):
        cur.execute("INSERT INTO wall (x_coordinate, y_coordinate) VALUES (?, ?)", (data['wallXPositions'], data['wallXPositions'],))
    for i in range(len(data['monsterXPositions'])):
        cur.execute("INSERT INTO monster (x_coordinate, y_coordinate) VALUES (?, ?)", (data['monsterXPositions'], data['monsterXPositions'],))
    

    conn.close()
    #print(levels)
    return json.dumps({
        'msg': 'levels gathered',
        'success': True,
        'levels': data
    })