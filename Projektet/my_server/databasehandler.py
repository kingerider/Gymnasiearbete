import sqlite3
from my_server import app

def create_connection(db_file = app.config['DB_PATH']):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn
