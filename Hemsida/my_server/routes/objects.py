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
        self.field_map = [] #[][]

        
        for i in range(int(canvasw/tile_size)):
            self.field_map.append([])
            for j in range(int(canvash/tile_size)):
                self.field_map[i].append(None)
        #field_map[x][y]
        
        self.room_id = room_id
    
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
        for item in self.field.items:
            dict_item = dict(type="item", type_of_item = item.type)
            self.field_map[item.positionX][item.positionY] = dict_item
        #for x in range(0, self.field.tile_size):
            #for y in range(0, self.field.tile_size):
                #if self.field_map[x][y] != None:
                    #self.field_map[x][y] = None
        # dict_player1 = dict(type = "player", name = self.players[0].name, direction = self.players[0].direction, health = self.players[0].health)
        # dict_player2 = dict(type = "player", name = self.players[1].name, direction = self.players[1].direction, health = self.players[1].health)
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
        print(dict_game)
        return dict_game
    
    # def start_game(self):
    #     if self.awaiting_players == False:
    #         return True
    #     return False
    
    # def end_game(self):
    #     self.players = []
    #     self.awaiting_players = True
    #     return self.start_game()

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
    
    def object_to_dict(self):
        return dict(type = "player", name = self.name, direction = self.direction, health = self.health)
    
    def damage_taken(self):
        if self.health >= 1:
            self.health -= 1