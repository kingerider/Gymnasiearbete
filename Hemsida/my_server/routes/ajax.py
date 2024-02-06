from my_server import app
from flask import request
import json
from my_server.routes.game import ongoing_games

@app.route('/ajax_get_positions', methods = ['POST'])
def ajax_get_positions():
    data = request.get_json()
    game = ongoing_games[data['id']]
    walls = game.field.get_wall_pos()
    monsters = game.field.get_monster_pos()
    items = game.field.get_item_pos()
    print(walls)
    print(monsters)
    print(items)
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