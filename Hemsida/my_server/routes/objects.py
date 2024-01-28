from my_server.routes.dbhandler import create_connection

class Game:
    def __init__(self, room_id):
        self.awaiting_players = True
        self.players = []
        self.field = None
        self.room_id = room_id
    
    def add_field(self, field):
        self.field = field
    
    def add_player(self, player):
        self.players.append(player)
        if len(self.players) == 2:
            self.awaiting_players = False 
    
    def start_game(self):
        if self.awaiting_players == False:
            return True
        return False
    
    def end_game(self):
        self.players = []
        self.awaiting_players = True
        self.start_game()

class Entity:
    def __init__(self):
        self.positionX = None,
        self.positionY = None
    
    def set_position(self, posX, posY):
        self.positionX = posX,
        self.positionY = posY

class Player(Entity): 
    def __init__(self, name, health):
        self.name = name
        self.health = health
    
    def __repr__(self):
        print(self.name)
    
    def moveTo(self, newPosX, newPosY):
        self.set_position(newPosX, newPosY)
    
    def damage_taken(self, game):
        self.health -= 1
        if self.health == 0:
            game.end_game()

class Enemy(Entity):
    def __init__(self, id, level_id, posX, posY):
        self.id = id,
        self.level_id = level_id,
        self.set_position(posX, posY)

class Wall(Entity):
    def __init__(self, id, level_id, posX, posY):
        self.id = id,
        self.level_id = level_id,
        self.set_position(posX, posY)

class Item(Entity):
    def __init__(self, id, level_id, posX, posY, type):
        self.id = id,
        self.level_id = level_id,
        self.set_position(posX, posY),
        self.type = type

class Field:
    def __init__(self, id, name):
        self.id = id,
        self.id = name,
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

    def get_monster_pos(self):
        list_of_positions = []
        for enemy in self.enemies:
            list_of_positions.append({
                'x': enemy.positionX,
                'y': enemy.positionY
            })
        return list_of_positions
    
    def get_wall_pos(self):
        list_of_positions = []
        for wall in self.walls:
            list_of_positions.append({
                'x': wall.positionX,
                'y': wall.positionY
            })
        return list_of_positions
    
    def get_item_pos(self):
        list_of_positions = []
        for item in self.items:
            list_of_positions.append({
                'x': item.positionX,
                'y': item.positionY
            })
        return list_of_positions