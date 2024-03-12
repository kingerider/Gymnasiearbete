from my_server.routes.dbhandler import create_connection
from my_server.routes.game import ongoing_games, player_taken_damage
import random
import threading

canvasw = 800
canvash = 400
tile_size = 20



class Game:
    def __init__(self, id, name, room_id):
        self.id = id
        self.name = name
        self.awaiting_players = True
        self.players = []
        self.projectiles = [None, None]
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
            dict_wall = dict(type= "wall")
            self.field_map[wall.positionX][wall.positionY] = dict_wall
        for monster in self.field.enemies:
            dict_monster = dict(type="enemy")
            self.field_map[monster.positionX][monster.positionY] = dict_monster
        for item in self.field.items:
            dict_item = dict(type="item", type_of_item = item.type)
            self.field_map[item.positionX][item.positionY] = item
        #for x in range(0, self.field.tile_size):
            #for y in range(0, self.field.tile_size):
                #if self.field_map[x][y] != None:
                    #self.field_map[x][y] = None
        dict_player1 = dict(type = "player", name = self.players[0].name, direction = self.players[0].direction, health = self.players[0].health)
        dict_player2 = dict(type = "player", name = self.players[1].name, direction = self.players[1].direction, health = self.players[1].health)
        self.field_map[int(self.players[0].positionX)][int(self.players[0].positionY)] = dict_player1
        self.field_map[int(self.players[1].positionX)][int(self.players[1].positionY)] = dict_player2

    def add_player(self, player):
        self.players.append(player)
        if len(self.players) == 2:
            self.awaiting_players = False 
    
    def get_game_info(self):
        
        if self.awaiting_players == True:
            name_list = [self.players[0].name]    
        else:
            name_list = [self.players[0].name, self.players[1].name]
        dict_game = dict(id = self.id, name = self.name, awaiting_players = self.awaiting_players, players = name_list, field_map = self.field_map, room_id = self.room_id)
        print(dict_game)
        return dict_game
    
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
        self.positionX = posX
        self.positionY = posY
    
    def set_x(self, posX):
        self.positionX = posX
    
    def set_y(self, posY):
        self.positionY = posY

class Player(Entity): 
    def __init__(self, name, health, direction, posX, posY):
        self.name = name
        self.health = health
        self.direction = direction
        super().__init__(posX, posY)

    def moveTo(self, newPosX, newPosY):
        self.set_position(newPosX, newPosY)
    
    def damage_taken(self):
        if self.health >= 1:
            self.health -= 1

class Enemy(Entity):
    def __init__(self, id, level_id, posX, posY):
        self.id = id
        self.level_id = level_id
        self.direction = None
        # self.t = threading.Timer(0.2)
        super().__init__(posX, posY)

    def change_direction(self, str):
        self.direction = str

    def moveTo(self, newPosX, newPosY):
        self.set_position(newPosX, newPosY)

    def monster_move(data):

        game = ongoing_games[data['room']]
        monsters = game.field.enemies
        positions = game.field_map
        players = game.players

        for monster in monsters:

            movementChoose = 0
            x = monster.positionX
            y = monster.positionY
            dict_monster = dict(type="enemy")
            #how close is player, if player is within 5 tiles don't do random action
            #if(5*tileSize > (playerX - monsterArray[j].getX()) and -5*tileSize < (playerX - monsterArray[j].getX()) && 5*tileSize > (playerY - monsterArray[j].getY()) && -5*tileSize < (playerY - monsterArray[j].getY())){
            #movementChoose = 1;
            if(False):
                pass
            else:
                movementChoose = random.randint(1, 4)
            #Left
            if movementChoose == 1:
                #Check if movement available
                try:
                    if positions[int(x - 1)][(int(y))] == None:
                        positions[int(x - 1)][(int(y))] = dict_monster
                        positions[int(x)][(int(y))] = None
                        monster.positionX -= 1
                    elif positions[int(x - 1)][(int(y))]['type'] == 'player':
                        player_taken_damage(players, positions, x, y)
                        # for player in players:
                        #     if player.name == positions[int(x - 1)][(int(y))]['name']:
                        #         player.damage_taken()
                        #         print(f'{player.name} tog skada')
                except:
                    print("Ajabaja, kan inte röra dig dära lillen")

            #Right
            elif movementChoose == 2:
                #Check if movement available
                try:
                    if positions[int(x + 1)][(int(y))] == None:
                        positions[int(x + 1)][(int(y))] = dict_monster
                        positions[int(x)][(int(y))] = None
                        monster.positionX += 1
                    elif positions[int(x + 1)][(int(y))]['type'] == 'player':
                        player_taken_damage(players, positions, x, y)
                        # for player in players:
                        #     if player.name == positions[int(x + 1)][(int(y))]['name']:
                        #         player.damage_taken()
                        #         print(f'{player.name} tog skada')
                except:
                    print("Ajabaja, kan inte röra dig dära lillen")
            #Up
            elif movementChoose == 3:
                #Check if movement available
                try:
                    if positions[int(x)][(int(y - 1))] == None:
                        positions[int(x)][(int(y - 1))] = dict_monster
                        positions[int(x)][(int(y))] = None
                        monster.positionY -= 1
                    elif positions[int(x)][(int(y - 1))]['type'] == 'player':
                        player_taken_damage(players, positions, x, y)
                        # for player in players:
                        #     if player.name == positions[int(x)][(int(y - 1))]['name']:
                        #         player.damage_taken()
                        #         print(f'{player.name} tog skada')
                except:
                    print("Ajabaja, kan inte röra dig dära lillen")
            #Down
            elif movementChoose == 4:
                #Check if movement available
                try:
                    if positions[int(x)][(int(y + 1))] == None:
                        positions[int(x)][(int(y + 1))] = dict_monster
                        positions[int(x)][(int(y))] = None
                        monster.positionY += 1
                    elif positions[int(x)][(int(y + 1))]['type'] == 'player':
                        player_taken_damage(players, positions, x, y)
                        # for player in players:
                        #     if player.name == positions[int(x)][(int(y + 1))]['name']:
                        #         player.damage_taken()
                        #         print(f'{player.name} tog skada')
                except:
                    print("Ajabaja, kan inte röra dig dära lillen")
    

class Wall(Entity):
    def __init__(self, id, level_id, posX, posY):
        self.id = id
        self.level_id = level_id
        super().__init__(posX, posY)

class Item(Entity):
    def __init__(self, id, level_id, posX, posY, type):
        self.id = id
        self.level_id = level_id
        super().__init__(posX, posY)
        self.type = type

class Projectile(Entity):
    def __init__(self, posX, posY, dir, id):
        super().__init__(posX, posY)
        self.direction = dir
        self.player_id = id
    
    def object_to_dict(self):
        return dict(type = 'projectile', player_id = self.player_id, direction = self.direction)

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