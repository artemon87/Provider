import pandas
import log
from collections import namedtuple

def read(location):
    Profile = namedtuple('Profile', 'File Dictionary')
    provFile = pandas.read_excel(location)
    dic = {}
    return Profile(provFile, dic)

def process(location):
    file = read(location)
    providerFile = file.File
    providerDict = file.Dictionary
    Provider = namedtuple('Provider', 'Name Fax Phone')
    for elem in providerFile.index:
	    try:
		    inst = Provider(providerFile['Name'][elem],
				    int(providerFile['Fax'][elem]),
				    int(providerFile['Phone'][elem]))
	    except Exception as e:
		    log.loggingInfo(e, 'needlesStat.py', 'process function') 
	    if inst not in providerDict:
		    providerDict[inst] = 1
	    else:
		    #inst.Weight += 1
		    providerDict[inst] += 1
    return toNamedtuple(providerDict)

def toNamedtuple(dic):
    Provider = namedtuple('Provider', 'Name Fax Phone Weight')
    providerList = []
    for key, value in dic.items():
        try:
            inst = Provider(key.Name, key.Fax, key.Phone, value)
            providerList.append(inst)
        except Exception as e:
            log.loggingInfo(e, 'needlesStat.py', 'toNamedtuple function') 
    return providerList
