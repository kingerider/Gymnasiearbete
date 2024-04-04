from my_server import app
from flask import render_template, abort, session
from my_server.routes.dbhandler import create_connection


@app.route('/memberarea')
def memberarea():
    if session['logged_in']:
        conn = create_connection()
        cur = conn.cursor()
        levels_play_count = cur.execute("SELECT * FROM level ORDER BY play_count DESC LIMIT 3").fetchall()
        levels_date = cur.execute("SELECT * FROM level ORDER BY date DESC LIMIT 3").fetchall()
        print(levels_play_count)
        print(levels_date)
        conn.close()
        return render_template('memberarea.html', levels_play_count = levels_play_count, levels_date = levels_date)
    abort(401)
