from random import randint, choice
from tcod import libtcodpy
from entity import Entity
from map_objects.rectangle import Rectangle
from map_objects.tile import Tile

class GameMap:
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range (self.map_height)] for x in range (self.map_width)]
        return tiles

    def make_map(self, dungeon, player):
        rooms = []
        number_of_rooms = 0

        for room in range (dungeon.max_rooms -1):
            w = randint(dungeon.room_min_size, dungeon.room_max_size)
            h = randint(dungeon.room_min_size, dungeon.room_max_size)
            x = randint(0, self.map_width - w -1)
            y = randint(0, self.map_height - h -1)
            new_room = Rectangle(x, y, w, h)
            intersect:bool = False

            for other_room in rooms:
                if new_room.intersects(other_room):
                    intersect = True
                    break

            if not intersect:
                if self.create_room(new_room):
                    (new_x, new_y) = new_room.center()
                    if number_of_rooms == 0:
                        player.x = new_x
                        player.y = new_y
                    else:
                        (prev_x, prev_y) = rooms[number_of_rooms-1].center()
                        if randint(0, 1) == 1:
                            self.create_h_tunnel(prev_x, new_x, prev_y)
                            self.create_v_tunnel(prev_y, new_y, new_x)
                        else:
                            self.create_v_tunnel(prev_y, new_y, prev_x)
                            self.create_h_tunnel(prev_x, new_x, new_y)

                    self.place_entity(new_room, dungeon)
                    rooms.append(new_room)
                    number_of_rooms += 1


    def create_h_tunnel(self, x1, x2, y):
        x1 = int(x1)
        x2 = int(x2)
        y = int(y)

        for x in range (min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        y1 = int(y1)
        y2 = int(y2)
        x = int(x)

        for y in range (min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_room(self, room)->bool:
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
        return True

    def is_blocked(self, x, y):
        return self.tiles[x][y].blocked or (self.tiles[x][y].entity is not None and self.tiles[x][y].entity.blocks_path)


    def place_entity(self, room, dungeon):
        number_of_enemies = randint(0, dungeon.max_enemies_per_room)
        for i in range (number_of_enemies):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in dungeon.entities if (int(entity.x) == x and int(entity.y) == y)]):
                if randint(0, 100)< 80:
                    monster = Entity(int(x), int(y) , 'o', libtcodpy.desaturated_green, 'Orc', blocks_path=True)
                else:
                    monster = Entity(int(x), int(y) , 's', libtcodpy.darker_green, 'Slime', blocks_path=True)

                self.tiles[x][y].entity = monster
                dungeon.entities.append(monster)