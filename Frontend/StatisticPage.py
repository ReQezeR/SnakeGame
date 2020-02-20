import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

from PIL import Image, ImageTk
from pandastable import Table, pd  # pandastable v0.22

""" IMPORTANT
There's this bug in the latest version of pandas (pandas 0.23) that gives you an error on importing pandas.
But this can be easily fixed by installing an earlier version of pandas (pandas 0.22) using the command pip install pandas==0.22 on Windows Command Prompt.
"""


class StatisticPage(tk.Frame):
    def setTheme(self, bg):
        self.backgroundColor = "white"
        self.secondBackgroundColor = bg
        self.testColor = "orange"
        self.white = "#FFFFFF"
        self.Table_font = tkfont.Font(family='Helvetica', size=20, weight="bold", slant="italic")
        self.statisticLabel = ImageTk.PhotoImage(Image.open("Images/StatisticPage/statisticMenuLabel.png"))
        self.helpMenuButton = ImageTk.PhotoImage(Image.open("Images/MenuPage/helpButtonImage.png"))
        self.customButtonImage = ImageTk.PhotoImage(Image.open("Images/defaultButtonImage.png"))

        self.menuLabelImage = ImageTk.PhotoImage(Image.open("Images/MenuPage/menuLabelImage.png"))
        self.returnButtonImage = ImageTk.PhotoImage(Image.open("Images/returnButton.png"))
        self.refreshButtonImage = ImageTk.PhotoImage(Image.open("Images/StatisticPage/refreshButtonImage.png"))

    def createMenu(self, parent):
        main_frame = tk.Frame(parent, borderwidth=20, background="#FFFFFF")
        tk.Label(main_frame, text='Database', image=self.statisticLabel, font=self.button_font, bd=10,
                 bg="#F0F0F0").pack(fill=tk.BOTH, expand=1)
        self.createSpace(main_frame, 30).pack(fill=tk.BOTH, expand=1)
        self.customButton(main_frame, "Refresh", self.refreshButtonImage, lambda: self.callback("GameLog"),
                          x=self.x / 4, xmargin=10, bgcolor="#666666", fontcolor="#8BB0F9").pack(expand=False)
        self.createSpace(main_frame, 240).pack(fill=tk.BOTH, expand=1)
        self.customButton(main_frame, "Return", self.returnButtonImage, lambda: self.controller.show_frame("Menu"),
                          x=self.x / 2, xmargin=10, bgcolor="#666666", fontcolor="#8BB0F9").pack(expand=0)
        self.createSpace(main_frame, 30).pack(fill=tk.BOTH, expand=1)
        return main_frame

    def createSpace(self, parent, y):
        temp_frame = tk.LabelFrame(parent, bd=0, bg="white", height=y)
        temp_frame.pack(fill=tk.BOTH, expand=0)
        return temp_frame

    def configure_grid(self, frame_name, index=0):
        tk.Grid.rowconfigure(frame_name, index, weight=1)
        tk.Grid.columnconfigure(frame_name, index, weight=1)

    # TODO: remove redundancy
    def customButton(self, parent, text, img, command, x=10, y=1, xmargin=0, ymargin=0, bgcolor="#FFA900",
                     fontcolor="#FFFFFF"):
        buttonFrame = tk.LabelFrame(parent, bd=0, bg=self.secondBackgroundColor, width=x, height=y)
        buttonFrame.pack(fill=tk.BOTH, expand=0)
        self.configure_grid(buttonFrame)

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
                  command=command).pack(expand=1)

        tk.Label(buttonFrame, width=int(x / 7), height=int(ymargin / 2), bg=self.white).pack()  # add space
        return buttonFrame

    def helpButton(self, parent, text, img, x=10, y=1, xmargin=0, ymargin=0, bgcolor="#FFA900", fontcolor="#FFFFFF"):
        def clicked():
            messagebox.showinfo('HELP', 'Aplikacja do obsługi bazy danych.')

        buttonFrame = tk.LabelFrame(parent, bd=0, bg=self.secondBackgroundColor, width=x, height=y)
        buttonFrame.pack(fill=tk.BOTH, expand=0)

        self.configure_grid(buttonFrame)

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

    def customPandasTable(self, parent):
        def set_order(cols_order):  # fix kolejnosci kolumn
            x = []
            for i in cols_order:
                x.append(list(df.columns).index(i))
            return x

        tableFrame = tk.LabelFrame(parent, bd=0, bg="#515E5A")
        tableFrame.pack(fill=tk.BOTH, expand=1)
        df = pd.DataFrame(self.dataSet)  # wczytanie danych
        df = df.transpose()  # transpozycja danych ( zamiana wierszy z kolumnami )
        df = df[df.columns[set_order(list(self.dataSet[str(0)].keys()))]]  # fix kolejnosci kolumn

        if 'Result' in df.columns:
            df['Result'] = df['Result'].astype(int)
        if 'ID' in df.columns:
            df['ID'] = df['ID'].astype(int)

        table = Table(tableFrame, dataframe=df, showtoolbar=False, showstatusbar=False)
        table.show()
        return tableFrame

    def callback(self, name=""):
        if name == "GameLog":
            self.dataSet = self.controller.database.get_data_from_table(name)  # wczytanie nowych danych
            self.custom_table.destroy()  # usunięcie starej tabeli
            self.custom_table = self.customPandasTable(self.input_frame)  # stworzenie nowej z aktualnymi danymi
            self.custom_table.pack(fill=tk.BOTH, expand=1)  # rozmieszczenie

    def getCustomData(self):
        for typ, n in self.names.items():
            query = str(n.get())
            if query.__len__() > 10:
                self.dataSet = self.controller.database.custom_select(query)  # wczytanie nowych danych
                self.custom_table.destroy()  # usunięcie starej tabeli
                self.custom_table = self.customPandasTable(self.input_frame)  # stworzenie nowej z aktualnymi danymi
                self.custom_table.pack(fill=tk.BOTH, expand=1)  # rozmieszczenie

    def createButton(self, cont):
        button = tk.Button(cont, text="GO", command=self.getCustomData, bg="#666666", width=10)
        return button

    def enterQuery(self, event):
        if event.keycode == 13:
            self.getCustomData()

    def createEntry(self, parent, temp_width=100, labelName="wartosc"):
        entryFrame = tk.Frame(parent, width=30, bd=0, bg="white", highlightbackground="white", pady=10)
        for i in range(4):
            entryFrame.columnconfigure(i, weight=1)

        self.createButton(entryFrame).pack(expand=0, side=tk.RIGHT)

        def clearBox(self):
            if username.get() == "zapytanie: ":
                name.delete(0, 'end')

        username = tk.StringVar()
        username.set("zapytanie: ")
        name = tk.Entry(entryFrame, bd=3, textvariable=username, width=temp_width)
        name.bind('<Button-1>', clearBox)
        name.bind("<Key>", self.enterQuery)
        name.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)

        self.names[labelName] = name
        return entryFrame

    def __str__(self):
        return "statisticpage"

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=500, height=200)
        self.controller = controller
        self.parent = parent
        # self.setColors("#110E0A")
        self.dataSet = controller.database.get_data_from_table("GameLog")
        self.setTheme("#FFFFFF")

        self.configure(bg=self.backgroundColor)
        self.button_font = tkfont.Font(family='Helvetica', size=16, weight="bold", slant="italic")

        self.x = self.winfo_reqwidth()
        self.y = self.winfo_reqheight()

        page_menu_frame = tk.Frame(self, borderwidth=2, relief=tk.GROOVE, background="white")
        self.createMenu(page_menu_frame).pack(fill=tk.Y, expand=0)
        page_menu_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        self.input_frame = tk.Frame(self, borderwidth=0, relief=tk.GROOVE, background="white",
                                    highlightbackground="white")
        self.names = {}
        self.entry = self.createEntry(self.input_frame)
        self.entry.pack(fill=tk.BOTH, expand=0)
        self.custom_table = self.customPandasTable(self.input_frame)
        self.custom_table.pack(fill=tk.BOTH, expand=1)
        self.input_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
