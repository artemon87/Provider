from net import *
from find import *
from myDB import *
import tkinter as tk
from ChartSwapSearching import *
from HospitalsBS import *
from yelp import *
import time
import random
import geocoder
from geopy.distance import great_circle
from geopy.distance import vincenty
import googlemaps
from textMessage import *
from time import gmtime, strftime
from hospitalUpdate import *
from queue import Queue
import log
import logging
from collections import namedtuple

        

myTextQueue = Queue()
myTextQueue2 = Queue()
myTextQueue3 = Queue()

def writeToQueue1(line):
    myTextQueue.put(line)

def getQueue1():
    return myTextQueue.get(0)

def writeToQueue2(line):
    myTextQueue2.put(line)

def getQueue2():
    return myTextQueue2.get(0)

def writeToQueue3(line):
    myTextQueue3.put(line)

def getQueue3():
    return myTextQueue3.get(0)


def createTablesInDB():
    DB = connectToDB()
    createHospitalDB(DB)
    createNeedlesDB(DB)
    createProviderDB(DB)

def connectToDB():
    return setupDB()

def createNeedlesList():
    needlesFile = 'netRace.xlsx'
    tupple = processAll(needlesFile)
    providerDict, dictWeighted, needlesProvider, ed = createNX(*tupple, 5)
    needlesList = createDicForDB(dictWeighted, needlesProvider)
    return needlesList

def updProviderSpecialty():
    lst = []
    DB = connectToDB()
    dic = {'Chiropractic': 'Chiropractors', 'Family Practice': 'Family Practice Near Me',
           'Medical Clinic' : 'Medical Clinic Near Me', 'Pediatrics' : 'Pediatrics Near Me',
           'Physicians' : 'Physicians Near Me'}
    Cor = namedtuple('Cor', 'Specialty oldSpecialty')
    for k,v in dic.items():
        inst = Cor(k, v)
        lst.append(inst)
    updateProviderSpecialty(DB, lst)

def updNeedlesSpecialty():
    lst = []
    DB = connectToDB()
    list_of_items = [['Chiropractic', 'Chiropractic'], ['Chiropractic', 'Chiro'], ['Chiropractic', 'DC'],
           ['Chiropractic', 'D.C.'], ['Hospital' , 'Medical Center'], ['Hospital' , 'Hospital'],
           ['Urgent Care' , 'Urgent Care'], ['Massage Therapy' , 'Massage'], ['Massage Therapy' , 'LMP'],
           ['Family Practice' , 'Medicine'], ['Family Practice' , 'MD'], ['Family Practice' , 'M.D.']]
    Cor = namedtuple('Cor', 'Specialty Name')
    for i in list_of_items:
        inst = Cor(i[0], i[1])
        print(i[0], i[1])
        lst.append(inst)
    updateNeedlesSpecialty(DB, lst)

    
def fillinDB(upNeedles,upYelp, upHospital, text):
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    line = ''
    totalSleep = 0
    createTablesInDB()
    DB = connectToDB()
    lst = []
    city = ['Seattle,WA', 'Federal Way,WA', 'Tacoma,WA', 'Bellevue,WA',
            'Everett,WA', 'Renton,WA', 'Lake City,WA', 'Sammamish,WA',
            'Lynnwood,WA']
    spec = ['Chiropractors', 'Chiropractic','Urgent Care', 'Orthopedic Doctor', 'Physical Therapy',
            'Pediatrics', 'Physicians', 'Massage Therapy', 'Diagnostic Imaging',
            'Medical Clinic', 'Family Practice']
    
    if upYelp:
        print('Started updating Yelp')
        random.shuffle(city)
        random.shuffle(spec)
        for c in city:
            for s in spec:
                result = lookup(s, c)
                line += 'Found '+str(len(result))+' '+str(s)+' in '+str(c)+'\n'
                print('Found',len(result), s, 'in',c)
                lst.append(result)
        writeToQueue1(line)
        if len(lst) == 0:
            return -1
        for elem in lst:
            addProvider(elem, DB)
    if upHospital:
        print('Started updating hospitals')
        hosp = findAllHospitals()
        addHospital(hosp, DB)
    if upNeedles:
        print('Started updating Needles')
        needlesList = createNeedlesList()
        addNeedlesProvider(needlesList, DB)
    return line
    
