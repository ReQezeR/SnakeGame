from random import randint
from SnakeGame.Field import Field


class Board:
    def __init__(self, size):
        self.sizeXY = int(size)
        self.matrix = [[Field(i, j, False, ' ') for j in range(self.sizeXY)] for i in range(self.sizeXY)]
        self.fruits = []

    def print(self):
        for row in self.matrix:
            for field in row:
                print(field, end="")
            print(" ")

    def change_value(self, x, y, value):
        self.matrix[x][y].change_value(value)

    def generate(self, snake):
        r = self.sizeXY
        temp_board = self.matrix
        for i in range(r):
            for j in range(r):
                if i == 0 or i == r - 1:
                    temp_board[i][j].value = 'X'
                elif j == 0 or j == r - 1:
                    temp_board[i][j].value = 'X'
                elif i == snake.px and j == snake.py:
                    temp_board[i][j].value = 'D'
                else:
                    temp_board[i][j].value = ' '
                temp_board[i][j].x = i
                temp_board[i][j].y = j
        self.matrix = temp_board

    def placeFruit(self, fruit):
        x = randint(1, self.sizeXY-2)
        y = randint(1, self.sizeXY-2)
        if self.matrix[x][y].value == ' ':
            self.matrix[x][y].value = fruit
            self.fruits.append(self.matrix[x][y])

