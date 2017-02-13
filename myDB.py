import sqlite3
from collections import namedtuple

def setupDB():
    DB = namedtuple('DB', 'connection cursor')
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    return DB(conn, c)

def createHospitalDB(tup):
    tup.cursor.execute('''CREATE TABLE IF NOT EXISTS HOSPITAL(NAME varchar NOT NULL,
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
    tup.cursor.execute('''CREATE TABLE IF NOT EXISTS NEEDLES(NAME varchar NOT NULL,
                                       ADDRESS varchar,
                                       PHONE varchar DEFAULT NULL,
                                       FAX varchar DEFAULT NULL,
                                       SPECIALTY varchar DEFAULT NULL,
                                       ID varchar NOT NULL,
                                       WEIGHT integer DEFAULT 0,
                                       RU integer DEFAULT 0,
                                       ES integer DEFAULT 0,
                                       EN integer DEFAULT 0,
                                       PRIMARY KEY(ID));''')
    tup.connection.commit()


def createProviderDB(tup):
    tup.cursor.execute('''CREATE TABLE IF NOT EXISTS PROVIDER(NAME varchar NOT NULL,
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

def addNeedlesProvider(providerCollection, tup):
    for provider in providerCollection:
        tup.cursor.execute('''SELECT * FROM NEEDLES WHERE ID = ?''', (str(provider.ID),))
        result = tup.cursor.fetchall()
        if len(result) == 0:
            tup.cursor.execute('''INSERT INTO NEEDLES (NAME, ADDRESS, PHONE, ID, WEIGHT, RU, ES, EN) VALUES(?, ?, ?, ?, ?, ?, ?, ?);''',
                      (provider.Name, provider.Address, provider.Phone, str(provider.ID), provider.Weight, provider.Ru, provider.Es, provider.En))

    tup.connection.commit()
    

def readFromHospital(tup):
    returnList = []
    sqlRetrive = '''SELECT * FROM HOSPITAL ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive):
        returnList.append(row)
    return returnList
        
def readFromHospitalName(tup, name):
    P = namedtuple('P', 'NAME ADDRESS CITY STATE ZIP PHONE FAX RECORDS BILLING LINK UMBRELLA')
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT * FROM HOSPITAL WHERE NAME like ? or NAME like ? or NAME like ? ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        for elem in row:
            inst = P(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5], elem[6], elem[7], elem[8], elem[9], elem[10])
            returnList.append(inst)
    return returnList

def readFromHospitalUmbrella(tup, name):
    P = namedtuple('P', 'NAME ADDRESS CITY STATE ZIP PHONE FAX RECORDS BILLING LINK UMBRELLA')
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT * FROM HOSPITAL WHERE UMBRELLA like ? or UMBRELLA like ? or UMBRELLA like ? ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            returnList.append(inst)
        except IndexError as e:
            pass        
    return returnList

def readFromNeedlesName(tup, name):
    P = namedtuple('P', 'NAME ADDRESS PHONE FAX SPECIALTY ID WEIGHT RU ES EN')
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT * FROM NEEDLES WHERE NAME like ? or NAME like ? or NAME like ? ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            returnList.append(inst)
        except IndexError as e:
            pass        
    return returnList


def readFromProviderName(tup, name):
    P = namedtuple('P', 'NAME ADDRESS CITY STATE ZIP PHONE FAX LINK SPECIALTY')
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT * FROM PROVIDER WHERE NAME like ? or NAME like ? or NAME like ? ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            returnList.append(inst)
        except IndexError as e:
            pass        
    return returnList

def readFromProvider(tup):
    sqlRetrive = '''SELECT * FROM PROVIDER ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive):
        print(row)


