import sqlite3
from datetime import datetime

from config import plus_category, minus_category
from scripts.tmp import *


class Banker:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        self.user_counter = self.cursor.execute("SELECT COUNT(*) FROM 'users'").fetchall()[0][0]
        self.transfer_counter = self.cursor.execute("SELECT COUNT(*) FROM 'transfers'").fetchall()[0][0]

    # !!! METHODS FOR USER INFORMATION !!!
    def addUser(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('id, user_id', 'condition', 'account') VALUES (?, ?, ?, 0)", (self.user_counter, user_id, True)).fetchall()

    def isActive(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'users' WHERE user_id = ?", (user_id, )).fetchall()[0][0]

    # !!! METHODS FOR TRANSFERS INFORMATION !!!
    def addTransfer(self, user_id: int, value: int, date, category: str):
        with self.connection:
            return self.connection.execute("INSERT INTO 'transfers' ('id', 'user_id', 'value', 'transfer_date', 'category') VALUES(?, ?, ?, ?, ?)", (self.transfer_counter, user_id, value, date, category))

    def monthlyReport(self, user_id):
        # return all transfers per month
        with self.connection:
            start = datetime.now().replace(day=1, microsecond=0)
            stop = datetime.now().replace(microsecond=0)
            return self.connection.execute("SELECT * FROM 'transfers' WHERE user_id = ? AND transfer_date >= ? AND transfer_date <= ?", (user_id, str(start), str(stop))).fetchall()

    '''
    def topCategory(self, user_id):
        # return the most popular category of user per month
        transfers = self.monthlyReport(user_id)
        a = [minus_category, [0 for i in range(len(minus_category))]]
        for i in range(len(transfers)):
            a[1][minus_category.index(transfers[i][5])] += transfers[i][5]
        return QSForDouble(a)
    '''


db = Banker('db.db')
print()