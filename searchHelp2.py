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

'''class textQueue:
    def __init__(self):
        self.queue1 = Queue()
        self.queue2 = Queue()
        self.queue3 = Queue()

    def writeToQueue1(self, line):
        self.queue1.put(line)

    def writeToQueue2(self, line):
        self.queue2.put(line)

    def writeToQueue3(self, line):
        self.queue3.put(line)

    @staticmethod 
    def getQueue1():
        return queue1.get(0)

    @staticmethod
    def getQueue2():
        return self.queue2.get(0)

    @staticmethod
    def getQueue3():
        return self.queue3.get(0)
    def myQueue():
        pass'''
        

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

'''def clearScreen(text):
    try:
        text.delete(1.0,tk.END)
    except Exception as e:
        log.loggingWarning(e, 'searchHelp.py', 'clearScreen')'''

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

def fillinDB(upNeedles,upYelp, upHospital, text):
    line = ''
    #clearScreen(text)
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
                #text.insert(tk.INSERT, 'Found ')
                line += 'Found '
                #text.insert(tk.INSERT, len(result))
                line += str(len(result))
                #text.insert(tk.INSERT, ' ')
                line += ' '
                #text.insert(tk.INSERT, s+' in ')
                line += str(s)+' in '+str(c)+'\n'
                #text.insert(tk.INSERT, c+'\n')
                print('Found',len(result), s, 'in',c)
                lst.append(result)
                writeToQueue1(line)
        for elem in lst:
            addProvider(elem, DB)
        if len(lst) == 0:
            return -1
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
    #clearScreen(text)
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
                #text.insert(tk.INSERT, elem.NAME+ "\n")
                if dispAddr:
                    if elem.ADDRESS is not None:
                        #text.insert(tk.INSERT, elem.ADDRESS)
                        line += str(elem.ADDRESS)
                        #text.insert(tk.INSERT, "\n")
                        line += "\n"
                        #text.insert(tk.INSERT, elem.CITY)
                        line += elem.CITY
                        #text.insert(tk.INSERT, "\n")
                        line += "\n"
                    else:
                        #text.insert(tk.INSERT, "Address: None\n")
                        line += "Address: None\n"
                if dispPhone:
                    if elem.PHONE is not None:
                        #text.insert(tk.INSERT, "General Phone: ")
                        line += "General Phone: "
                        #text.insert(tk.INSERT, elem.PHONE)
                        line += str(elem.PHONE)
                        #text.insert(tk.INSERT, "\n")
                        line += "\n"
                    else:
                        #text.insert(tk.INSERT, "General Phone: None\n")
                        line += "General Phone: None\n"
                if dispFax:
                    if elem.FAX is not None:
                        #text.insert(tk.INSERT, "General Fax: ")
                        line += "General Fax: "
                        #text.insert(tk.INSERT, elem.FAX)
                        line += str(elem.FAX)
                        #text.insert(tk.INSERT, "\n")
                        line += "\n"
                    else:
                        #text.insert(tk.INSERT, "Fax: None\n")
                        line += "Fax: None\n"
                if dispInfo:
                    if elem.LINK is not None:
                        #text.insert(tk.INSERT, "Link: ")
                        line += "Link: "
                        #text.insert(tk.INSERT, elem.LINK)
                        line += str(elem.LINK)
                        #text.insert(tk.INSERT, "\n")
                        line += "\n"
                    else:
                        #text.insert(tk.INSERT, "Link: None\n")
                        line += "Link: None\n"
                if dispSpec:
                    if elem.SPECIALTY is not None:
                        #text.insert(tk.INSERT, "Specialty: ")
                        line += "Specialty: "
                        #text.insert(tk.INSERT, elem.SPECIALTY)
                        line += str(elem.SPECIALTY)
                        #text.insert(tk.INSERT, "\n")
                        line += "\n"
                    else:
                        #text.insert(tk.INSERT, "Specialty: None\n")
                        line += "Specialty: None\n"
                looking = findOnChartSwap(elem.NAME, pand, ratio)
                if len(looking) > 0:
                    #text.insert(tk.INSERT, 'ChartSwap: ')
                    line += "ChartSwap: "
                    #text.insert(tk.INSERT, ''.join(str(looking)))
                    line += ''.join(str(looking))
                #text.insert(tk.INSERT,"\n")
                #text.insert(tk.INSERT,"\n")
                line += "\n\n"
            except Exception as e:
                log.loggingWarning(e, 'searchHelp.py', 'confirmSearchProvider')
        print('Line is:', line)
    else:
        #text.insert(tk.INSERT,"Nothing was found. Search again or update Yelp Database...")
        line += 'Nothing was found. Search again or update Yelp Database...\n'
        #text.insert(tk.INSERT,"\n")
    writeToQueue1(line)
    

