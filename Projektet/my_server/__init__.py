from flask import Flask
from my_server.config import Config

app = Flask (__name__)
app.config.from_object(Config)

from my_server import routes, error
