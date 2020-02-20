class Field:
    def __init__(self, x, y, flag, value):
        self.x = x
        self.y = y
        self.flag = flag  # True = pole niedostepne; False = pole dostepne
        self.value = value

    def __str__(self):
        return " [%d, %d %s] " % (self.x, self.y, self.value)

    def change_value(self, value):
        self.value = value
        if value != ' ':
            self.flag = True
        else:
            self.flag = False