def confirmProvider(fileToRead, name, text, displayArgs, ratio):
    line = ''
    dispName, dispAddr, dispPhone, dispFax, dispSpec, dispInfo = displayArgs
    DB = connectToDB()
    lst = []
    #clearScreen(text)
    print('Going to Needles DB')
    lst = readFromNeedlesName(DB, name.upper())
    pand = readChartSwap('Washington')
    if lst:
        #clearScreen(text)
        #text.insert(tk.INSERT, "Is that what you are looking for?\n\n")
        line += "Is that what you are looking for?\n\n"
        for elem in lst:
            #text.insert(tk.INSERT, elem.NAME+ "\n")
            line += str(elem.NAME) + '\n'
            if dispAddr:
                if elem.ADDRESS is not None:
                    #text.insert(tk.INSERT, elem.ADDRESS+ "\n")
                    line += str(elem.ADDRESS) + '\n'
                else:
                    #text.insert(tk.INSERT, "Address: None")
                    line += 'Address: None'
                try:
                    #text.insert(tk.INSERT, elem.CITY+ "\n")
                    line += str(elem.CITY) + '\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: addr')
            if dispPhone:
                if elem.PHONE is not None:
                    #text.insert(tk.INSERT, "General Phone: ")
                    line += 'General Phone: '
                    #text.insert(tk.INSERT, elem.PHONE)
                    line += str(elem.PHONE)
                    #text.insert(tk.INSERT, "\n")
                    line += '\n'
                else:
                    #text.insert(tk.INSERT, "Feneral Phone: None\n")
                    line += 'Feneral Phone: None\n'
            if dispFax:
                if elem.FAX is not None:
                    #text.insert(tk.INSERT, "General Fax: ")
                    line += 'General Fax: '
                    #text.insert(tk.INSERT, elem.FAX)
                    line += str(elem.FAX)
                    
                    #text.insert(tk.INSERT, "\n")
                    line += '\n'
                else:
                    #text.insert(tk.INSERT, "General Fax: None\n")
                    line += 'General Fax: None\n'
            if dispInfo:
                try:
                    if elem.LINK is not None:
                        #text.insert(tk.INSERT, "Link: ")
                        line += 'Link: '
                        #text.insert(tk.INSERT, elem.LINK)
                        line += str(elem.LINK)
                        #text.insert(tk.INSERT, "\n")
                        line += '\n'
                    else:
                        #text.insert(tk.INSERT, "Link: None\n")
                        line += 'Link: None\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: info')
            if dispSpec:
                try:
                    if elem.SPECIALTY is not None:
                        #text.insert(tk.INSERT, "Umbrella/Specialty: ")
                        line += 'Umbrella/Specialty: '
                        #text.insert(tk.INSERT, elem.SPECIALTY)
                        line += str(elem.SPECIALTY)
                        #text.insert(tk.INSERT, "\n")
                        line += '\n'
                    else:
                        #text.insert(tk.INSERT, "Umbrella/Specialty: None\n")
                        line += 'Umbrella/Specialty: None\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: spec2')
            looking = findOnChartSwap(elem.NAME, pand, ratio)
            if len(looking) > 0:
                try:
                    #text.insert(tk.INSERT, 'ChartSwap: ')
                    line += 'ChartSwap: ' 
                    #text.insert(tk.INSERT, ''.join(str(looking)))
                    line += ''.join(str(looking)) 
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: chartSwap')
            #text.insert(tk.INSERT,"\n")
            #text.insert(tk.INSERT,"\n")
            line += '\n\n'
    else:
        line = findProvider(fileToRead, name, ratio, text)
        #text.insert(tk.INSERT,"Nothing was found. Search again...")
        #text.insert(tk.INSERT,"\n")
        #line += 'Nothing was found. Search again...\n'
    writeToQueue1(line)



