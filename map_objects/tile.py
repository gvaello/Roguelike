class Tile:
    def __init__(self, blocked, block_sight=None, explored = False, entity = None):
        self.blocked = blocked
        #By default, if a tile is blocked it should also block the sight
        self.block_sight = block_sight if block_sight is not None else blocked

        self.explored = explored
        self.entity = entity