def confirmSearchProvider(name, text, displayArgs, ratio):
    line = ''
    dispName, dispAddr, dispPhone, dispFax, dispSpec, dispInfo = displayArgs
    lst = []
    DB = connectToDB()
    lst = readFromProviderName(DB, name)
    print('Lengthe of list returned from Provider Database', len(lst))
    line += 'Found '+ str(len(lst)) +' providers:\n\n'
    pand = readChartSwap('Washington')
    if lst:
        for elem in lst:
            try:
                line += str(elem.NAME)+ "\n"
                if dispAddr:
                    if elem.ADDRESS is not None:
                        line += str(elem.ADDRESS)
                        line += "\n"
                        line += elem.CITY
                        line += "\n"
                    else:
                        line += "Address: None\n"
                if dispPhone:
                    if elem.PHONE is not None:
                        line += "General Phone: "
                        line += str(elem.PHONE)
                        line += "\n"
                    else:
                        line += "General Phone: None\n"
                if dispFax:
                    if elem.FAX is not None:
                        line += "General Fax: "
                        line += str(elem.FAX)
                        line += "\n"
                    else:
                        line += "Fax: None\n"
                if dispInfo:
                    if elem.LINK is not None:
                        line += "Link: "
                        line += str(elem.LINK)
                        line += "\n"
                    else:
                        line += "Link: None\n"
                if dispSpec:
                    if elem.SPECIALTY is not None:
                        line += "Specialty: "
                        line += str(elem.SPECIALTY)
                        line += "\n"
                    else:
                        line += "Specialty: None\n"
                looking = findOnChartSwap(elem.NAME, pand, ratio)
                if len(looking) > 0:
                    line += "ChartSwap: "
                    line += ''.join(str(looking))
                line += "\n\n"
            except Exception as e:
                log.loggingWarning(e, 'searchHelp.py', 'confirmSearchProvider')
        print('Line is:', line)
    else:
        line += 'Nothing was found. Search again or update Yelp Database...\n'
    writeToQueue1(line)
    

def confirmProvider(fileToRead, name, text, displayArgs, ratio):
    line = ''
    dispName, dispAddr, dispPhone, dispFax, dispSpec, dispInfo = displayArgs
    DB = connectToDB()
    lst = []
    print('Going to Needles DB')
    lst = readFromNeedlesName(DB, name.upper())
    pand = readChartSwap('Washington')
    if lst:
        line += "Is that what you are looking for?\n\n"
        for elem in lst:
            line += str(elem.NAME) + '\n'
            if dispAddr:
                if elem.ADDRESS is not None:
                    line += str(elem.ADDRESS) + '\n'
                else:
                    line += 'Address: None'
                try:
                    line += str(elem.CITY) + '\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: addr')
            if dispPhone:
                if elem.PHONE is not None:
                    line += 'General Phone: '
                    line += str(elem.PHONE)
                    line += '\n'
                else:
                    line += 'Feneral Phone: None\n'
            if dispFax:
                if elem.FAX is not None:
                    line += 'General Fax: '
                    line += str(elem.FAX)
                    line += '\n'
                else:
                    line += 'General Fax: None\n'
            if dispInfo:
                try:
                    if elem.LINK is not None:
                        line += 'Link: '
                        line += str(elem.LINK)
                        line += '\n'
                    else:
                        line += 'Link: None\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: info')
            if dispSpec:
                try:
                    if elem.SPECIALTY is not None:
                        line += 'Umbrella/Specialty: '
                        line += str(elem.SPECIALTY)
                        line += '\n'
                    else:
                        line += 'Umbrella/Specialty: None\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: spec2')
            looking = findOnChartSwap(elem.NAME, pand, ratio)
            if len(looking) > 0:
                try:
                    line += 'ChartSwap: ' 
                    line += ''.join(str(looking)) 
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: chartSwap')
            line += '\n\n'
    else:
        line = findProvider(fileToRead, name, ratio, text)
    writeToQueue1(line)