def confirmSearchHospital(name, text, displayArgs, ratio):
    line = ''
    dispName, dispAddr, dispPhone, dispFax, dispSpec, dispInfo = displayArgs
    DB = connectToDB()
    umbr = {'SWEDISH': False, 'MULTICARE': False, 'PROVIDENCE': False, 'FRANCISACAN': False,
            'UW MEDICINE': False, 'PEACEHEALTH': False, 'CONFLUENCE': False}
    facility = ''
    lst = []
    #clearScreen(text)
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
        #clearScreen(text)
        text.insert(tk.INSERT, "Is that what you are looking for?\n\n")
        line += 'Is that what you are looking for?\n\n'
        for elem in lst:
            #text.insert(tk.INSERT, elem.NAME+ "\n")
            line += str(elem.NAME) +'\n'
            if dispAddr:
                if elem.ADDRESS is not None:
                    #text.insert(tk.INSERT, elem.ADDRESS+ "\n")
                    line += str(elem.ADDRESS) + '\n'
                else:
                    #text.insert(tk.INSERT, "Address: None\n")
                    line += 'Address: None\n'
                try:
                    #text.insert(tk.INSERT, elem.CITY+ "\n")
                    line += str(elem.CITY) + '\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: addr')
            if dispPhone:
                if elem.PHONE is not None:
                    #text.insert(tk.INSERT, "General Phone: ")
                    line += 'General Phone: '
                    #text.insert(tk.INSERT, elem.PHONE)
                    line += str(elem.PHONE)
                    #text.insert(tk.INSERT, "\n")
                    line += '\n'
                else:
                    #text.insert(tk.INSERT, "General Phone: None\n")
                    line += 'General Phone: None'
            if dispFax:
                if elem.FAX is not None:
                    #text.insert(tk.INSERT, "General Fax: ")
                    line += 'General Fax: '
                    #text.insert(tk.INSERT, elem.FAX)
                    line += str(elem.FAX)
                    #text.insert(tk.INSERT, "\n")
                    line += '\n'
                else:
                    #text.insert(tk.INSERT, "General Fax: None\n")
                    line += 'General Fax: None'
                try:
                    if elem.RECORDS is not None:
                        #text.insert(tk.INSERT, "Records Fax: ")
                        line += 'Records Fax: '
                        #text.insert(tk.INSERT, elem.RECORDS)
                        line += str(elem.RECORDS)
                        #text.insert(tk.INSERT, "\n")
                        line += '\n'
                    else:
                        #text.insert(tk.INSERT, "Records Fax: None\n")
                        line += 'Records Fax: None\n'
                    if elem.BILLING is not None:
                        #text.insert(tk.INSERT, "Billing Fax: ")
                        line += 'Billing Fax: '
                        #text.insert(tk.INSERT, elem.BILLING)
                        line += str(elem.BILLING)
                        #text.insert(tk.INSERT, "\n")
                        line += '\n'
                    else:
                        #text.insert(tk.INSERT, "Billing Fax: None\n")
                        line += 'Billing Fax: NOne'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: fax')
            if dispInfo:
                try:
                    if elem.LINK is not None:
                        #text.insert(tk.INSERT, "Link: ")
                        line += 'Link: '
                        #text.insert(tk.INSERT, elem.LINK)
                        line += str(elem.LINK)
                        #text.insert(tk.INSERT, "\n")
                        line += '\n'
                    else:
                        #text.insert(tk.INSERT, "Link: None\n ")
                        line += 'Link: None\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: info')
            if dispSpec:
                try:
                    if elem.UMBRELLA is not None:
                        #text.insert(tk.INSERT, "Umbrella: ")
                        line += 'Umbrella: '
                        #text.insert(tk.INSERT, elem.UMBRELLA)
                        line += str(elem.UMBRELLA)
                        #text.insert(tk.INSERT, "\n")
                        line += '\n'
                    else:
                        #text.insert(tk.INSERT, "Umbrella/Specialty: None\n ")
                        line += 'Umbrella/Speciakty: None\n'
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: spec')
            looking = findOnChartSwap(elem.NAME, pand, ratio)
            if len(looking) > 0:
                try:
                    #text.insert(tk.INSERT, 'ChartSwap: ')
                    line += 'ChartSwap: '
                    #text.insert(tk.INSERT, ''.join(str(looking)))
                    line += ''.join(str(looking))
                except Exception as e:
                    log.loggingWarning(e, 'searchHelp.py', 'confirmProvider: chartSwap')
            #text.insert(tk.INSERT,"\n")
            #text.insert(tk.INSERT,"\n")
            line += '\n\n'
    else:
        #findProvider(fileToRead, name, ratio, text)
        #text.insert(tk.INSERT,"Nothing was found. Search again or update Hospital Database...")
        #text.insert(tk.INSERT,"\n")
        line = ''
        line += 'Nothing was found. Search again or update Hospital Database...\n'
    writeToQueue1(line)


