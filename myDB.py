import sqlite3
from collections import namedtuple

def setupDB():
    DB = namedtuple('DB', 'connection cursor')
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    return DB(conn, c)

def createHospitalDB(tup):
    tup.cursor.execute('''CREATE TABLE HOSPITAL(ID integer PRIMARY KEY,
                                       NAME varchar NOT NULL,
                                       ADDRESS varchar,
                                       CITY varchar,
                                       STATE varchar,
                                       ZIP integer,
                                       PHONE integer UNIQUE,
                                       UMBRELLA varchar DEFAULT NULL);''')
    tup.connection.commit()


def addHospital(hospitalCollection, tup):
    for hospital in hospitalCollection:
        tup.cursor.execute('''INSERT INTO HOSPITAL (ID, NAME, ADDRESS, CITY, STATE, ZIP, PHONE) VALUES(?, ?, ?, ?, ?, ?, ?);''',
                  (int(hospital.ID), hospital.Name, hospital.Address, hospital.City, hospital.State, int(hospital.Zip), int(hospital.Phone)))

    tup.connection.commit()
    

def readFromHospital(tup):
    sqlRetrive = '''SELECT * FROM HOSPITAL ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive):
        print(row)


