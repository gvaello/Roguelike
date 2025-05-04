class Entity:
    def __init__(self, x, y, char, color, name=None, blocks_path=False, found=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.blocks_path = blocks_path
        self.name = name
        self.found = found

    def move(self, dx, dy):
        self.x += dx
        self.y += dy