import sqlite3
import datetime


class Database:
    def __init__(self, filename):
        self.__connection = sqlite3.connect(filename)
        self.__cursor = self.__connection.cursor()

    def saveData(self, table, data):
        self.__cursor.execute(f'INSERT INTO {table} VALUES ({data[0]}, {data[1]}, {str(datetime.datetime.now()).split()[0]}) ')
        self.__connection.commit()

    def __del__(self):
        self.__connection.close()
        del self

    def getAllData(self, table):
        self.__cursor.execute(f"SELECT * FROM {table}")
        return self.__cursor.fetchall()
