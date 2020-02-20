from SnakeGame.Field import Field


class Snake:
    def __init__(self, px, py, size=3):
        self.body = [Field(px,py,True,"D")]
        self.max_size = size
        self.head = self.body[-1]
        self.tail = self.body[0]
        self.px = px
        self.py = py

    def __str__(self):
        return self.body

    def increase_size(self, value=1):
        self.max_size = self.max_size + value

    def update_features(self):
        self.head = self.body[-1]
        self.tail = self.body[0]

    def append(self, segment):
        self.body.append(segment)
        self.update_features()

    def cut_off_tail(self):
        self.body.pop(0)
        self.tail = self.body[0]
