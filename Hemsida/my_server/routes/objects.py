from my_server.routes.dbhandler import create_connection

class Player: 
    def __init__(self, name, health):
        self.name = name
        self.positionX = None
        self.positionY = None
        self.health = health
    
    def moveTo(self, newPosX, newPosY):
        self.positionX = newPosX
        self.positionY = newPosY
    
    def damage_taken(self):
        self.health -= 1
        if self.health == 0:
            pass


class Field:
    def __init__(self, id):
        self.id = id
        self.walls = []
        self.enemies = []
        self.items = []
    
    def load_from_database(self):
        cur = create_connection().cursor()
        fetched_walls = cur.execute("SELECT * FROM wall WHERE level_id = ?", (self.id, )).fetchall()
        for wall in fetched_walls:
            self.walls.append(wall)
        fetched_enemies = cur.execute("SELECT * FROM enemy WHERE level_id = ?", (self.id, )).fetchall()
        for enemy in fetched_enemies:
            self.enemies.append(enemy)
        fetched_items = cur.execute("SELECT * FROM item WHERE level_id = ?", (self.id, )).fetchall()
        for item in fetched_items:
            self.items.append(item)


    def place_player(self, player):
        pass