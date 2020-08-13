import sqlite3
from datetime import datetime



class Banker:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.user_counter = self.cursor.execute("SELECT COUNT(*) FROM 'users'").fetchall()[0][0]
        self.transfer_counter = self.cursor.execute("SELECT COUNT(*) FROM 'transfers'").fetchall()[0][0]

    # METHODS FOR USER INFORMATION
    def addUser(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('id, user_id', 'condition', account) VALUES (?, ?, ?, 0)", (self.user_counter, user_id, True)).fetchall()

    def isActive(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'users' WHERE 'user_id' = ?", (user_id, )).fetchall()[0][0]

    # METHODS FOR TRANSFERS INFORMATION
    def addTransfer(self, user_id: int, value: int, date, category: str):
        with self.connection:
            return self.connection.execute("INSERT INTO 'transfers' ('id', 'user_id', 'value', 'date', 'category') VALUES(?, ?, ?, ?, ?)", (self.transfer_counter, user_id, value, date, category))

    def monthlyReport(self, user_id):
        pass


db = Banker('db.db')
print(db.user_counter)