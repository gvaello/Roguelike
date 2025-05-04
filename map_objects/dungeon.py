from game_map.game_map import GameMap


class Dungeon:
    def __init__(self, max_rooms, min_rooms, room_max_size, room_min_size):
        self.max_rooms = max_rooms
        self.min_rooms = min_rooms
        self.room_max_size = room_max_size
        self.room_min_size = room_min_size