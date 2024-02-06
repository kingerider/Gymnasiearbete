from my_server import app
from flask import request
import json

@app.route('/ajax_get_positions', methods = ['POST'])
def ajax_get_positions():
    data = request.get_json()
    walls = data['game'].field.get_wall_pos()
    monsters = data['game'].field.get_monster_pos()
    items = data['game'].field.get_item_pos()
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