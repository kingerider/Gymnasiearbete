from my_server.routes.dbhandler import create_connection

class Player: 
    def __init__(self, name, health):
        self.name = name
        self.positionX = None
        self.positionY = None
        self.health = health
    
    def __repr__(self):
        print(self.name)
    
    def moveTo(self, newPosX, newPosY):
        self.positionX = newPosX
        self.positionY = newPosY
    
    def damage_taken(self):
        self.health -= 1
        if self.health == 0:
            pass

class Enemy:
    def __init__(self, id, level_id, posX, posY):
        self.id = id,
        self.level_id = level_id,
        self.positionX = posX,
        self.positionY = posY
    
    #def get_x(self):
    #    return self.positionX
    
    #def get_y(self):
    #    return self.positionY

class Wall:
    def __init__(self, id, level_id, posX, posY):
        self.id = id,
        self.level_id = level_id,
        self.positionX = posX,
        self.positionY = posY

class Item:
    def __init__(self, id, level_id, posX, posY, type):
        self.id = id,
        self.level_id = level_id,
        self.positionX = posX,
        self.positionY = posY,
        self.type = type

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
            self.walls.append(Wall(wall[0], wall[1], wall[2], wall[3]))
        fetched_enemies = cur.execute("SELECT * FROM enemy WHERE level_id = ?", (self.id, )).fetchall()
        for enemy in fetched_enemies:
            self.enemies.append(Enemy(enemy[0], enemy[1], enemy[2], enemy[3]))
        fetched_items = cur.execute("SELECT * FROM item WHERE level_id = ?", (self.id, )).fetchall()
        for item in fetched_items:
            self.items.append(Item(item[0], item[1], item[2], item[3], item[4]))


    def place_player(self, player):
        pass

    def get_monster_pos(self):
        list_of_positions = []
        for enemy in self.enemies:
            list_of_positions.append({
                'x': enemy.positionX,
                'y': enemy.positionY
            })
        return list_of_positions
