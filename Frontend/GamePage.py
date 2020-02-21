import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from time import sleep
import threading

from SnakeGame.GameLogic import Game
from Backend.Backend import DbProvider
from Backend.ThreadManagement import ThreadWithTrace

from PIL import Image, ImageTk


class GamePage(tk.Frame):
    def setTheme(self, bg):
        self.backgroundColor = "white"
        self.secondBackgroundColor = bg
        self.testColor = "orange"
        self.white = "#FFFFFF"
        self.Table_font = tkfont.Font(family='Helvetica', size=20, weight="bold", slant="italic")

        self.snakeLabel = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("GamePage/snakeMenuLabel.png")))
        self.newGameButtonImage = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("GamePage/newGameButtonImage.png")))
        self.playButtonImage = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("GamePage/playButtonImage.png")))
        self.pauseButtonImage = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("GamePage/pauseButtonImage.png")))

        self.helpMenuButton = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("MenuPage/helpButtonImage.png")))
        self.customButtonImage = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("defaultButtonImage.png")))
        self.menuLabelImage = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("MenuPage/menuLabelImage.png")))
        self.returnButtonImage = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("returnButton.png")))

        self.appleImage = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("GamePage/apple.png")))
        self.bombImage = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("GamePage/bomb.png")))
        self.gameOverImage = ImageTk.PhotoImage(
            Image.open(self.controller.resource_path("GamePage/gameOverImage.png")))

    def createMenu(self, parent):
        menuFrame = tk.Frame(parent, borderwidth=20, background="#FFFFFF")
        tk.Label(menuFrame, text='Database', image=self.snakeLabel, font=self.button_font, bd=10, bg="#F0F0F0").pack(
            fill=tk.BOTH, expand=1)
        self.createSpace(menuFrame, 30).pack(fill=tk.BOTH, expand=1)
        self.customButton(menuFrame, "New Game", self.newGameButtonImage, lambda: self.new_game(20), x=self.x / 4,
                          xmargin=10, bgcolor="#666666", fontcolor="#8BB0F9").pack(expand=False)
        self.customButton(menuFrame, "Play/Pause", self.playButtonImage, lambda: self.toggle_game_state(), x=self.x / 2,
                          xmargin=10, bgcolor="#666666", fontcolor="#8BB0F9", toggle=1).pack(expand=False)
        self.createSpace(menuFrame, 100).pack(fill=tk.BOTH, expand=1)
        self.customButton(menuFrame, "Return", self.returnButtonImage, lambda: self.returnFunction(), x=self.x / 2,
                          xmargin=10, bgcolor="#666666", fontcolor="#8BB0F9").pack(expand=0)
        self.createSpace(menuFrame, 30).pack(fill=tk.BOTH, expand=1)
        return menuFrame

    def createSpace(self, parent, y):
        emptyFrame = tk.LabelFrame(parent, bd=0, bg="white", height=y)
        emptyFrame.pack(fill=tk.BOTH, expand=0)
        return emptyFrame

    # TODO: remove redundancy
    def customButton(self, parent, text, img, comd, x=10, y=1, xmargin=0, ymargin=0, bgcolor="#FFA900",
                     fontcolor="#FFFFFF", toggle=0):
        buttonFrame = tk.LabelFrame(parent, bd=0, bg=self.secondBackgroundColor, width=x, height=y)
        buttonFrame.pack(fill=tk.BOTH, expand=0)

        tk.Grid.rowconfigure(buttonFrame, 0, weight=1)
        tk.Grid.columnconfigure(buttonFrame, 0, weight=1)

        tk.Label(buttonFrame, width=int(x / 7), height=int(ymargin / 2), bg=self.white).pack()  # add space

        button = tk.Button(buttonFrame,
                           text=text,
                           font=self.button_font,
                           padx=10,
                           pady=10,
                           bd=0,
                           image=img,
                           bg=bgcolor,
                           fg=fontcolor,
                           command=comd)  # lambda: self.controller.show_frame(frame))
        if (toggle == 1):
            self.toggleButton = button
        button.pack(expand=1)

        tk.Label(buttonFrame, width=int(x / 7), height=int(ymargin / 2), bg=self.white).pack()  # add space
        return buttonFrame

    def helpButton(self, parent, text, img, x=10, y=1, xmargin=0, ymargin=0, bgcolor="#FFA900", fontcolor="#FFFFFF"):
        def clicked():
            messagebox.showinfo('HELP', 'Aplikacja do obsługi bazy danych.')

        buttonFrame = tk.LabelFrame(parent, bd=0, bg=self.secondBackgroundColor, width=x, height=y)
        buttonFrame.pack(fill=tk.BOTH, expand=0)

        tk.Grid.rowconfigure(buttonFrame, 0, weight=1)
        tk.Grid.columnconfigure(buttonFrame, 0, weight=1)

        tk.Label(buttonFrame, width=int(x / 7), height=int(ymargin / 2), bg=self.white).pack()  # add space

        button = tk.Button(buttonFrame,
                           text=text,
                           font=self.button_font,
                           padx=10,
                           pady=10,
                           bd=0,
                           image=img,
                           bg=bgcolor,
                           fg=fontcolor,
                           command=lambda: clicked())
        button.pack(expand=1)

        tk.Label(buttonFrame, width=int(x / 7), height=int(ymargin / 2), bg=self.white).pack()  # add space
        return buttonFrame

    def gameBoard(self, parent):
        WIDTH = 600
        HEIGHT = 600
        canvas = tk.Canvas(parent, width=WIDTH, height=HEIGHT, background="white", highlightbackground="white")
        return canvas

    def new_game(self, size):
        # end previous game
        if self.controller.t1 != None:
            self.controller.t1.kill()
            self.controller.t1.join()

        self.game_engine = Game(size)
        # self.canvas_snake = []
        self.direction = None
        self.game_canvas.delete(tk.ALL)
        self.display_board()

        self.started = False
        self.pause = True
        self.toggleButton['image'] = self.playButtonImage
        # Start thread for snake to move when direction is set
        self.move()

    def move(self):
        self.controller.t1 = ThreadWithTrace(target=self._move)
        self.controller.t1.start()

    def _move(self):
        while True:
            sleep(0.2)
            if self.started is False and self.pause is False:
                self.started = True
            elif self.started is True and self.game_engine.game_over is False and self.pause is False:
                lock = threading.Lock()
                lock.acquire()
                self.game_engine.preform_move(self.direction)
                self.update_canvas()

                self.game_canvas.after(10)
                lock.release()
            elif self.game_engine.game_over == True:
                result = self.game_engine.snake.body.__len__()
                lock = threading.Lock()
                lock.acquire()
                self.place_image(120, 70, image=self.gameOverImage, anchor="nw")
                self.place_text(300, 180, fill="black", font="Monospace 40 bold",
                                text=result)
                self.game_canvas.after(10)
                lock.release()
                DbProvider().game_log.insert_into_table(result)
                break

    def get_direction(self, event):
        if self.controller.frame.__str__() == "gamepage":
            if event.keycode == 32:
                self.toggle_game_state()
                # if self.pause == False:
            if (event.keycode == 87 or event.keycode == 38) and self.direction != 2:
                self.toggle_game_state(1)
                self.direction = 4
                # print("up")
            elif (event.keycode == 68 or event.keycode == 39) and self.direction != 1:
                self.direction = 3
                self.toggle_game_state(1)
                # print("right")
            elif (event.keycode == 83 or event.keycode == 40) and self.direction != 4:
                self.direction = 2
                self.toggle_game_state(1)
                # print("down")
            elif (event.keycode == 65 or event.keycode == 37) and self.direction != 3:
                self.direction = 1
                self.toggle_game_state(1)
                # print("left")

    def update_canvas(self):
        # TODO: optymalizacja wyswietlania
        field_size = 30
        a = field_size
        b = (field_size * self.game_engine.size) - field_size
        self.game_canvas.delete("head", "tail", "fruits")

        x = self.game_engine.snake.head.x * field_size
        y = self.game_engine.snake.head.y * field_size
        self.place_rectangle(x, y, x + field_size, y + field_size, fill="orange", tags="head")

        for field in self.game_engine.snake.body:
            x = field.x * field_size
            y = field.y * field_size
            if (field.value == 'O'):
                self.place_rectangle(x, y, x + field_size, y + field_size, fill="green", tags="tail")
        for field in self.game_engine.board.fruits:
            x = field.x * field_size
            y = field.y * field_size
            if (field.value == '*'):
                self.place_image(x, y, tags="fruits", image=self.appleImage, anchor="nw")

    def display_board(self):
        field_size = 30  # 30
        a = field_size
        b = (field_size * self.game_engine.size) - field_size
        self.place_rectangle = self.game_canvas.create_rectangle
        self.place_image = self.game_canvas.create_image
        self.place_text = self.game_canvas.create_text
        self.place_rectangle(a, a, b, b, fill="white", tags="background")

        for field in self.game_engine.snake.body:
            x = field.x * field_size
            y = field.y * field_size
            if (field.value == 'D'):
                self.place_rectangle(x, y, x + field_size, y + field_size, fill="orange", tags="head")
            elif (field.value == 'O'):
                self.place_rectangle(x, y, x + field_size, y + field_size, fill="green")

        for field in self.game_engine.board.fruits:
            x = field.x * field_size
            y = field.y * field_size
            if (field.value == '*'):
                self.place_image(x, y, tags="fruits", image=self.appleImage, anchor="nw")

    def toggle_game_state(self, value=0):
        if self.pause == True and (value == 1 or value == 0):
            self.pause = False
            self.toggleButton['image'] = self.pauseButtonImage
        elif self.pause == False and (value == 2 or value == 0):
            self.pause = True
            self.toggleButton['image'] = self.playButtonImage

    def returnFunction(self):
        self.toggle_game_state(2)
        self.controller.show_frame("Menu")

    def __str__(self):
        return "gamepage"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=500, height=200)
        self.controller = controller
        self.parent = parent
        # self.setColors("#110E0A")
        self.setTheme("#FFFFFF")

        self.configure(bg=self.backgroundColor)
        self.button_font = tkfont.Font(family='Helvetica', size=16, weight="bold", slant="italic")

        self.x = self.winfo_reqwidth()
        self.y = self.winfo_reqheight()

        self.input_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, background="white")
        self.names = {}
        self.game_canvas = self.gameBoard(self.input_frame)
        self.game_canvas.pack()
        self.game_canvas.focus_set()
        controller.bind("<Key>", self.get_direction)

        self.input_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)

        content_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, background="white")
        self.createMenu(content_frame).pack(fill=tk.Y, expand=0)

        content_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)

        self.new_game(20)