def confirmSearchHospital(name, text, displayArgs, ratio):
    line = ''
    dispName, dispAddr, dispPhone, dispFax, dispSpec, dispInfo = displayArgs
    DB = connectToDB()
    umbr = {'SWEDISH': False, 'MULTICARE': False, 'PROVIDENCE': False, 'FRANCISACAN': False,
            'UW MEDICINE': False, 'PEACEHEALTH': False, 'CONFLUENCE': False}
    facility = ''
    lst = []
    for k,v in umbr.items():
        result = searchFirst(k, name.upper())
        if result:
            umbr[k] = True
            facility = k
            lst = readFromHospitalUmbrella(DB, facility)
    pand = readChartSwap('Washington')
    if not lst:
        print('Going to Hospital DB')
        lst = readFromHospitalName(DB, name.upper())
    if lst:
        line += 'Is that what you are looking for?\n\n'
        for elem in lst:
            line += str(elem.NAME) +'\n'
            if dispAddr:
                if elem.ADDRESS is not None:
                    line += str(elem.ADDRESS) + '\n'
                else:
                    line += 'Address: None\n'
                try:
                    line += str(elem.CITY) + '\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: addr')
            if dispPhone:
                if elem.PHONE is not None:
                    line += 'General Phone: '
                    line += str(elem.PHONE)
                    line += '\n'
                else:
                    line += 'General Phone: None'
            if dispFax:
                if elem.FAX is not None:
                    line += 'General Fax: '
                    line += str(elem.FAX)
                    line += '\n'
                else:
                    line += 'General Fax: None'
                try:
                    if elem.RECORDS is not None:
                        line += 'Records Fax: '
                        line += str(elem.RECORDS)
                        line += '\n'
                    else:
                        line += 'Records Fax: None\n'
                    if elem.BILLING is not None:
                        line += 'Billing Fax: '
                        line += str(elem.BILLING)
                        line += '\n'
                    else:
                        line += 'Billing Fax: NOne'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: fax')
            if dispInfo:
                try:
                    if elem.LINK is not None:
                        line += 'Link: '
                        line += str(elem.LINK)
                        line += '\n'
                    else:
                        line += 'Link: None\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: info')
            if dispSpec:
                try:
                    if elem.UMBRELLA is not None:
                        line += 'Umbrella: '
                        line += str(elem.UMBRELLA)
                        line += '\n'
                    else:
                        line += 'Umbrella/Speciakty: None\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: spec')
            looking = findOnChartSwap(elem.NAME, pand, ratio)
            if len(looking) > 0:
                try:
                    line += 'ChartSwap: '
                    line += ''.join(str(looking))
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: chartSwap')
            line += '\n\n'
    else:
        line = ''
        line += 'Nothing was found. Search again or update Hospital Database...\n'
    writeToQueue1(line)


def readED(fileToRead, hosp, name, n, ratio, weighted = None):
    args = processFacility(fileToRead, hosp, name, ratio)
    providerDict, newDict, needlesProvider, ed = createNX(*args, n, weighted)
    return ed, providerDict

