import sqlite3


def getdata(response):
    
    connection = sqlite3.connect('kun.db')
    cursor = connection.cursor()

    cursor.execute(response)

    return cursor.fetchall()


def setdata(response):

    connection = sqlite3.connect('kun.db')
    cursor = connection.cursor()

    cursor.execute(response)

    connection.commit()

