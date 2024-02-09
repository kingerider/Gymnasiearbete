from my_server.routes.dbhandler import create_connection

canvasw = 800
canvash = 400
tile_size = 20



class Game:
    def __init__(self, id, name, room_id):
        self.id = id
        self.name = name
        self.awaiting_players = True
        self.players = []
        self.field = None
        self.field_map = [] #[][]

        
        for i in range(int(canvasw/tile_size)):
            self.field_map.append([])
            for j in range(int(canvash/tile_size)):
                self.field_map[i].append(None)
        #field_map[x][y]
        
        self.room_id = room_id
    
    def add_field(self, field):
        self.field = field
    
    def place_objects_field(self):
        for wall in self.field.walls:
            self.field_map[wall.positionX][wall.positionY] = wall
        for monster in self.field.enemies:
            self.field_map[monster.positionX][monster.positionY] = monster
        for item in self.field.items:
            self.field_map[item.positionX][item.positionY] = item
        #for x in range(0, self.field.tile_size):
            #for y in range(0, self.field.tile_size):
                #if self.field_map[x][y] != None:
                    #self.field_map[x][y] = None
        self.field_map[self.players[0].positionX][self.players[0].positionY] = self.players[0]
        self.field_map[self.players[1].positionX][self.players[1].positionY] = self.players[1]

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
        return self.start_game()

class Entity:
    def __init__(self, posX, posY):
        self.positionX = posX,
        self.positionY = posY
    
    def set_x(self, posX):
        self.positionX = posX
    
    def set_y(self, posY):
        self.positionY = posY

class Player(Entity): 
    def __init__(self, name, health):
        self.name = name
        self.health = health
        self.direction = None
    
    def change_direction(self, str):
        self.direction = str

    def moveTo(self, newPosX, newPosY):
        self.set_position(newPosX, newPosY)
    
    def damage_taken(self, game):
        self.health -= 1
        if self.health == 0:
            game.end_game()
        return self.health

class Enemy(Entity):
    def __init__(self, id, level_id, posX, posY):
        self.id = id
        self.level_id = level_id
        self.direction = None

    def change_direction(self, str):
        self.direction = str

    def moveTo(self, newPosX, newPosY):
        self.set_position(newPosX, newPosY)

class Wall(Entity):
    def __init__(self, id, level_id, posX, posY):
        self.id = id,
        self.level_id = level_id,

class Item(Entity):
    def __init__(self, id, level_id, posX, posY, type):
        self.id = id,
        self.level_id = level_id,
        self.type = type

class Field:
    def __init__(self, id, health):
        self.id = id
        self.health = health
        self.walls = []
        self.enemies = []
        self.items = []

        #self.field = [][]
        #self.field[0][5] = Monster()
        #self.field[0][6] = None
        #self.field[5][6] = Wall()

        #Flytta monster ned ett steg.
        #self.field[1][5] = self.field[0][5]
        #self.field[0][5] = None
    
    def load_from_database(self):
        conn = create_connection()
        cur = conn.cursor()
        fetched_walls = cur.execute("SELECT * FROM wall WHERE level_id = ?", (self.id, )).fetchall()
        for wall in fetched_walls:
            self.walls.append(Wall(wall[0], wall[1], wall[2], wall[3]))
        fetched_enemies = cur.execute("SELECT * FROM enemy WHERE level_id = ?", (self.id, )).fetchall()
        for enemy in fetched_enemies:
            self.enemies.append(Enemy(enemy[0], enemy[1], enemy[2], enemy[3]))
        fetched_items = cur.execute("SELECT * FROM item WHERE level_id = ?", (self.id, )).fetchall()
        for item in fetched_items:
            self.items.append(Item(item[0], item[1], item[2], item[3], item[4]))
        conn.close()

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