from flask import Flask
from flask_socketio import SocketIO
from my_server.config import Config

app = Flask(__name__)

app.config.from_object(Config)
socket = SocketIO(app)

from my_server import routes