def readED(fileToRead, hosp, name, n, ratio, weighted = None):
    args = processFacility(fileToRead, hosp, name, ratio)
    providerDict, newDict, needlesProvider, ed = createNX(*args, n, weighted)
    return ed, providerDict

def printOutProvider(providerDict, text, displayArgs, ratio):
    line = ''
    #clearScreen(text)
    #text.insert(tk.INSERT, "Network was created. Please see Network Graph for details...\n\n")
    line += 'Network was created. Please see Network Graph for details...\n\n'
    print('printOUTProvider launched!')
    dispName, dispAddr, dispPhone, dispFax, dispSpec, dispInfo = displayArgs
    DB = connectToDB()
    lst = []
    name = None
    #clearScreen(text)
    for k,v in providerDict.items():
        print('LOOKING FOR: ', k.Name)
        lst = readFromNeedlesNameExact(DB,k.Name)
    if not lst:
        print('Nothing was wound with EXACT name;')
        line += 'Nothing was found'
    for elem in lst:
        #text.insert(tk.INSERT, elem.NAME+ "\n")
        line += str(elem.NAME) + '\n'
        if dispAddr:
            if elem.ADDRESS is not None:
                #text.insert(tk.INSERT, elem.ADDRESS+ "\n")
                line += str(elem.ADDRESS) + '\n'
            else:
                #text.insert(tk.INSERT, "Address: None\n")
                line += 'Address: None\n'
        if dispPhone:
            if elem.PHONE is not None:
                #text.insert(tk.INSERT, "General Phone: ")
                line += 'General Phone: '
                #text.insert(tk.INSERT, elem.PHONE)
                line += str(elem.PHONE)
                #text.insert(tk.INSERT, "\n")
                line += '\n'
            else:
                text.insert(tk.INSERT, "Feneral Phone: None\n")
                line += 'Feneral Phone: None\n'
        if dispFax:
             if elem.FAX is not None:
                 #text.insert(tk.INSERT, "General Fax: ")
                 line += 'General Fax: '
                 #text.insert(tk.INSERT, elem.FAX)
                 line += str(elem.FAX)
                 #text.insert(tk.INSERT, "\n")
                 line += '\n'
             else:
                 #text.insert(tk.INSERT, "General Fax: None\n")
                 line += 'General Fax: None\n'
        if dispInfo:
            try:
                if elem.LINK is not None:
                    #text.insert(tk.INSERT, "Link: ")
                    line += 'Link: '
                    #text.insert(tk.INSERT, elem.LINK)
                    line += str(elem.LINK)
                    #text.insert(tk.INSERT, "\n")
                    line += '\n'
                else:
                    #text.insert(tk.INSERT, "Link: None\n ")
                    line += 'Link: None\n'
            except Exception as e:
                log.loggingWarning(e, 'searchHelp.py', 'printOutProvider: link')
            try:
                if elem.WEIGHT is not None:
                    #text.insert(tk.INSERT, "Popularity: ")
                    line += 'Popularity: '
                    #text.insert(tk.INSERT, elem.WEIGHT)
                    line += str(elem.WEIGHT)
                    #text.insert(tk.INSERT, " clients served for the last 2 years\n")
                    line += ' clients served for the last 2 years\n'

            except Exception as e:
                log.loggingWarning(e, 'searchHelp.py', 'printOutProvidr: weight')
        #text.insert(tk.INSERT, "\n")
        pand = readChartSwap('Washington')
        looking = findOnChartSwap(elem.NAME, pand, ratio)
        if len(looking) > 0:
            try:
                #text.insert(tk.INSERT, 'ChartSwap: ')
                line += 'ChartSwap: '
                #text.insert(tk.INSERT, ''.join(str(looking)))
                line += ''.join(str(looking))
            except Exception as e:
                log.loggingWarning(e, 'searchHelp.py', 'printOutProvider: ChartSwap')
        #text.insert(tk.INSERT,"\n")
        #text.insert(tk.INSERT,"\n")
        line += '\n\n'
    #text.insert(tk.INSERT,"Nothing was found with your search term\n")
    writeToQueue1(line)


