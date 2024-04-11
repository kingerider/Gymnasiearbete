from my_server import app
from flask import render_template, session
from my_server.routes.dbhandler import create_connection
from my_server.routes.route_login import user_logged_in
import json
@app.route('/profile')
def profile():
    user_logged_in()
    conn = create_connection()
    cur = conn.cursor()
    inlogged_user = cur.execute("SELECT * FROM user WHERE id = ?", (session['id'], )).fetchone()
    user_levels = cur.execute("SELECT * FROM level WHERE creator_id = ?", (session['id'], )).fetchall()

    list_user_levels_data = []
    for level in user_levels:
        level_id = level[0]
        wall_x = cur.execute("SELECT x_coordinate FROM wall WHERE level_id == ?", (level[0], )).fetchall()
        wall_x = [x[0] for x in wall_x]
        wall_y = cur.execute("SELECT y_coordinate FROM wall WHERE level_id == ?", (level[0], )).fetchall()
        wall_y = [y[0] for y in wall_y]
        monster_x = cur.execute("SELECT x_coordinate FROM enemy WHERE level_id == ?", (level[0], )).fetchall()
        monster_x = [x[0] for x in monster_x]
        monster_y = cur.execute("SELECT y_coordinate FROM enemy WHERE level_id == ?", (level[0], )).fetchall()
        monster_y = [y[0] for y in monster_y]
        title = cur.execute("SELECT title FROM level WHERE id == ?", (level[0], )).fetchone()[0]
        description = cur.execute("SELECT description FROM level WHERE id == ?", (level[0], )).fetchone()[0]
        hearts = cur.execute("SELECT player_health FROM level WHERE id == ?", (level[0], )).fetchone()[0]
        user_levels_data = {
            'levelId': level_id,
            'wallX': wall_x,
            'wallY': wall_y,
            'monsterX': monster_x,
            'monsterY': monster_y,
            'title': title,
            'description': description,
            'hearts': hearts
        }
        list_user_levels_data.append(user_levels_data)
    print(list_user_levels_data)
    conn.close()

    return render_template('profile.html', user = inlogged_user, levels = user_levels, levels_data=json.dumps(list_user_levels_data))