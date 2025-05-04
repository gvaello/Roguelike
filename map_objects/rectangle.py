class Rectangle:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def center(self):
        center_x = self.x1 + (self.x2 - self.x1) / 2
        center_y = self.y1 + (self.y2 - self.y1) / 2
        return center_x, center_y

    def intersects(self, other):
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1