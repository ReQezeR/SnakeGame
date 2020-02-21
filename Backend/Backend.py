import sqlite3
import re
import os
import sys
from time import sleep


class DbProvider:
    # path to exe folder
    def database_path(self, relative):
        p = os.path.join(os.environ.get("_MEIPASS2", os.path.abspath(".")), relative)
        print(p)
        return p

    def get_dict(self, headers, rows):  #  Create dict
        dataset = {}
        data = {}
        j = 0
        for row in rows:
            i = 0
            for item in row:
                data[str(headers[i])] = str(item)
                i += 1
            dataset[str(j)] = data.copy()
            j += 1
            data.clear()
        self.dataSet.clear()
        self.dataSet = dataset
        return dataset


    # Select ID, Result From GameLog g where g.Result>10
    def custom_select(self, select_formula):
        headers =[]
        x = re.split("(?i)FROM",select_formula)
        headers = re.findall(r'(\w+)+', re.split("(?i)SELECT", x[0])[1], re.IGNORECASE)
        if headers == []:
            headers = re.findall(r'([*]+)', re.split("(?i)SELECT", x[0])[1], re.IGNORECASE)

        table_name = re.findall(r'(\w+)+', x[1], re.IGNORECASE)[0]
         # Get headers of table
        if (headers[0] == '*'):
            header_request = '''SELECT name FROM PRAGMA_TABLE_INFO('{}')'''.format(table_name)
            self.cursor.execute(header_request)
            headers = self.cursor.fetchall()
            new_headers = []
            for h in headers:
                new_headers.append(h[0])
            headers = new_headers
        #  Get rows of table
        sql = select_formula
        try:
            self.cursor.execute(sql)
        except (e):
            print(e)
        rows = self.cursor.fetchall()
        return self.get_dict(headers, rows)

    def get_data_from_table(self, table_name):
        #  Get headers of table
        header_request = '''SELECT name FROM PRAGMA_TABLE_INFO('{}')'''.format(table_name)
        self.cursor.execute(header_request)
        headers = self.cursor.fetchall()
        new_headers = []
        for h in headers:
            new_headers.append(h[0])
        headers = new_headers

        #  Get rows of table
        sql = '''SELECT * FROM {}'''.format(table_name)
        try:
            self.cursor.execute(sql)
        except (e):
            print(e)
        rows = self.cursor.fetchall()
        return self.get_dict(headers, rows)

    def __init__(self):
        self.path = self.database_path('DB\db.sqlite')
        self.dataSet = {}
        # Create database if not exist and get a connection to it
        if not os.path.isfile(self.path):
            try:
                os.mkdir(self.database_path("DB"))
            except:
                pass
        self.connection = sqlite3.connect(self.path)

         # Get a cursor to execute sql statements
        self.cursor = self.connection.cursor()
        # Create tables
        self.game_log = self.GameLog(self)

    class GameLog:
        def insert_into_table(self, result):
            sql = '''INSERT INTO GameLog(Time, Result) VALUES (DATETIME('now','localtime'), '{}');'''.format(result)
            self.cursor.execute(sql)
            self.connection.commit()

        def __init__(self, parent):
            self.connection = parent.connection
            self.cursor = parent.cursor
            sql = '''CREATE TABLE IF NOT EXISTS GameLog
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Time varchar(100),
            Result INTEGER
            )'''
            self.cursor.execute(sql)
            self.connection.commit()


