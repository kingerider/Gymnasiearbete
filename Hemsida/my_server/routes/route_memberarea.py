from my_server import app
from flask import render_template
from my_server.routes.dbhandler import create_connection
from my_server.routes.route_login import user_logged_in
from my_server.routes.game import list
import json

@app.route('/memberarea')
def memberarea():
    user_logged_in()
    conn = create_connection()
    cur = conn.cursor()
    levels_play_count = cur.execute("SELECT * FROM level ORDER BY play_count DESC LIMIT 3").fetchall()
    levels_date = cur.execute("SELECT * FROM level ORDER BY date DESC LIMIT 3").fetchall()
    user_id_name = cur.execute("SELECT user.id, user.username FROM user").fetchall()
    levels_play_count_j = list(levels_play_count)
    levels_date_j = list(levels_date)
    print
    conn.close()
    return render_template('memberarea.html', levels_play_count = levels_play_count, levels_play_count_j=json.dumps(levels_play_count_j), levels_date = levels_date, levels_date_j=json.dumps(levels_date_j), user_id_name = user_id_name)