def printOutProvider(providerDict, text, displayArgs, ratio):
    line = ''
    line += 'Network was created. Please see Network Graph for details...\n\n'
    print('printOUTProvider launched!')
    dispName, dispAddr, dispPhone, dispFax, dispSpec, dispInfo = displayArgs
    DB = connectToDB()
    lst = []
    name = None
    for k,v in providerDict.items():
        print('LOOKING FOR: ', k.Name)
        lst = readFromNeedlesNameExact(DB,k.Name)
    if not lst:
        print('Nothing was wound with EXACT name;')
        line += 'Nothing was found'
    for elem in lst:
        line += str(elem.NAME) + '\n'
        if dispAddr:
            if elem.ADDRESS is not None:
                line += str(elem.ADDRESS) + '\n'
            else:
                line += 'Address: None\n'
        if dispPhone:
            if elem.PHONE is not None:
                line += 'General Phone: '
                line += str(elem.PHONE)
                line += '\n'
            else:
                text.insert(tk.INSERT, "Feneral Phone: None\n")
                line += 'Feneral Phone: None\n'
        if dispFax:
             if elem.FAX is not None:
                 line += 'General Fax: '
                 line += str(elem.FAX)
                 line += '\n'
             else:
                 line += 'General Fax: None\n'
        if dispInfo:
            try:
                if elem.LINK is not None:
                    line += 'Link: '
                    line += str(elem.LINK)
                    line += '\n'
                else:
                    line += 'Link: None\n'
            except Exception as e:
                log.loggingWarning(e, 'searchHelp.py', 'printOutProvider: link')
            try:
                if elem.WEIGHT is not None:
                    line += 'Popularity: '
                    line += str(elem.WEIGHT)
                    line += ' clients served for the last 2 years\n'

            except Exception as e:
                log.loggingWarning(e, 'searchHelp.py', 'printOutProvidr: weight')
        pand = readChartSwap('Washington')
        looking = findOnChartSwap(elem.NAME, pand, ratio)
        if len(looking) > 0:
            try:
                line += 'ChartSwap: '
                line += ''.join(str(looking))
            except Exception as e:
                log.loggingWarning(e, 'searchHelp.py', 'printOutProvider: ChartSwap')
        line += '\n\n'
    writeToQueue1(line)


def findProvider(fileToRead, name, ratio, text):
    line = ''
    line += 'Finding provider. Please wait...\n'
    print('FIND PROVIDER LOUNCHED')
    providerDict, *rest = processAll(fileToRead)
    newList = providerDictToList(providerDict)
    possibleOptions = deepSearch(name, newList, 10, ratio)
    if len(possibleOptions) < 10:
        print('Less than 10 providers found')
        possibleOptions = deepSearch(name, newList, 10, 0.2)
    if len(possibleOptions) < 1:
        print('Less than 1 providers found')
        possibleOptions = searchFirstDict(name, providerDict)
    if len(possibleOptions) == 0:
        line += 'Nothing was found with your search term\nPlease try again...\n'
        return
    else:
        try:
            possibleOptions = deepSearch(possibleOptions[0].Name, newList, 10, 0.2)
        except Exception as e:
            log.loggingWarning(e, 'searchHelp.py', 'findProvider: possibleOptions')
    line += 'Is that what you are looking for...?\n\n'
    for i in possibleOptions:
        line += str(i) + '\n'
    line += '\n'
    writeToQueue1(line)