def findProvider(fileToRead, name, ratio, text):
    line = ''
    #clearScreen(text)
    #text.insert(tk.INSERT, 'Finding provider. Please wait...\n')
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
        clearScreen(text)
        #text.insert(tk.INSERT,"Nothing was found with your search term\n")
        #text.insert(tk.INSERT, 'Please try again...\n')
        line += 'Nothing was found with your search term\nPlease try again...\n'
        return
    else:
        clearScreen(text)
        try:
            possibleOptions = deepSearch(possibleOptions[0].Name, newList, 10, 0.2)
        except Exception as e:
            log.loggingWarning(e, 'searchHelp.py', 'findProvider: possibleOptions')
    #try:
        #text.delete(1.0,tk.END)
    #except Exception as e:
        #pass
    #text.insert(tk.INSERT, 'Is that what you are looking for...?\n\n')
    line += 'Is that what you are looking for...?\n\n'
    for i in possibleOptions:
        #text.insert(tk.INSERT, i+ "\n")
        line += str(i) + '\n'
    #text.insert(tk.INSERT,"\n")
    line += '\n'
    #text.insert(tk.INSERT, 'Please search again...\n')
    writeToQueue1(line)

def treatmentPlan(language, text, sLocation, radius, needlesOnly, avoidPhys, onlyChiro):
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
    #loc1 = geocoder.google(sLocation)
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
        #clearScreen(text)
        #text.insert(tk.INSERT,"Cant find this location. Please try again...\n")
        #text.insert(tk.INSERT,"Either enter full address or in this format: [city, state]...\n")
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
    #clearScreen(text)
    for key, value in txPlanDict.items():
        if avoidPhys:
            check = checkForSpecialties(key.NAME, places)
        '''if onlyChiro and not needlesOnly:
            allProviders = False
            try:
                if 'Chiropractic'.upper() not in key.NAME.upper():
                    continue
                if key.SPECIALTY is not 'Chiropractors' or key.SPECIALTY is not 'Chiropractic':
                    continue
            except Exception as e:
                print(e)'''
        if check:
            if languageDict[language] == 1:
                try:
                    if key.RU > 3:
                        line += printProviderTX(text, key, value, language)
                        #writeToQueue2(line)
                except Exception as e:
                    log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: RU')
                    line += printProviderTX(text, key, value, language)
            elif languageDict[language] == 2:
                try:
                    if key.ES > 3:
                        line += printProviderTX(text, key, value, language)
                        #writeToQueue2(line)
                        #print(key.NAME, 'is only', value,'miles away.', key.ADDRESS)
                except Exception as e:
                    log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: ES')
                    line += printProviderTX(text, key, value, language)
            elif languageDict[language] == 3:
                try:
                    if key.EN > 3:
                        line += printProviderTX(text, key, value, language)
                        #writeToQueue2(line)
                        #print(key.NAME, 'is only', value,'miles away.', key.ADDRESS)
                except Exception as e:
                    log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: EN')
                    line += printProviderTX(text, key, value, language)
            elif languageDict[language] == 4:
                try:
                    if key.RU >= 0 or key.ES >= 0 or key.EN >= 0:
                        line += printProviderTX(text, key, value, language)
                        #writeToQueue2(line)
                        #print(key.NAME, 'is only', value,'miles away.', key.ADDRESS)
                except Exception as e:
                    log.loggingInfo(e, 'searchHelp.py', 'treatmentPlan: ALL languages')
                    line += printProviderTX(text, key, value, language)
    writeToQueue2(line)
            
    return True

