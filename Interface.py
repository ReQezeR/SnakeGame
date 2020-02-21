import os
import sys
import tkinter as tk
from tkinter import font as tkfont

from Backend.Backend import DbProvider
from Frontend.GamePage import GamePage
from Frontend.MenuPage import Menu
from Frontend.StatisticPage import StatisticPage


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.database = DbProvider()
        self.t1 = None
        self.title_font = tkfont.Font(family='Helvetica', size=40, weight="bold", slant="italic")
        self.sizeFlag = False

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Menu, GamePage, StatisticPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Menu")

    def exit_callback(self):
        self.t1.kill()
        self.t1.join()
        self.destroy()

    # path to files include in exe
    def resource_path(self, relative_path):
        default = "Frontend/Images/"
        relative_path = default + relative_path
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def make_window_bigger(self):
        self.geometry('1200x650')
        self.minsize(1200, 650)

    def make_window_smaller(self):
        self.geometry('440x650')
        self.minsize(440, 650)

    def show_frame(self, page_name):
        #  Show a frame for the given page name
        if page_name != "Menu" and self.sizeFlag == False:
            self.make_window_bigger()
            self.sizeFlag = True
        elif page_name == "Menu" and self.sizeFlag == True:
            self.make_window_smaller()
            self.sizeFlag = False

        self.frame = self.frames[page_name]
        self.frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.wm_protocol("WM_DELETE_WINDOW", app.exit_callback)
    app.minsize(440, 650)
    app.title("Snake Game")
    app.geometry("440x650")
    app.mainloop()