def treatmentPlan(language, text, sLocation, radius, needlesOnly, avoidPhys, onlyChiro, sortBy):
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    line = ''
    radius = float(radius)
    gmaps = googlemaps.Client(key = 'AIzaSyBePe2zZ69dI2-YMifPVmNirkarl86Hic4')
    #gmaps = googlemaps.Client(key = 'AIzaSyBePe2zZ69dI2-YMifPVmNirkarl86Hic4')
    #gmaps = googlemaps.Client(key = 'AIzaSyD2WQ2msw84ZYXOMSciz6YQtZ8W-PI6xIw') #1
    #gmaps = googlemaps.Client(key = 'AIzaSyCsATCl3uaPZGRcamcl11Nd1NnaLD8SIew') 
    #   AIzaSyCsATCl3uaPZGRcamcl11Nd1NnaLD8SIew
    lst = []
    lst2 = []
    lst3 = []
    check = True
    allProviders = True
    geocode_result = None
    places = ['Phys', 'Physician', 'Physicians', 'Rad', 'Radiology',
              'ER', 'Emergency', 'Imaging', 'Ambulance', 'Fire', 'City of', 'Pathology']
    languageDict = {'Russian': 1, 'Spanish': 2, 'English' : 3, 'Unspecified': 4}
    txPlanDict = {}
    if ', WA' not in sLocation.upper() or ',WA' not in sLocation.upper() or ' WA' not in sLocation.upper():
        sLocation = sLocation + ' WA'
        print(sLocation)
    DB = connectToDB()
    if not needlesOnly:
        lst2 = readFromHospital(DB)
        lst3 = readFromProvider(DB)
    lst = readFromNeedlesAll(DB)
    loc1 = None
    try:
        geocode_result = gmaps.geocode(sLocation)
    except Exception as e:
        print(e)
        log.loggingWarning(e, 'searchHelp.py', 'geocode_result = gmaps.geocode(sLocation)')
    if geocode_result:
        try:
            location = geocode_result[0]['geometry']['location']
            loc1 = location['lat'], location['lng']
        except Exception as e:
            print(e)
            log.loggingWarning(e, 'searchHelp.py', 'treatmentPlan: couldnt create GEOcoder')
    if loc1 is None:
        line += 'Cant find this location. Please try again...\n'
        line += 'Either enter full address or in this format: [city, state]...\n'
        writeToQueue2(line)
        return
    loc2 = None
    distance = float
    for elem in lst:
        try:
            if elem.GEO is not 'NONE' or elem.GEO is not None:
                loc2 = elem.GEO
                #distance = great_circle(loc1.latlng, loc2).miles
                distance = great_circle(loc1, loc2).miles
                if distance < radius:
                    txPlanDict[elem] = distance
            else:
                pass
        except Exception as e:
            log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: GEO in lst')
    if lst2:
        for elem in lst2:
            try:
                if elem.GEO is not 'NONE' or elem.GEO is not None:
                    loc2 = elem.GEO
                    #distance = great_circle(loc1.latlng, loc2).miles 
                    distance = great_circle(loc1, loc2).miles
                    if distance < radius:
                        txPlanDict[elem] = distance
                else:
                    pass
            except Exception as e:
                log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: GEO in lst2')
    if lst3:
        for elem in lst3:
            try:
                if elem.GEO is not 'NONE' or elem.GEO is not None:
                    loc2 = elem.GEO
                    #distance = great_circle(loc1.latlng, loc2).miles
                    distance = great_circle(loc1, loc2).miles
                    if distance < radius:
                        txPlanDict[elem] = distance
                else:
                    pass
            except Exception as e:
                log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: GEO in lst3')
    list_of_items = []
    single_list = []
    list_of_items_tup = []
    for key, value in txPlanDict.items():
        if avoidPhys:
            check = checkForSpecialties(key.NAME, places)
        if check:
            if languageDict[language] == 1:
                try:
                    if key.RU > 3:
                        l , single_list, inst = printProviderTX(text, key, value, language)
                        line += l
                except Exception as e:
                    log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: RU')
                    l , single_list, inst = printProviderTX(text, key, value, language)
                    line += l
            elif languageDict[language] == 2:
                try:
                    if key.ES > 3:
                        l , single_list, inst = printProviderTX(text, key, value, language)
                        line += l
                except Exception as e:
                    log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: ES')
                    l , single_list, inst = printProviderTX(text, key, value, language)
                    line += l
            elif languageDict[language] == 3:
                try:
                    if key.EN > 3:
                        l , single_list, inst = printProviderTX(text, key, value, language)
                        line += l
                except Exception as e:
                    log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: EN')
                    l , single_list, inst = printProviderTX(text, key, value, language)
                    line += l
            elif languageDict[language] == 4:
                try:
                    if key.RU >= 0 or key.ES >= 0 or key.EN >= 0:
                        l , single_list, inst = printProviderTX(text, key, value, language)
                        line += l
                except Exception as e:
                    log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: ALL languages')
                    l , single_list, inst = printProviderTX(text, key, value, language)
                    line += l
            if single_list:
                list_of_items.append(single_list)
                list_of_items_tup.append(inst)
                single_list = []
    
    newString = ''
    mySortedList = None
    mySortedList2 = None
    if sortBy == 1:
        mySortedList = sorted(list_of_items, key =lambda  x: x[0])
        mySortedList2 = sorted(list_of_items_tup, key =lambda  x: x.Name)
    elif needlesOnly and sortBy == 2:
        mySortedList = sorted(list_of_items, key =lambda  x: int(x[5]), reverse=True)
        mySortedList2 = sorted(list_of_items_tup, key =lambda  x: int(x.Pop), reverse=True)
    elif sortBy == 4:
        mySortedList2 = sorted(list_of_items_tup, key =lambda  x: str(x.Spec))
    else:
        mySortedList = sorted(list_of_items, key =lambda  x: float(x[2]))
        mySortedList2 = sorted(list_of_items_tup, key =lambda  x: float(x.Dis))
    for i in mySortedList2:
        newString += str(i.Name) + ' is only '+str(i.Dis)+' miles away from you\n'
        if i.Pop:
            newString += 'There were '+str(i.Pop) +' '+ str(i.Lan) + ' speeking clients in the past 2 years\n'
        newString += 'Full Address: '+str(i.Addr)
        if i.City:
            newString += ', '+str(i.City)
        newString += '\nPhone: '+str(i.Phone)
        if i.Spec:
            newString += '\nSpecialty: '+str(i.Spec)
        newString += '\n\n'
    '''finalPrint = [inner for outer in mySortedList for inner in outer]'''
    if len(line) == 0:
        line += 'Nothing was found with your request. Try again...\n'
    #writeToQueue2(''.join(finalPrint))
    writeToQueue2(newString)
            
    return True

