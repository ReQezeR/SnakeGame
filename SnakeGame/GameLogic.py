from SnakeGame.Board import Board
from SnakeGame.Snake import Snake


class Game:
    def __init__(self, size):
        self.size = int(size)
        self.px = int(self.size / 2)
        self.py = int(self.size / 2)
        self.snake = Snake(self.px, self.py)
        self.board = Board(self.size)
        self.board.generate(self.snake)
        self.latency = 0.25
        self.mov_counter = 1
        self.game_over = False
        self.owoc = '*'

    def move(self, x, y, xd=0, yd=0):
        def update(x, y, xd=0, yd=0):
            self.board.change_value(x, y, 'O')
            self.board.change_value(x + xd, y + yd, 'D')
            self.snake.append(self.board.matrix[x + xd][y + yd])
            self.mov_counter = self.mov_counter + 1
            if self.mov_counter % 15 == 0:
                self.board.placeFruit(self.owoc)  # umieszczanie owocow

        next_field = self.board.matrix[x + xd][y + yd]
        if next_field.value == 'X':
            pass
        elif next_field.value == 'O' or next_field.value == 'D':
            self.game_over = True
            pass
        elif next_field.value == self.owoc:  # czy owoc
            update(x, y, xd=xd, yd=yd)
            self.board.fruits.remove(next_field)
            self.snake.increase_size()
        else:
            update(x, y, xd=xd, yd=yd)

    """ Praca krokowa ( do integracji z interfejsem ) """
    def preform_move(self, ruch):
        if not self.game_over and ruch is not None:
            board = self.board.matrix  # przypisanie tablicy
            head = self.snake.head
            if (board[head.x - 1][head.y].flag and board[head.x + 1][head.y].flag and board[head.x][head.y - 1].flag
                    and board[head.x][head.y + 1].flag):
                self.game_over = True
            else:
                if ruch == 1:
                    self.move(head.x, head.y, xd=-1)
                elif ruch == 2:
                    self.move(head.x, head.y, yd=1)
                elif ruch == 3:
                    self.move(head.x, head.y, xd=1)
                elif ruch == 4:
                    self.move(head.x, head.y, yd=-1)

                # Usuwanie nadmiarowych segmentow sneaka
                if self.snake.body.__len__() > self.snake.max_size:
                    self.board.change_value(self.snake.tail.x, self.snake.tail.y, ' ')  # aktualizacja tablicy
                    self.snake.cut_off_tail()  # odciecie ogona




