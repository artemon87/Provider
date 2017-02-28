import pandas
import log
from collections import namedtuple
from collections import defaultdict
from collections import Counter
import networkx as nx
from find import *
import googlemaps
import geocoder

def read(location):
    Profile = namedtuple('Profile', 'File Dictionary')
    provFile = pandas.read_excel(location)
    dic = defaultdict(list)
    return Profile(provFile, dic)

def processAll(location):
    toRemove = ['UNKNOWN-MEDICAL PROVIDER', 'Secure Health Information', 'Rubinstein Law Offices',
                'BISHOP LAW OFFICES, P.S.','ER Hospital visit', 'LAW OFFICES OF MARK A. HAMMER & ASSOCIATES, INC.',
                'Rx', 'Rx Bartell Drugs', 'Rx Fred Meyer', 'Rx Rite Aid', 'Rx Walgreens',
                'TOW EXPRESS', 'UNKNOWN-INSURANCE', 'WAGE LOSS', 'bishoplegal', 'Healthport (Smart Document Solutions)',
                'KISSELMAN LAW FIRM']
    file = read(location)
    providerFile = file.File
    providerDict = file.Dictionary
    Provider = namedtuple('Provider', 'Name Address Phone ID')
    currentCase = previousCase = 0
    for elem in providerFile.index:
        if providerFile['compute_0005'][elem] not in toRemove:
            currentCase = providerFile['casenum'][elem]
            phone = str(providerFile['compute_0008'][elem])
            addr = str(providerFile['compute_0007'][elem])
            if phone:
                phone = phone.replace('(', '').replace(') ', '').replace(' - ', '')
            else:
                phone = 'NONE'
            if addr:
                addr = addr.replace('\n\n', ' ')
            else:
                addr = 'NONE'
                
            inst = Provider(providerFile['compute_0005'][elem],
                            addr,
                            phone,
                            providerFile['names_id'][elem])
            if inst in providerDict:
                providerDict[inst] += 1
            else:
                providerDict[inst] = 1
    return providerDict, providerFile, toRemove


def processFacility(location, hospitals = None, singleProvider = None, ratio = 0.85):
    toRemove = ['UNKNOWN-MEDICAL PROVIDER', 'Secure Health Information', 'Rubinstein Law Offices',
                'BISHOP LAW OFFICES, P.S.','ER Hospital visit', 'LAW OFFICES OF MARK A. HAMMER & ASSOCIATES, INC.',
                'Rx', 'Rx Bartell Drugs', 'Rx Fred Meyer', 'Rx Rite Aid', 'Rx Walgreens',
                'TOW EXPRESS', 'UNKNOWN-INSURANCE', 'WAGE LOSS', 'bishoplegal', 'Healthport (Smart Document Solutions)']
    file = read(location)
    totalPossibleOptions = 0
    providerFile = file.File
    providerDict = file.Dictionary
    Provider = namedtuple('Provider', 'Name Address Phone ID')
    currentCase = previousCase = 0
    for elem in providerFile.index:
        if providerFile['compute_0005'][elem] not in toRemove:
            currentCase = providerFile['casenum'][elem]
            phone = str(providerFile['compute_0008'][elem])
            addr = str(providerFile['compute_0007'][elem])
            if phone:
                phone = phone.replace('(', '').replace(') ', '').replace(' - ', '')
            else:
                phone = 'NONE'
            if addr:
                addr = addr.replace('\n\n', ' ')
            else:
                addr = 'NONE'
            inst = Provider(providerFile['compute_0005'][elem],
                            addr,
                            phone,
                            providerFile['names_id'][elem])
            if hospitals != None:
                for i in hospitals:
                    res = searchRatio(inst.Name.upper(), i.Name.upper(), ratio)
                    if res:
                        if inst not in providerDict:
                            providerDict[inst] = 1
                        else:
                            providerDict[inst] += 1
            elif singleProvider != None:
                if totalPossibleOptions < 3:
                    res = searchRatio(inst.Name.upper(), singleProvider.upper(), ratio)
                    if res:
                        providerDict[inst] = 1
                        totalPossibleOptions += 1
                else:
                    log.loggingInfo('totalPossibleOptions', 'net.py', 'processFacility function') 
                    break
    
    return providerDict, providerFile, toRemove
    
    

