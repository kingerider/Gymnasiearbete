from my_server import app
from flask import render_template, redirect, url_for, flash, session
from my_server.routes.dbhandler import create_connection

@app.route('/edit-game')
def edit_game():
    pass


@app.route('/play-game')
def play_game():
    pass
