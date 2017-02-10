import sqlite3
from collections import namedtuple

def setupDB():
    DB = namedtuple('DB', 'connection cursor')
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    return DB(conn, c)

def createHospitalDB(tup):
    tup.cursor.execute('''CREATE TABLE HOSPITAL(NAME varchar NOT NULL,
                                       ADDRESS varchar,
                                       CITY varchar,
                                       STATE varchar,
                                       ZIP varchar,
                                       PHONE varchar DEFAULT NULL,
                                       FAX varchar DEFAULT NULL,
                                       RECORDS varchar DEFAULT NULL,
                                       BILLING varchar DEFAULT NULL,
                                       LINK varchar DEFAULT NULL,
                                       UMBRELLA varchar DEFAULT NULL,
                                       PRIMARY KEY(NAME, PHONE));''')
    tup.connection.commit()


def createNeedlesDB(tup):
    tup.cursor.execute('''CREATE TABLE NEEDLES(NAME varchar NOT NULL,
                                       ADDRESS varchar,
                                       PHONE varchar DEFAULT NULL,
                                       FAX varchar DEFAULT NULL,
                                       SPECIALTY varchar DEFAULT NULL,
                                       ID integer PRIMARY KEY NOT NULL,
                                       WEIGHT integer DEFAULT 0,
                                       PRIMARY KEY(NAME, PHONE));''')
    tup.connection.commit()


def createProviderDB(tup):
    tup.cursor.execute('''CREATE TABLE PROVIDER(NAME varchar NOT NULL,
                                       ADDRESS varchar,
                                       CITY varchar,
                                       STATE varchar,
                                       ZIP varchar,
                                       PHONE varchar DEFAULT NULL,
                                       FAX varchar DEFAULT NULL,
                                       LINK varchar DEFAULT NULL,
                                       SPECIALTY varchar DEFAULT NULL,
                                       PRIMARY KEY(NAME, PHONE));''')
    tup.connection.commit()


def addHospital(hospitalCollection, tup):
    for hospital in hospitalCollection:
        tup.cursor.execute('''INSERT INTO HOSPITAL (NAME, ADDRESS, CITY, STATE, ZIP, PHONE, FAX, LINK, UMBRELLA) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                  (hospital.Name, hospital.Address, hospital.City, hospital.State, hospital.Zip, hospital.Phone, hospital.Fax, hospital.Link, hospital.Umbrella))

    tup.connection.commit()

def addProvider(providerCollection, tup):
    for provider in providerCollection:
        tup.cursor.execute('''SELECT * FROM PROVIDER WHERE NAME = ? AND PHONE = ?''', (provider.Name, provider.Phone))
        result = tup.cursor.fetchall()
        if len(result) == 0:
            tup.cursor.execute('''INSERT INTO PROVIDER (NAME, ADDRESS, CITY, STATE, ZIP, PHONE, SPECIALTY) VALUES(?, ?, ?, ?, ?, ?, ?);''',
                      (provider.Name, provider.Address, provider.City, provider.State, provider.Zip, provider.Phone, provider.Specialty))

    tup.connection.commit()
    

def readFromHospital(tup):
    sqlRetrive = '''SELECT * FROM HOSPITAL ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive):
        print(row)
def readFromHospitalName(tup, name):
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT NAME, ADDRESS, CITY, PHONE, LINK FROM HOSPITAL WHERE NAME like ? or NAME like ? or NAME like ? ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        returnList.append(row)
    return returnList

def readFromHospitalUmbrella(tup, name):
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT NAME, ADDRESS, CITY, PHONE, LINK FROM HOSPITAL WHERE UMBRELLA like ? or UMBRELLA like ? or UMBRELLA like ? ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        returnList.append(row)
    return returnList

def readFromProvider(tup):
    sqlRetrive = '''SELECT * FROM PROVIDER ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive):
        print(row)