def printProviderTX(text, provider, value, language):
    NT = namedtuple('NT', 'Name Dis Pop Lan Addr City Phone Spec')
    single_list = []
    line = ''
    name = str(provider.NAME)
    line += ' is only '
    single_list.append(str(provider.NAME))
    single_list.append(' is only ')
    dis = str(round(value, 2))
    single_list.append(str(round(value, 2)))
    line += ' miles away from you\n'
    single_list.append(' miles away from you\n')
    pop = None
    lan = None
    try:
        if provider.WEIGHT:
            line += 'There were '
            single_list.append('There were ')
            pop = str(provider.WEIGHT)
            single_list.append(str(provider.WEIGHT))
            line += ' '
            single_list.append(' ')
            lan = str(language)
            single_list.append(str(language))
            line += ' speeking clients in the past 2 years\n'
            single_list.append(' speeking clients in the past 2 years\n')
    except Exception as e:
        log.loggingInfo(e, 'searchHelp.py', 'printProviderTX: Weight')
    line += 'Full Address: '
    single_list.append('Full Address: ')
    addr = str(provider.ADDRESS)
    single_list.append(str(provider.ADDRESS))
    city = None
    try:
        if provider.CITY:
            line += ', '
            single_list.append(', ')
            city = str(provider.CITY)
            single_list.append(str(provider.CITY))
    except Exception as e:
        log.loggingInfo(e, 'searchHelp.py', 'printProviderTX: City')
    line +='\n'
    single_list.append('\n')
    line += 'Phone: '
    single_list.append('Phone: ')
    phone = str(provider.PHONE)
    single_list.append(str(provider.PHONE))
    spec = None
    try:
        if provider.SPECIALTY:
            line += '\n'
            single_list.append('\n')
            line += 'Specialty: '
            single_list.append('Specialty: ')
            spec = str(provider.SPECIALTY)
            single_list.append(str(provider.SPECIALTY))
    except Exception as e:
        log.loggingInfo(e, 'searchHelp.py', 'printProviderTX: Specialty')
    line += '\n\n'
    single_list.append('\n\n')
    if not spec:
        spec = 'Needles provider: undefined'
    inst = NT(name, dis, pop, lan, addr, city, phone, spec)
    return line, single_list, inst

def updateFaxInNeedles():
    DB = connectToDB()
    dic = getFaxNeedles('netFax.xlsx')
    updateNeedlesFax(DB, dic)

def updateHospitalGeoLocation():
    gmaps = googlemaps.Client(key = 'AIzaSyBePe2zZ69dI2-YMifPVmNirkarl86Hic4')
    DB = connectToDB()
    geo = None
    P = namedtuple('P', 'Name, Geo')
    lstWithGeo = []
    lst = readFromHospital(DB)
    for i in lst:
        fullAddress = i.ADDRESS + i.CITY
        geocode_result = gmaps.geocode(fullAddress)
        if geocode_result:
            try:
                location = geocode_result[0]['geometry']['location']
                geo = location['lat'], location['lng']
            except Exception as e:
                log.loggingWarning(e, 'searchHelp.py', 'updateHospitalGeoLocation')
        else:
            geo = 'NONE'
        inst = P(i.NAME, geo)
        lstWithGeo.append(inst)
    updateHospitalGEO(DB, lstWithGeo)

