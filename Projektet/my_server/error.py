from my_server import app
from flask import render_template


@app.errorhandler(404)
def not_found_error(error):
    return render_template('/errors/404.html'), 404

@app.errorhandler(403)
def not_found_error(error):
    return render_template('/errors/404.html'), 403

@app.errorhandler(401)
def not_found_error(error):
    return render_template('/errors/404.html'), 401
