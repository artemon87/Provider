import pandas
import log
from collections import namedtuple
from collections import defaultdict
from collections import Counter
import networkx as nx
from find import *

def read(location):
    Profile = namedtuple('Profile', 'File Dictionary')
    provFile = pandas.read_excel(location)
    dic = defaultdict(list)
    return Profile(provFile, dic)

def processAll(location):
    toRemove = ['UNKNOWN-MEDICAL PROVIDER', 'Secure Health Information', 'Rubinstein Law Offices',
                'BISHOP LAW OFFICES, P.S.','ER Hospital visit', 'LAW OFFICES OF MARK A. HAMMER & ASSOCIATES, INC.',
                'Rx', 'Rx Bartell Drugs', 'Rx Fred Meyer', 'Rx Rite Aid', 'Rx Walgreens',
                'TOW EXPRESS', 'UNKNOWN-INSURANCE', 'WAGE LOSS', 'bishoplegal']
    file = read(location)
    providerFile = file.File
    providerDict = file.Dictionary
    Provider = namedtuple('Provider', 'Name Phone ID')
    currentCase = previousCase = 0
    for elem in providerFile.index:
        if providerFile['compute_0005'][elem] not in toRemove:
            currentCase = providerFile['casenum'][elem]
            phone = str(providerFile['compute_0008'][elem])
            if phone:
                phone = phone.replace('(', '').replace(') ', '').replace(' - ', '')
            else:
                phone = 'NONE'
            inst = Provider(providerFile['compute_0005'][elem],
                            phone,
                            providerFile['names_id'][elem])
            if inst in providerDict:
                providerDict[inst] += 1
            else:
                providerDict[inst] = 1
    return createNX(providerDict, providerFile, toRemove, 3)


def processFacility(location, hospitals = None, singleProvider = None, netSize = None):
    toRemove = ['UNKNOWN-MEDICAL PROVIDER', 'Secure Health Information', 'Rubinstein Law Offices',
                'BISHOP LAW OFFICES, P.S.','ER Hospital visit', 'LAW OFFICES OF MARK A. HAMMER & ASSOCIATES, INC.',
                'Rx', 'Rx Bartell Drugs', 'Rx Fred Meyer', 'Rx Rite Aid', 'Rx Walgreens',
                'TOW EXPRESS', 'UNKNOWN-INSURANCE', 'WAGE LOSS', 'bishoplegal']
    file = read(location)
    providerFile = file.File
    providerDict = file.Dictionary
    Provider = namedtuple('Provider', 'Name Phone ID')
    currentCase = previousCase = 0
    for elem in providerFile.index:
        if providerFile['compute_0005'][elem] not in toRemove:
            currentCase = providerFile['casenum'][elem]
            phone = str(providerFile['compute_0008'][elem])
            if phone:
                phone = phone.replace('(', '').replace(') ', '').replace(' - ', '')
            else:
                phone = 'NONE'
            inst = Provider(providerFile['compute_0005'][elem],
                            phone,
                            providerFile['names_id'][elem])
            if hospitals != None:
                for i in hospitals:
                    res = searchRatio(inst.Name.upper(), i.Name.upper(), 0.85)
                    if res:
                        if inst not in providerDict:
                            providerDict[inst] = 1
                        else:
                            providerDict[inst] += 1
            elif singleProvider != None:
                res = searchRatio(inst.Name.upper(), singleProvider.upper(), 0.85)
                if res:
                    providerDict[inst] = 1
                    break
                else:
                    res = searchRatio(inst.Name.upper(), singleProvider.upper(), 0.75)
                    if res:
                        providerDict[inst] = 1
                        break
    return createNX(providerDict, providerFile, toRemove, netSize)
    

def createNX(providerDict, providerFile, toRemove, netSize):
    singleElement = None
    if len(providerDict) == 1:
        for k,v in providerDict.items():
            singleElement = k

    newDict = defaultdict(list)
    ProviderWeighted = namedtuple('ProviderWeighted', 'Name Phone ID Weight')
    Provider = namedtuple('Provider', 'Name Phone ID')
    lst = []
    list_of_lists = []
    list_of_single_elem = []
    ed = nx.Graph()
    current = prev = 0
    for elem in providerFile.index:
        prev = current
        current = providerFile['casenum'][elem]
        if current == prev:
            if providerFile['compute_0005'][elem] not in toRemove:
                phone = str(providerFile['compute_0008'][elem])
                if phone:
                    phone = phone.replace('(', '').replace(') ', '').replace(' - ', '')
                else:
                    phone = 'NONE'
                inst = Provider(providerFile['compute_0005'][elem],
                                phone,
                                providerFile['names_id'][elem])
                lst.append(inst)
                
        else:
            if singleElement in lst:
                for i in lst:
                    if singleElement != i:
                        list_of_single_elem.append(i)
            list_of_lists.append(lst)
            lst = []
    for key, value in providerDict.items():
        inst = ProviderWeighted(key.Name, key.Phone, key.ID, value)
        ed.add_node(key.Name)
        if singleElement:
            count = Counter(list_of_single_elem)
            try:
                count = count.most_common(netSize)
                for i in count:
                    ed.add_edge(singleElement.Name, i[0].Name)
            except Exception as e:
                print(e)
        else:
            for l in list_of_lists[1:]:
                if key in l:
                    for i in l:
                        if i != key:
                            ed.add_edge(key.Name, i.Name)
                            newDict[inst].append(i)

    return providerDict, newDict, ed


def providerDictToList(providerDict):
    lst = []
    for key,value in providerDict.items():
        lst.append(key)
    return lst
        
        
    
    
        
        
    


        
        
