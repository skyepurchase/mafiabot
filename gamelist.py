import sqlite3
from sqlite3 import Error

class GameList:
    instance = None

    def __init__(self):
        print("Connecting to local database file game_list.sqlite...")
        
        self.db = None
        try:
            self.db = sqlite3.connect("game_list.sqlite")
        except Error as e:
            print(e)
        
        sql_create_games_table = """CREATE TABLE IF NOT EXISTS games (
                                        gameName TEXT NOT NULL PRIMARY KEY,
                                        creatorID INTEGER NOT NULL
                                        status TEXT NOT NULL);"""
        sql_create_attendances_table = """CREATE TABLE IF NOT EXISTS attendances (
                                            playerID INTEGER NOT NULL PRIMARY KEY,
                                            FOREIGN KEY (gameName) REFERENCES games (gameName),
                                            condition TEXT NOT NULL,
                                            role TEXT NOT NULL);"""
        if self.db is not None:
            self.__create_table(sql_create_games_table)
            self.__create_table(sql_create_attendances_table)
        else:
            print("Error! cannot create the database connection.")

    def create_game(self, name, member):
        self.db.execute("INSERT INTO games(gameName, creatorID, status) VALUES (?, ?, 'open')",
                        [name, member.id])
        self.db.commit()

    def create_attendance(self, member, game_name, role):
        self.db.execute("""INSERT INTO attendances(playerID, gameName, condition, role) 
                            VALUES (?, ?, 'alive', ?)""",
                            [member.id, game_name, role])
        self.db.commit()

    def close_game(self, game_name):
        self.db.execute("UPDATE games SET status='closed' WHERE gameName=?", [game_name])
        self.db.commit()

    def kill_player(self, game_name, member):
        self.db.execute("UPDATE attendances SET condition='dead' WHERE gameName=? AND playerID=?",
                            [game_name, member.id])
        self.db.commit()

    def get_roles(self, game_name):
        c = self.db.cursor()
        c.execute("SELECT role, playerID FROM attendances WHERE gameName=? AND condition='alive'",
                    [game_name])
        results = c.fetchall()

        if len(results) < 1:
            return None

        return results

    def get_all_roles(self, game_name):
        c = self.db.cursor()
        c.execute("SELECT role, playerID FROM attendances WHERE gameName=?", [game_name])
        results = c.fetchall()

        if len(results) < 1:
            return None

        return results

    def get_role(self, game_name, member):
        c = self.db.cursor()
        c.execute("SELECT role FROM attendances WHERE gameName=? AND playerID=?",
                    [game_name, member.id])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def get_condition(self, game_name, member):
        c = self.db.cursor()
        c.execute("SELECT condition FROM attendances WHERE gameName=? AND playerID=?",
                    [game_name, member.id])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def get_status(self, game_name):
        c = self.db.cursor()
        c.execute("SELECT status FROM games WHERE gameName=?", [game_name])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def get_creator(self, game_name):
        c = self.db.cursor()
        c.execute("SELECT creatorID FROM games WHERE gameName=?", [game_name])
        results = c.fetchall()

        if len(results) < 1:
            return None

        row = results[0]
        return row[0]

    def __create_table(self, create_table_sql):
        try:
            c = self.db.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
