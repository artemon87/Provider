import sqlite3
from collections import namedtuple



def setupCookiesDB():
    DB = namedtuple('DB', 'connection cursor')
    conn = sqlite3.connect('cookieDB.db')
    c = conn.cursor()
    return DB(conn, c)
def createCookieTable(tup):
    tup.cursor.execute('''CREATE TABLE IF NOT EXISTS COOKIE(ID ineger NOT NULL PRIMARY KEY,
                                       IN varchar,
                                       OUT varchar DEFAULT NULL;''')
def addCookie(name, possibleChoice, tup):
    name = name.upper()
    tup.cursor.execute('''SELECT * FROM COOKIE WHERE IN = ?;''', (name))
    result = tup.cursor.fetchall()
    if len(result) == 0:
        tup.cursor.execute('''INSERT INTO COOKIE (IN, OUT) VALUES(?);''', (name, possibleChoice))
    tup.connection.commit() 
                       
    

    
def setupDB():
    DB = namedtuple('DB', 'connection cursor')
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    return DB(conn, c)

def createMessageDB(tup):
    tup.cursor.execute('''CREATE TABLE IF NOT EXISTS MESSAGE(ID integer NOT NULL PRIMARY KEY,
                                       NUMBER varchar NOT NULL,
                                       NOTE varchar DEFAULT NULL,
                                       ATTACHMENT varchar DEFAULT NULL,
                                       TIME_SENT varchar DEFAULT NULL);''')
    tup.connection.commit()

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
                                       GEO varchar DEFAULT NULL,
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

def alterProviderTable(tup):
    tup.cursor.execute('''ALTER TABLE PROVIDER ADD COLUMN GEO varchar DEFAULT NULL;''')
    tup.connection.commit()


def alterHospitalTable(tup):
    tup.cursor.execute('''ALTER TABLE HOSPITAL ADD COLUMN GEO varchar DEFAULT NULL;''')
    tup.connection.commit()


def addMessage(tup, message):
    tup.cursor.execute('''SELECT * FROM MESSAGE WHERE NUMBER = ? AND NOTE = ?;''', (message.Number, message.Note))
    result = tup.cursor.fetchall()
    if len(result) == 0:
        tup.cursor.execute('''INSERT INTO MESSAGE (NUMBER, NOTE, TIME_SENT, ATTACHMENT) VALUES(?,?,?,?);''',(message.Number, message.Note, message.Date, message.Attachment))
    tup.connection.commit()

def readFromMessage(tup):
    returnList = []
    M = namedtuple('M', 'ID Number Note Attachment Date')
    sqlRetrive = '''SELECT * FROM MESSAGE'''
    for row in tup.cursor.execute(sqlRetrive):
        try:
            inst = M(row[0], row[1], row[2], row[3], row[4])
            returnList.append(inst)
        except Exception as e:
            pass
    return returnList


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
            tup.cursor.execute('''INSERT INTO NEEDLES (NAME, ADDRESS, PHONE, ID, GEO, WEIGHT, RU, ES, EN) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);''',
                      (provider.Name.upper(), provider.Address, provider.Phone, str(provider.ID), str(provider.Geo), provider.Weight, provider.Ru, provider.Es, provider.En))

    tup.connection.commit()
    

