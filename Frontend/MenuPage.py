import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from PIL import Image, ImageTk


class Menu(tk.Frame):
    def setTheme(self, bg):
        self.backgroundColor = "white"
        self.secondBackgroundColor = bg
        self.testColor = "orange"
        self.white = "#FFFFFF"
        self.Table_font = tkfont.Font(family='Helvetica', size=20, weight="bold", slant="italic")
        self.statisticMenuButton = ImageTk.PhotoImage(Image.open(self.controller.resource_path("StatisticPage/statisticButtonImage.png")))
        self.snakeMenuButton = ImageTk.PhotoImage(Image.open(self.controller.resource_path("MenuPage/snakeButtonImage.png")))
        self.helpMenuButton = ImageTk.PhotoImage(Image.open(self.controller.resource_path("MenuPage/helpButtonImage.png")))
        self.customButtonImage = ImageTk.PhotoImage(Image.open(self.controller.resource_path("defaultButtonImage.png")))
        self.menuLabelImage = ImageTk.PhotoImage(Image.open(self.controller.resource_path("MenuPage/menuLabelImage.png")))

    def createMenu(self, parent):
        main_frame = tk.Frame(parent, borderwidth=20, background="#FFFFFF")
        tk.Label(main_frame, text='MENU:', image=self.menuLabelImage, font=self.button_font, bg="#FFFFFF").pack(
            fill=tk.BOTH)
        self.createSpace(main_frame, 80).pack(fill=tk.BOTH, expand=1)
        self.customButton(main_frame, "Snake", self.snakeMenuButton, "GamePage", x=self.x / 2, xmargin=10,
                          bgcolor="#666666", fontcolor="#8BB0F9").pack(expand=False)
        self.customButton(main_frame, "Statistic", self.statisticMenuButton, "StatisticPage", x=self.x / 2, xmargin=10,
                          bgcolor="#666666", fontcolor="#8BB0F9").pack(expand=False)
        self.createSpace(main_frame, 80).pack(fill=tk.BOTH, expand=1)
        self.helpButton(main_frame, "Creditsy", self.helpMenuButton, x=self.x / 2, xmargin=10, bgcolor="#666666",
                        fontcolor="#8BB0F9").pack(expand=False)
        self.createSpace(main_frame, 30).pack(fill=tk.BOTH, expand=1)
        return main_frame

    def createSpace(self, parent, y):
        temp_frame = tk.LabelFrame(parent, bd=0, bg="white", height=y)
        temp_frame.pack(fill=tk.BOTH, expand=0)
        return temp_frame

    # TODO: remove redundancy
    def customButton(self, parent, text, img, frame="Menu", x=10, y=1, xmargin=0, ymargin=0, bgcolor="#FFA900",
                     fontcolor="#FFFFFF"):
        buttonFrame = tk.LabelFrame(parent, bd=0, bg=self.secondBackgroundColor, width=x, height=y)
        buttonFrame.pack(fill=tk.BOTH, expand=0)

        tk.Grid.rowconfigure(buttonFrame, 0, weight=1)
        tk.Grid.columnconfigure(buttonFrame, 0, weight=1)

        tk.Label(buttonFrame, width=int(x / 7), height=int(ymargin / 2), bg=self.white).pack()  # add space

        tk.Button(buttonFrame,
                  text=text,
                  font=self.button_font,
                  padx=10,
                  pady=10,
                  bd=0,
                  image=img,
                  bg=bgcolor,
                  fg=fontcolor,
                  command=lambda: self.controller.show_frame(frame)).pack(expand=1)

        tk.Label(buttonFrame, width=int(x / 7), height=int(ymargin / 2), bg=self.white).pack()  # add space

        return buttonFrame

    def helpButton(self, parent, text, img, x=10, y=1, xmargin=0, ymargin=0, bgcolor="#FFA900", fontcolor="#FFFFFF"):
        def clicked():
            messagebox.showinfo('HELP', 'Klasyczna gra w snake\'a')

        buttonFrame = tk.LabelFrame(parent, bd=0, bg=self.secondBackgroundColor, width=x, height=y)
        buttonFrame.pack(fill=tk.BOTH, expand=0)

        tk.Grid.rowconfigure(buttonFrame, 0, weight=1)
        tk.Grid.columnconfigure(buttonFrame, 0, weight=1)

        tk.Label(buttonFrame, width=int(x / 7), height=int(ymargin / 2), bg=self.white).pack()  # add space

        tk.Button(buttonFrame,
                  text=text,
                  font=self.button_font,
                  padx=10,
                  pady=10,
                  bd=0,
                  image=img,
                  bg=bgcolor,
                  fg=fontcolor,
                  command=lambda: clicked()).pack(expand=1)
        tk.Label(buttonFrame, width=int(x / 7), height=int(ymargin / 2), bg=self.white).pack()  # add space

        return buttonFrame

    def __str__(self):
        return "menu"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=500, height=200)
        self.controller = controller
        self.parent = parent
        self.setTheme("#FFFFFF")

        self.configure(bg=self.backgroundColor)
        self.button_font = tkfont.Font(family='Helvetica', size=16, weight="bold", slant="italic")

        self.x = self.winfo_reqwidth()
        self.y = self.winfo_reqheight()

        menuFrame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, background="white")
        self.createMenu(menuFrame).pack(fill=tk.Y, expand=0)
        menuFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        placeholderFrame = tk.Frame(self, borderwidth=2, background="gray75")
        placeholderFrame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