def createNX(providerDict, providerFile, toRemove, netSize, weighted):
    singleElement = None
    race = int
    lessThan4 = ''
    if len(providerDict) == 1:
        for k,v in providerDict.items():
            singleElement = k
    elif len(providerDict) < 4:
        listOf4 = []
        for k,v in providerDict.items():
            listOf4.append(k.Name)
        lessThan4 = ''.join(str(listOf4))

    newDict = defaultdict(list)
    ProviderWeighted = namedtuple('ProviderWeighted', 'Name Address Phone ID Weight')
    Provider = namedtuple('Provider', 'Name Address Phone ID')
    needlesProvider = defaultdict(list)
    lst = []
    list_of_lists = []
    list_of_single_elem = []
    list_of_races = []
    ed = nx.Graph()
    current = prev = 0
    for elem in providerFile.index:
        prev = current
        current = providerFile['casenum'][elem]
        if current == prev:
            if providerFile['compute_0005'][elem] not in toRemove:
                phone = str(providerFile['compute_0008'][elem])
                addr = str(providerFile['compute_0007'][elem])
                try:
                    raceFirst = providerFile['race'][elem]
                    result = checkForNaN(raceFirst)
                    if result:
                        race = int(providerFile['race'][elem])
                except Exception as e:
                    log.loggingInfo(e, 'net.py', 'createNX function: race') 
                if phone:
                    phone = phone.replace('(', '').replace(') ', '').replace(' - ', '')
                else:
                    phone = 'NONE'
                if addr:
                    addr = addr.replace('\n\n', ' ')
                else:
                    addr = 'NONE'
                instP = Provider(providerFile['compute_0005'][elem],
                                addr,
                                phone,
                                providerFile['names_id'][elem])
                if race:
                    needlesProvider[instP].append(race)
                else:
                    needlesProvider[instP] = []
                lst.append(instP)
                
        else:
            #only one provider with that name was found
            if singleElement:
                if singleElement in lst:
                    for i in lst:
                        if singleElement != i:
                            list_of_single_elem.append(i)
            #3 or less providers with same name were found
            elif len(providerDict) < 4:
                for k, v in providerDict.items():
                    if k in lst:
                        for i in lst:
                            if k != i:
                                list_of_single_elem.append(i)
            list_of_lists.append(lst)
            lst = []
    for key, value in providerDict.items():
        inst = ProviderWeighted(key.Name, key.Address, key.Phone, key.ID, value)
        ed.add_node(key.Name)
        if ed.number_of_nodes() > 1:
            ed.remove_node(key.Name)
        if singleElement:
            count = Counter(list_of_single_elem)
            try:
                count = count.most_common(netSize)
                for i in count:
                    if weighted:
                        ed.add_edge(singleElement.Name, i[0].Name, weight = i[1])
                    else:
                        ed.add_edge(singleElement.Name, i[0].Name)
            except Exception as e:
                log.loggingInfo(e, 'net.py', 'createNX function: Counter.most_common') 
        elif lessThan4:
            count = Counter(list_of_single_elem)
            try:
                count = count.most_common(netSize)
                for i in count:
                    if weighted:
                        ed.add_edge(lessThan4, i[0].Name, weight = i[1])
                    else:
                        ed.add_edge(lessThan4, i[0].Name)
            except Exception as e:
                log.loggingInfo(e, 'net.py', 'createNX function: Counter.most_common2') 
        else:
            for l in list_of_lists[1:]:
                if key in l:
                    for i in l:
                        if i != key:
                            ed.add_edge(key.Name, i.Name)
                            newDict[inst].append(i)
    for key, value in needlesProvider.items():
        needlesProvider[key] = Counter(value)
    return providerDict, newDict, needlesProvider, ed


def providerDictToList(providerDict):
    lst = []
    for key,value in providerDict.items():
        lst.append(key)
    return lst
    
    

def createDicForDB(providerDict, needlesProvider):
    gmaps = googlemaps.Client(key = 'AIzaSyBePe2zZ69dI2-YMifPVmNirkarl86Hic4')
    #gmaps = googlemaps.Client(key = 'AIzaSyD2WQ2msw84ZYXOMSciz6YQtZ8W-PI6xIw') #1
    #gmaps = googlemaps.Client(key = 'AIzaSyCsATCl3uaPZGRcamcl11Nd1NnaLD8SIew') #3
    
    places = ['Phys', 'Physician', 'Physicians', 'Rad', 'Radiology', 'ER', 'Emergency', 'Imaging', 'Ambulance', 'Fire']
    lst = []
    n = 0
    geo = None
    needlesDict = defaultdict(list)
    FinalProvider = namedtuple('FinalProvider', 'Name Address Phone ID Weight Ru Es En Geo')
    for key, value in needlesProvider.items():
        for k,v in providerDict.items():
            #geocode_result = gmaps.geocode(addr)
                #geocode_result = geocoder.google(addr)
            if key.ID == k.ID:
                n += 1
                #check = checkForSpecialties(key.Name, places)
                if key.Address != 'NONE':
                    try:
                    #geoLoc = geocoder.google(key.Address)
                        geocode_result = gmaps.geocode(key.Address)
                        location = geocode_result[0]['geometry']['location']
                        geo = location['lat'], location['lng']
                        #geo = geoLoc.latlng
                    except Exception as e:
                        log.loggingInfo(e, 'net.py', 'createDicForDB: geolocation') 
                else:
                    geo = 'NONE'
                try:
                    inst = FinalProvider(key.Name, key.Address, key.Phone, key.ID, k.Weight, value[1], value[2], value[3], geo)
                    lst.append(inst)
                    pass
                except Exception as e:
                    log.loggingInfo(e, 'net.py', 'createDicForDB: namedtuple instance')
    print('Total providers:', n)
    return lst

def getFaxNeedles(location):
    file = read(location)
    providerFile = file.File
    dic = {}
    F = namedtuple('F', 'ID Fax')
    for elem in providerFile.index:
        ID = providerFile['names_id'][elem]
        fax = providerFile['fax_number'][elem]
        try:
            fax = int(fax)
        except ValueError as v:
            log.loggingInfo(v, 'net.py', 'getFaxNeedles: fax')
        if ID not in dic:
            dic[ID] = fax
    return dic
        
    
            
def checkForNaN(elem):
    if elem == elem:
        return True
    else:
        return False
        
    


        
        
