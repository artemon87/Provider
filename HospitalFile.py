from collections import defaultdict
from collections import namedtuple
import pandas

def initHospital():
    Hospitals = namedtuple('Hospitals', 'File List')
    hospFile = pandas.read_excel('HospitalsInTheUS.xlsx')
    hospList = []
    return Hospitals(hospFile, hospList)


def readHospital(state):
    initiated = initHospital()
    hospFile = initiated.File
    hospList = initiated.List
    HospitalProfile = namedtuple('HospitalProfile', 'Name Address City State Zip Phone')
    for elem in hospFile.index:
        if hospFile['State'][elem] == state:
            instance = HospitalProfile(hospFile['Hospital Name'][elem],
                                       hospFile['Address'][elem],
                                       hospFile['City'][elem],
                                       hospFile['State'][elem],
                                       hospFile['ZIP Code'][elem],
                                       hospFile['Phone Number'][elem])
            hospList.append(instance)
    return hospList

def findHospitalFull(name, hList):
    looking = [elem for elem in hList if name.upper() in elem.Name]
    return looking

def findHospitalStartsWith(name, hList):
    looking = [elem for elem in hList if elem.Name.startswith(name.upper())]
    return looking 