def printProviderTX(text, provider, value, language):
    line = ''
    #text.insert(tk.INSERT,provider.NAME)
    line += str(provider.NAME)
    #text.insert(tk.INSERT," is only ")
    line += ' is only '
    #text.insert(tk.INSERT,round(value, 2))
    line += str(round(value, 2))
    #text.insert(tk.INSERT," miles away from you\n")
    line += ' miles away from you\n'
    try:
        if provider.WEIGHT:
            #text.insert(tk.INSERT,"There were ")
            line += 'There were '
            #text.insert(tk.INSERT,provider.WEIGHT)
            line += str(provider.WEIGHT)
            #text.insert(tk.INSERT," ")
            line += ' '
            #text.insert(tk.INSERT, language)
            line += str(language)
            #text.insert(tk.INSERT," speeking clients in the past 2 years\n")
            line += ' speeking clients in the past 2 years\n'
    except Exception as e:
        log.loggingInfo(e, 'searchHelp.py', 'printProviderTX: Weight')
    #text.insert(tk.INSERT,"Full address: ")
    line += 'Full Address: '
    #text.insert(tk.INSERT,provider.ADDRESS)
    line += str(provider.ADDRESS)
    try:
        if provider.CITY:
            #text.insert(tk.INSERT,", ")
            line += ', '
            #text.insert(tk.INSERT,provider.CITY)
            line += str(provider.CITY)
    except Exception as e:
        log.loggingInfo(e, 'searchHelp.py', 'printProviderTX: City')
    #text.insert(tk.INSERT,"\n")
    line +='\n'
    #text.insert(tk.INSERT,"Phone: ")
    line += 'Phone: '
    #text.insert(tk.INSERT,provider.PHONE)
    line += str(provider.PHONE)
    try:
        if provider.SPECIALTY:
            #text.insert(tk.INSERT,"\n")
            line += '\n'
            #text.insert(tk.INSERT,"Specialty: ")
            line += 'Specialty: '
            #text.insert(tk.INSERT,provider.SPECIALTY)
            line += str(provider.SPECIALTY)
    except Exception as e:
        log.loggingInfo(e, 'searchHelp.py', 'printProviderTX: Specialty')
    #text.insert(tk.INSERT,"\n\n")
    line += '\n\n'
    return line

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
        #text.insert(tk.INSERT,"ID: ")
        line += 'ID: ' + str(elem.ID) + ' .Sent to: '+str(elem.Number)+'\nMessage: '+str(elem.Note)+'Sent on: '+str(elem.Date)+'\n'
        #text.insert(tk.INSERT,elem.ID)
        #line += str(elem.ID)
        #text.insert(tk.INSERT,". Sent to: ")
        #line += '. Sent to: '
        #text.insert(tk.INSERT, elem.Number)
        #text.insert(tk.INSERT,"\n")
        #text.insert(tk.INSERT, "Message: ")
        #text.insert(tk.INSERT, elem.Note)
        #text.insert(tk.INSERT, "Sent on: ")
        #text.insert(tk.INSERT, elem.Date)
        #text.insert(tk.INSERT, "\n")
        if elem.Attachment:
            #text.insert(tk.INSERT,"Attachment: ")
            #text.insert(tk.INSERT,elem.Attachment)
            #text.insert(tk.INSERT,"\n")
            line += 'Attachment: '+str(elem.Attachment)+'\n'
        #text.insert(tk.INSERT,"\n")
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
        
    
            
        
        
    
    

    
        
        
        
    
    
    
