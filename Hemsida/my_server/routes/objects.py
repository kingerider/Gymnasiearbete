from my_server.routes import ongoing_games
from my_server.routes.dbhandler import create_connection
from threading import Thread, Event
import time
import random

canvasw = 800
canvash = 400
tile_size = 20

class Game:
    def __init__(self, id, name, room_id):
        self.id = id
        self.name = name
        self.host = None
        self.awaiting_players = True
        self.players = []
        self.projectiles = [None, None]
        self.field = None
        self.field_map = []
        self.room_id = room_id
        
        for i in range(int(canvasw/tile_size)):
            self.field_map.append([])
            for j in range(int(canvash/tile_size)):
                self.field_map[i].append(None)
    
    def add_field(self, field):
        self.field = field
    
    def set_host(self, host):
        self.host = host
    
    def place_objects_field(self):
        for wall in self.field.walls:
            dict_wall = dict(type= "wall")
            self.field_map[wall.positionX][wall.positionY] = dict_wall
        for monster in self.field.enemies:
            dict_monster = dict(type="enemy")
            self.field_map[monster.positionX][monster.positionY] = dict_monster
        self.field_map[int(self.players[0].positionX)][int(self.players[0].positionY)] = self.players[0].object_to_dict()
        self.field_map[int(self.players[1].positionX)][int(self.players[1].positionY)] = self.players[1].object_to_dict()

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
        return dict_game
    

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
    
    def object_to_dict(self):
        return dict(type = "player", name = self.name, direction = self.direction, health = self.health)
    
    def damage_taken(self):
        if self.health >= 1:
            self.health -= 1

class EnemyThread(Thread):
    def __init__(self, enemy):
        Thread.__init__(self)
        self._stop_event = Event()
        self.enemy = enemy
        self.directions = ['right', 'left', 'up', 'down']
    
    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            self.enemy.move(ongoing_games[self.enemy.room_id])
            time.sleep(0.2)

class Enemy(Entity):
    def __init__(self, id, level_id, posX, posY, dir, room_id):
        super().__init__(posX, posY)
        self.id = id
        self.level_id = level_id
        self.room_id = room_id
        self.direction = dir
        self.thread = EnemyThread(self)
    
    def start_thread(self):
        self.thread.start()
    
    def object_to_dict(self):
        return dict(type="enemy")
    
    def change_direction(self, str):
        self.direction = str

    def move(self, game):
        field_map = game.field_map
        dir = self.thread.directions[random.randint(0, 3)]
        try:
            if self.direction == 'right':
                self.change_direction(dir)
                if field_map[int(self.positionX) + 1][(int(self.positionY))] == None:
                    self.set_x(int(self.positionX) + 1)
                    field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                    field_map[int(self.positionX) - 1][(int(self.positionY))] = None
                elif field_map[int(self.positionX) + 1][(int(self.positionY))]['type'] == 'player':
                    x = int(self.positionX) + 1
                    y = int(self.positionY)
                    players = game.players
                    for player in players:
                        if player.name == field_map[int(x)][(int(y))]['name']:
                            player.damage_taken()
                            field_map[int(x)][(int(y))] = player.object_to_dict()
            elif self.direction == 'left':
                self.change_direction(dir)
                if field_map[int(self.positionX) - 1][(int(self.positionY))] == None:
                    self.set_x(int(self.positionX) - 1)
                    field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                    field_map[int(self.positionX) + 1][(int(self.positionY))] = None
                elif field_map[int(self.positionX) - 1][(int(self.positionY))]['type'] == 'player':
                    x = int(self.positionX) - 1
                    y = int(self.positionY)
                    players = game.players
                    for player in players:
                        if player.name == field_map[int(x)][(int(y))]['name']:
                            player.damage_taken()
                            field_map[int(x)][(int(y))] = player.object_to_dict()
            elif self.direction == 'up':
                self.change_direction(dir)
                if field_map[int(self.positionX)][(int(self.positionY) - 1)] == None:
                    self.set_y(int(self.positionY) - 1)
                    field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                    field_map[int(self.positionX)][(int(self.positionY) + 1)] = None
                elif field_map[int(self.positionX)][(int(self.positionY) - 1)]['type'] == 'player':
                    x = int(self.positionX)
                    y = int(self.positionY) - 1
                    players = game.players
                    for player in players:
                        if player.name == field_map[int(x)][(int(y))]['name']:
                            player.damage_taken()
                            field_map[int(x)][(int(y))] = player.object_to_dict()
            elif self.direction == 'down':
                self.change_direction(dir)
                if field_map[int(self.positionX)][(int(self.positionY) + 1)] == None:
                    self.set_y(int(self.positionY) + 1)
                    field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                    field_map[int(self.positionX)][(int(self.positionY) - 1)] = None
                elif field_map[int(self.positionX)][(int(self.positionY) + 1)]['type'] == 'player':
                    x = int(self.positionX)
                    y = int(self.positionY) + 1
                    players = game.players
                    for player in players:
                        if player.name == field_map[int(x)][(int(y))]['name']:
                            player.damage_taken()
                            field_map[int(x)][(int(y))] = player.object_to_dict()
        except:
            print("Monster out of bounds")

