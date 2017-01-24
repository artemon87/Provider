import sqlite3
from collections import namedtuple

def setupDB():
    DB = namedtuple('DB', 'connection cursor')
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    return DB(conn, c)

def createHospitalDB(tup):
    tup.cursor.execute('''CREATE TABLE HOSPITAL(id INTEGER PRIMARY KEY NOT NULL,
                                       NAME varchar NOT NULL,
                                       ADDRESS varchar,
                                       CITY varchar,
                                       STATE varchar,
                                       ZIP varchar,
                                       PHONE varchar DEFAULT NULL,
                                       FAX varchar DEFAULT NULL,
                                       LINK varchar DEFAULT NULL);''')
    tup.connection.commit()


def addHospital(hospitalCollection, tup):
    for hospital in hospitalCollection:
        tup.cursor.execute('''INSERT INTO HOSPITAL (NAME, ADDRESS, CITY, STATE, ZIP, PHONE, FAX, LINK) VALUES(?, ?, ?, ?, ?, ?, ?, ?);''',
                  (hospital.Name, hospital.Address, hospital.City, hospital.State, hospital.Zip, hospital.Phone, hospital.Fax, hospital.Link))

    tup.connection.commit()
    

def readFromHospital(tup):
    sqlRetrive = '''SELECT * FROM HOSPITAL ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive):
        print(row)