def updateProviderGeoLocation():
    gmaps = googlemaps.Client(key = 'AIzaSyBePe2zZ69dI2-YMifPVmNirkarl86Hic4')
    #gmaps = googlemaps.Client(key = 'AIzaSyBePe2zZ69dI2-YMifPVmNirkarl86Hic4')
    #gmaps = googlemaps.Client(key = 'AIzaSyD2WQ2msw84ZYXOMSciz6YQtZ8W-PI6xIw') #1
    #gmaps = googlemaps.Client(key = 'AIzaSyCsATCl3uaPZGRcamcl11Nd1NnaLD8SIew') 
    DB = connectToDB()
    geo = None
    P = namedtuple('P', 'Name Phone Geo')
    lstWithGeo = []
    lst = readFromProvider(DB)
    n = 0
    for i in lst[5497:]:
        if i.ADDRESS and i.CITY: 
            fullAddress = i.ADDRESS + i.CITY
            geocode_result = gmaps.geocode(fullAddress)
            if geocode_result:
                try:
                    location = geocode_result[0]['geometry']['location']
                    geo = location['lat'], location['lng']
                    n += 1
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'updateProviderGeoLocation')
                inst = P(i.NAME, i.PHONE, geo)
                lstWithGeo.append(inst)
                if n >= 2000:
                    log.loggingWarning('GOOGLE', 'searchHelp.py', 'updateProviderGeoLocation: reached QUERY limit')
                    break
    updateProviderGEO(DB, lstWithGeo)

def updateProviderMissingGeoLocation():
    gmaps = googlemaps.Client(key = 'AIzaSyBePe2zZ69dI2-YMifPVmNirkarl86Hic4')
    #gmaps = googlemaps.Client(key = 'AIzaSyBePe2zZ69dI2-YMifPVmNirkarl86Hic4')
    #gmaps = googlemaps.Client(key = 'AIzaSyD2WQ2msw84ZYXOMSciz6YQtZ8W-PI6xIw') 
    #gmaps = googlemaps.Client(key = 'AIzaSyCsATCl3uaPZGRcamcl11Nd1NnaLD8SIew') 
    DB = connectToDB()
    geo = None
    P = namedtuple('P', 'Name Phone Geo')
    lstWithGeo = []
    lst = readFromProvider(DB)
    n = 0
    for i in lst[5497:]:
        if not i.GEO or i.GEO == 'NONE':
            if i.ADDRESS and i.CITY: 
                fullAddress = i.ADDRESS + i.CITY
                geocode_result = gmaps.geocode(fullAddress)
                if geocode_result:
                    try:
                        location = geocode_result[0]['geometry']['location']
                        geo = location['lat'], location['lng']
                        n += 1
                    except Exception as e:
                        log.loggingWarning(e, 'searchHelp.py', 'updateProviderMissingGeoLocation')
                    inst = P(i.NAME, i.PHONE, geo)
                    lstWithGeo.append(inst)
                    if n >= 2000:
                        log.loggingWarning('GOOGLE', 'searchHelp.py', 'updateProviderMissingGeoLocation: reached QUERY limit')
                        break
        else:
            continue
    updateProviderGEO(DB, lstWithGeo)

def sendMessageToClient(msg, number, filePath, popUp, attachment = None):
    MSG = namedtuple('MSG', 'Number Note Date Attachment')
    timeSent = strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    inst = MSG(number, msg, timeSent, filePath)
    DB = connectToDB()
    createMessageDB(DB)
    addMessage(DB, inst)
    newMessage = textMessage()
    newMessage.fillInList(number)
    result = newMessage.sendText(msg, filePath, attachment)
    if result:
        popUp.showinfo('Confirmation', 'Message sent')
        addMessage(DB, inst)
    else:
        popUp.showinfo('Confirmation', 'Message failed')