class Wall(Entity):
    def __init__(self, id, level_id, posX, posY):
        self.id = id
        self.level_id = level_id
        super().__init__(posX, posY)



class Field:
    def __init__(self, id, health, room_id):
        self.id = id
        self.room_id = room_id
        self.health = health
        self.walls = []
        self.enemies = []

    
    def load_from_database(self):
        conn = create_connection()
        cur = conn.cursor()
        directions = ['right', 'left', 'up', 'down']
        fetched_walls = cur.execute("SELECT * FROM wall WHERE level_id = ?", (self.id, )).fetchall()
        for wall in fetched_walls:
            self.walls.append(Wall(wall[0], wall[1], wall[2], wall[3]))
        fetched_enemies = cur.execute("SELECT * FROM enemy WHERE level_id = ?", (self.id, )).fetchall()
        for enemy in fetched_enemies:
            self.enemies.append(Enemy(enemy[0], enemy[1], enemy[2], enemy[3], directions[random.randint(0, 3)], self.room_id))
        conn.close()
    
    def start_monsters(self):
        for enemy in self.enemies:
            enemy.start_thread()
    
    def stop_monsters(self):
        for enemy in self.enemies:
            enemy.thread.stop()

class BulletThread(Thread):

    def __init__(self, bullet):
        Thread.__init__(self)
        self._stop_event = Event()
        self.bullet = bullet
    
    def stop(self):
        self._stop_event.set()

    def run(self):
        time.sleep(0.1)
        while not self._stop_event.is_set():
            self.bullet.move(ongoing_games[self.bullet.room_id])
            time.sleep(0.05)

