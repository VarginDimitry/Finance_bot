import sqlite3

from config import minus_category
from scripts import *


class Banker:

    def __init__(self, database):
        self.db_name = database
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

        self.user_counter = self.cursor.execute("SELECT COUNT(*) FROM 'users'").fetchall()[0][0]
        self.transfer_counter = self.cursor.execute("SELECT COUNT(*) FROM 'transfers'").fetchall()[0][0]

    # !!! METHODS FOR USER INFORMATION !!!

    def addUser(self, user_id):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO 'users' ('id', 'user_id', 'condition', 'account') "
                "VALUES (?, ?, ?, ?)", (self.user_counter, user_id, True, 0)).fetchall()

    def getUserById(self, user_id):
        with self.connection:
            user = self.cursor.execute("SELECT * FROM 'users' WHERE user_id = ?",
                                       (user_id, )).fetchall()
            return user[0] if user else None

    def userIdList(self, condition=2):
        with self.connection:
            # 2 is all users
            # 1 is users who use it now(True condition)
            # 0 is users who don't use it but was it the database
            if condition == 0:
                return [x[0] for x in self.cursor.execute("SELECT user_id, condition FROM 'users'").fetchall() if not x[1]]
            elif condition == 1:
                return [x[0] for x in self.cursor.execute("SELECT user_id, condition FROM 'users'").fetchall() if x[1]]
            return [int(x[0]) for x in self.cursor.execute("SELECT user_id FROM 'users'").fetchall()]

    def isActive(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'users' WHERE user_id = ?", (user_id,)).fetchall()[0][0]

    def setStatus(self, user_id, condition: bool):
        with self.connection:
            self.connection.execute("UPDATE 'users' SET condition = ? WHERE user_id = ?", (int(condition), user_id))

    # !!! METHODS FOR TRANSFERS INFORMATION !!!

    def addTransfer(self, user_id: int, value: float, date, category='неВыбрано✖'):
        with self.connection:
            self.connection.execute(
                "INSERT INTO 'transfers' ('id', 'user_id', 'value', 'transfer_date', 'category') VALUES(?, ?, ?, ?, ?)", (self.transfer_counter, user_id, value, date, category[:-1]))
            self.transfer_counter += 1

    def updateTransfer(self, its_id: int, user_id: int, value: float, category: str, date):
        with self.connection:
            value = abs(value) if category[-1] == '➕' else -abs(value)
            self.connection.execute(
                "UPDATE 'transfers' SET user_id = ?, value = ?, transfer_date = ?, category = ? WHERE id = ?",
                (user_id, value, date, category[:-1], its_id))
            account = self.connection.execute(
                "SELECT account FROM 'users' WHERE user_id = ?",
                (user_id,)).fetchall()[0][0]
            self.connection.execute("UPDATE 'users' SET account = ? WHERE user_id = ?", (account + value, user_id, ))

    def getLastTransfer(self, user_id: int):
        with self.connection:
            a = self.connection.execute(
                "SELECT * FROM 'transfers' WHERE user_id = ? ORDER BY transfer_date DESC",
                (user_id,)).fetchall()
            if len(a) != 0:
                return a[0]
            else:
                print(f'ERROR: У пользователя {user_id} нет записей!!!')
                return None

    def getTransferById(self, transfer_id):
        with self.connection:
            return self.connection.execute("SELECT * FROM 'transfers' WHERE id = ?", (transfer_id, )).fetchall()[0]

    def monthlyReport(self, user_id):
        with self.connection:
            # return all transfers per month
            start = datetime.now().replace(day=1, microsecond=0)
            stop = datetime.now().replace(microsecond=0)
            return self.connection.execute(
                "SELECT * FROM 'transfers' WHERE user_id = ? AND transfer_date >= ? AND transfer_date <= ?",
                (user_id, str(start), str(stop))).fetchall()

    def topCategory(self, user_id):
        with self.connection:
            # return the most popular category of user per month
            transfers = self.monthlyReport(user_id)
            a = [[0 for i in range(len(minus_category))], minus_category]
            for i in range(len(transfers)):
                if transfers[i][4] in minus_category:
                    a[0][minus_category.index(transfers[i][4])] += transfers[i][2]
                else:
                    a[0][minus_category.index('Другое')] += transfers[i][2]
            return QSDouble(a)

    def deleteEmptyTransfers(self, user_id):
        with self.connection:
            self.connection.execute("DELETE FROM 'transfer' WHERE user_id = ? and category = ?",
                                    (user_id, 'неВыбрано'))


'''
db = Banker('db.db')
print(db.monthlyReport(336619540))
'''