def readFromHospital(tup):
    P = namedtuple('P', 'NAME ADDRESS CITY STATE ZIP PHONE FAX RECORDS BILLING LINK UMBRELLA GEO')
    returnList = []
    sqlRetrive = '''SELECT * FROM HOSPITAL ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
            returnList.append(inst)
        except Exception as e:
            pass
    return returnList

        
def readFromHospitalName(tup, name):
    P = namedtuple('P', 'NAME ADDRESS CITY STATE ZIP PHONE FAX RECORDS BILLING LINK UMBRELLA GEO')
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT * FROM HOSPITAL WHERE NAME like ? or NAME like ? or NAME like ? ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
            returnList.append(inst)
        except Exception as e:
            pass
    return returnList

def readFromHospitalUmbrella(tup, name):
    P = namedtuple('P', 'NAME ADDRESS CITY STATE ZIP PHONE FAX RECORDS BILLING LINK UMBRELLA GEO')
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT * FROM HOSPITAL WHERE UMBRELLA like ? or UMBRELLA like ? or UMBRELLA like ? ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
            returnList.append(inst)
        except IndexError as e:
            pass        
    return returnList

def updateBillingHospitalUmbrella(tup, name, fax):
    name = name.upper()
    sqlRetrive = '''UPDATE HOSPITAL SET RECORDS = ? WHERE UMBRELLA like ? or UMBRELLA like ? or UMBRELLA like ?;'''
    tup.cursor.execute(sqlRetrive,[fax, ('%'+name+'%'), (name+'%'), ('%'+name)])
    tup.connection.commit()


def updateBillingHospitalName(tup, name, fax):
    name = name.upper()
    sqlRetrive = '''UPDATE HOSPITAL SET RECORDS = ? WHERE NAME like ? or NAME like ? or NAME like ?;'''
    tup.cursor.execute(sqlRetrive,[fax, ('%'+name+'%'), (name+'%'), ('%'+name)])
    tup.connection.commit()

def updateRecordsHospitalUmbrella(tup, name, fax):
    name = name.upper()
    sqlRetrive = '''UPDATE HOSPITAL SET RECORDS = ? WHERE UMBRELLA like ? or UMBRELLA like ? or UMBRELLA like ?;'''
    tup.cursor.execute(sqlRetrive,[fax, ('%'+name+'%'), (name+'%'), ('%'+name)])
    tup.connection.commit()


def updateRecordsHospitalName(tup, name, fax):
    name = name.upper()
    sqlRetrive = '''UPDATE HOSPITAL SET RECORDS = ? WHERE NAME like ? or NAME like ? or NAME like ?;'''
    tup.cursor.execute(sqlRetrive,[fax, ('%'+name+'%'), (name+'%'), ('%'+name)])
    tup.connection.commit()

def updateNeedlesFax(tup, provider):
    for key, value in provider.items():
        sqlRetrive = '''UPDATE NEEDLES SET FAX = ? WHERE ID = ?;'''
        tup.cursor.execute(sqlRetrive, [str(value), str(key)])
    tup.connection.commit()


def updateHospitalGEO(tup, provider):
    for elem in provider:
        sqlRetrive = '''UPDATE HOSPITAL SET GEO = ? WHERE NAME = ?;'''
        tup.cursor.execute(sqlRetrive, [str(elem.Geo), elem.Name])
    tup.connection.commit()

def updateProviderGEO(tup, provider):
    for elem in provider:
        sqlRetrive = '''UPDATE PROVIDER SET GEO = ? WHERE NAME = ? AND PHONE = ?;'''
        tup.cursor.execute(sqlRetrive, [str(elem.Geo), elem.Name, elem.Phone])
    tup.connection.commit()


def readFromNeedlesAll(tup):
    P = namedtuple('P', 'NAME ADDRESS PHONE FAX SPECIALTY ID GEO WEIGHT RU ES EN')
    returnList = []
    sqlRetrive = '''SELECT * FROM NEEDLES ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            returnList.append(inst)
        except IndexError as e:
            pass        
    return returnList
    

def readFromNeedlesName(tup, name):
    P = namedtuple('P', 'NAME ADDRESS PHONE FAX SPECIALTY ID GEO WEIGHT RU ES EN')
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT * FROM NEEDLES WHERE NAME like ? or NAME like ? or NAME like ? ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            returnList.append(inst)
        except IndexError as e:
            pass        
    return returnList

def readFromNeedlesNameExact(tup, name):
    P = namedtuple('P', 'NAME ADDRESS PHONE FAX SPECIALTY ID GEO WEIGHT RU ES EN')
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT * FROM NEEDLES WHERE NAME like ? or NAME like ? or NAME like ?;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])
            returnList.append(inst)
        except IndexError as e:
            pass        
    return returnList



def readFromProviderName(tup, name):
    P = namedtuple('P', 'NAME ADDRESS CITY STATE ZIP PHONE FAX LINK SPECIALTY GEO')
    name = name.upper()
    returnList = []
    sqlRetrive = '''SELECT * FROM PROVIDER WHERE NAME like ? or NAME like ? or NAME like ? ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive, [('%'+name+'%'), (name+'%'), ('%'+name)]):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            returnList.append(inst)
        except IndexError as e:
            pass        
    return returnList


def readFromProvider(tup):
    P = namedtuple('P', 'NAME ADDRESS CITY STATE ZIP PHONE FAX LINK SPECIALTY GEO')
    returnList = []
    sqlRetrive = '''SELECT * FROM PROVIDER ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive):
        try:
            inst = P(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            returnList.append(inst)
        except IndexError as e:
            pass 
    return returnList

def readFromNeedles(tup):
    sqlRetrive = '''SELECT * FROM NEEDLES ORDER BY NAME ASC;'''
    for row in tup.cursor.execute(sqlRetrive):
        print(row)

def dropHospital(tu):
    sqlRetrive = '''DROP TABLE IF EXISTS HOSPITAL;'''
    tup.cursor.execute(sqlRetrive)
    tup.connection.commit()

def dropNeedles(tup):
    sqlRetrive = '''DROP TABLE IF EXISTS NEEDLES;'''
    tup.cursor.execute(sqlRetrive)
    tup.connection.commit()

def dropProvider(tup):
    sqlRetrive = '''DROP TABLE IF EXISTS PROVIDER;'''
    tup.cursor.execute(sqlRetrive)
    tup.connection.commit()

def dropMessage(tup):
    sqlRetrive = '''DROP TABLE IF EXISTS MESSAGE;'''
    tup.cursor.execute(sqlRetrive)
    tup.connection.commit()