class Projectile(Entity):
    def __init__(self, posX, posY, dir, id, ri):
        super().__init__(posX, posY)
        self.direction = dir
        self.player_id = id
        self.room_id = ri
        self.thread = BulletThread(self)
        self.thread.start()
        
    def object_to_dict(self):
        return dict(type = 'projectile', player_id = self.player_id, direction = self.direction)

    def move(self, game):
        field_map = game.field_map
        if self.thread.is_alive():
            if self.direction == 'right':
                try:
                    if field_map[int(self.positionX) + 1][(int(self.positionY))] == None:
                        try:
                            self.set_x(int(self.positionX) + 1)
                            field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                            field_map[int(self.positionX) - 1][(int(self.positionY))] = None
                        except:
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                    elif field_map[int(self.positionX) + 1][(int(self.positionY))]['type'] == 'player':
                        if game.players[0].name == field_map[int(self.positionX) + 1][(int(self.positionY))]['name']:
                            game.players[0].damage_taken()
                            field_map[int(game.players[0].positionX)][(int(game.players[0].positionY))] = game.players[0].object_to_dict()
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                        elif game.players[1].name == field_map[int(self.positionX) + 1][(int(self.positionY))]['name']:
                            game.players[1].damage_taken()
                            field_map[int(game.players[1].positionX)][(int(game.players[1].positionY))] = game.players[1].object_to_dict()
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                    else:
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                except:
                    self.thread.stop()
                    game.projectiles[self.player_id] = None
                    field_map[int(self.positionX)][(int(self.positionY))] = None
            elif self.direction == 'left':
                try:
                    if field_map[int(self.positionX) - 1][(int(self.positionY))] == None:
                        try:
                            self.set_x(int(self.positionX) - 1)
                            field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                            field_map[int(self.positionX) + 1][(int(self.positionY))] = None
                        except:
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                    elif field_map[int(self.positionX) - 1][(int(self.positionY))]['type'] == 'player':
                        if game.players[0].name == field_map[int(self.positionX) - 1][(int(self.positionY))]['name']:
                            game.players[0].damage_taken()
                            field_map[int(game.players[0].positionX)][(int(game.players[0].positionY))] = game.players[0].object_to_dict()
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                        elif game.players[1].name == field_map[int(self.positionX) + 1][(int(self.positionY))]['name']:
                            game.players[1].damage_taken()
                            field_map[int(game.players[1].positionX)][(int(game.players[1].positionY))] = game.players[1].object_to_dict()
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                    else:
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                except:
                    self.thread.stop()
                    game.projectiles[self.player_id] = None
                    field_map[int(self.positionX)][(int(self.positionY))] = None
            elif self.direction == 'up':
                try:
                    if field_map[int(self.positionX)][(int(self.positionY) -1)] == None:
                        try:
                            self.set_y(int(self.positionY) - 1)
                            field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                            field_map[int(self.positionX)][(int(self.positionY)) + 1] = None
                        except:
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                    elif field_map[int(self.positionX)][(int(self.positionY) - 1)]['type'] == 'player':
                        if game.players[0].name == field_map[int(self.positionX)][(int(self.positionY) - 1)]['name']:
                            game.players[0].damage_taken()
                            field_map[int(game.players[0].positionX)][(int(game.players[0].positionY))] = game.players[0].object_to_dict()
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                        elif game.players[1].name == field_map[int(self.positionX)][(int(self.positionY) - 1)]['name']:
                            game.players[1].damage_taken()
                            field_map[int(game.players[1].positionX)][(int(game.players[1].positionY))] = game.players[1].object_to_dict()
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                    else:
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                except:
                    self.thread.stop()
                    game.projectiles[self.player_id] = None
                    field_map[int(self.positionX)][(int(self.positionY))] = None
            elif self.direction == 'down':
                try:
                    if field_map[int(self.positionX)][(int(self.positionY) + 1)] == None:
                        try:
                            self.set_y(int(self.positionY) + 1)
                            field_map[int(self.positionX)][(int(self.positionY))] = self.object_to_dict()
                            field_map[int(self.positionX)][(int(self.positionY)) - 1] = None
                        except:
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                    elif field_map[int(self.positionX)][(int(self.positionY) + 1)]['type'] == 'player':
                        if game.players[0].name == field_map[int(self.positionX)][(int(self.positionY) + 1)]['name']:
                            game.players[0].damage_taken()
                            field_map[int(game.players[0].positionX)][(int(game.players[0].positionY))] = game.players[0].object_to_dict()
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                        elif game.players[1].name == field_map[int(self.positionX) + 1][(int(self.positionY))]['name']:
                            game.players[1].damage_taken()
                            field_map[int(game.players[1].positionX)][(int(game.players[1].positionY))] = game.players[1].object_to_dict()
                            self.thread.stop()
                            game.projectiles[self.player_id] = None
                            field_map[int(self.positionX)][(int(self.positionY))] = None
                    else:
                        self.thread.stop()
                        game.projectiles[self.player_id] = None
                        field_map[int(self.positionX)][(int(self.positionY))] = None
                except:
                    self.thread.stop()
                    game.projectiles[self.player_id] = None
                    field_map[int(self.positionX)][(int(self.positionY))] = None
        else:
            self.thread.stop()
            game.projectiles[self.player_id] = None
            field_map[int(self.positionX)][(int(self.positionY))] = None