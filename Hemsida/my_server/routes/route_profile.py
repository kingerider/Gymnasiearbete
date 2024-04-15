from my_server import app
from flask import render_template, session
from my_server.routes.dbhandler import create_connection
from my_server.routes.route_login import user_logged_in
from my_server.routes.game import list_levels_j
import json
@app.route('/profile')
def profile():
    user_logged_in()
    conn = create_connection()
    cur = conn.cursor()
    inlogged_user = cur.execute("SELECT * FROM user WHERE id = ?", (session['id'], )).fetchone()
    user_levels = cur.execute("SELECT * FROM level WHERE creator_id = ?", (session['id'], )).fetchall()
    list_user_levels_data = list_levels_j(user_levels)
    conn.close()

    return render_template('profile.html', user = inlogged_user, levels = user_levels, levels_data=json.dumps(list_user_levels_data))