def displaySentMessages(text):
    line = ''
    DB = connectToDB()
    lst = readFromMessage(DB)
    for elem in lst:
        line += 'ID: ' + str(elem.ID) + ' .Sent to: '+str(elem.Number)+'\nMessage: '+str(elem.Note)+'Sent on: '+str(elem.Date)+'\n'
        if elem.Attachment:
            line += 'Attachment: '+str(elem.Attachment)+'\n'
        line += '\n'
    writeToQueue3(line)

def updateHospRecordsFax():
    #2534266408, (206) 215-2757
    swedishFax = updateSwedish()
    multicareFax = updateMulticare()
    uwmediceFax = updateUW()
    DB = connectToDB()
    franciscanDict = {'FRANCIS HOSPITAL': 2539447916,
                      'JOSEPH MEDICAL CENTER': 2534266924,
                      'CLARE HOSPITAL' : 2534266924,
                      'ANTHONY HOSPITAL' : 2534266924,
                      'HIGHLINE MEDICAL CENTER' : 2534266924,
                      'ELIZABETH HOSPITAL' : 3608028519,
                      'HARRISON MEDICAL CENTER' : 3607446607,
                      }
    hospitalsRBDict = {'OVERLAKE MEDICAL CENTER' : [4254673343, 4256885658],
                    'Regional Medical Center Everett' : [4253170701, 4253170701],
                       'EvergreenHealth' : [4258991933, 4258991933],
                       'CASCADE VALLEY HOSPITAL AND CLINICS' : [3604350525, 3604350525],
                       'CASCADE MEDICAL CENTER' : [5095482524, 5095482524],
                       'CENTRAL WASHINGTON HOSPITAL' : [5096626770, 5096626770],
                       'WENATCHEE VALLEY HOSPITAL & CLINICS' : [5096655891, 5096655891],
                       'EAST ADAMS RURAL HEALTHCARE' : [5096591113, 5096591113],
                       'GRAYS HARBOR COMMUNITY HOSPITAL' : [3605370588, 3605376100],
                       'GROUP HEALTH COOPERATIVE' : [2063262599, 2063262599],
                       'KADLEC REGIONAL MEDICAL CENTER' : [5099422701, 5099422701],
                       'KITTITAS VALLEY HEALTHCARE' : [5099627413, 5099627413],
                       'LEGACY SALMON CREEK MEDICAL CENTER' : [3604873419, 3604873419],
                       'NORTHWEST HOSPITAL' : [2066681920, 2066681920],
                       'MASON GENERAL HOSPITAL' : [3604279592, 3604279592],
                       'SACRED HEART MEDICAL CENTER & CHILDREN’S HOSPITAL' : [5094744815, 'None'],
                       'SEATTLE CHILDREN’S' : [2069853252, 2069853252],
                       'SHRINERS HOSPITALS FOR CHILDREN' : [5097441256, 5097441256],
                       'SUNNYSIDE COMMUNITY HOSPITAL' : [5098371637, 5098371637],
                       'VIRGINIA MASON MEDICAL CENTER' : [2062238885, 2065155803],
                       'YAKIMA REGIONAL MEDICAL AND CARDIAC CENTER' : [5095755244, 5095755244]}
                      
    umbrellaDict = {'SWEDISH': [swedishFax, 2062152757], 'MULTICARE': [multicareFax, multicareFax],
                    'uw' : [uwmediceFax, 2065980842]}
    
    for key, value in umbrellaDict.items():
        updateRecordsHospitalUmbrella(DB, key, value[0])
        updateBillingHospitalUmbrella(DB, key, value[1])
    for key, value in franciscanDict.items():
        updateRecordsHospitalName(DB, key, value)
        updateBillingHospitalName(DB, key, value)
    for key, value in hospitalsRBDict.items():
        updateRecordsHospitalName(DB, key, value[0])
        updateBillingHospitalName(DB, key, value[1])

def createNodeSize(links, weighted = None):
    startSize = 300
    nodeSizes = []
    for i in range(links + 1):
        nodeSizes.append(startSize)
        if weighted:
            startSize += 300
    return nodeSizes
        
    
            
        
        
    
    

    
        
        
        
    
    
    
