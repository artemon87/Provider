from net import *
from find import *
from myDB import *
import tkinter as tk
from ChartSwapSearching import *
from HospitalsBS import *
from yelp import *
import time
import random


def clearScreen(text):
    try:
        text.delete(1.0,tk.END)
    except Exception as e:
        pass

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
    try:
        text.delete(1.0,tk.END)
    except Exception as e:
        pass
    clearScreen(text)
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
                text.insert(tk.INSERT, 'Found ')
                text.insert(tk.INSERT, len(result))
                text.insert(tk.INSERT, ' ')
                text.insert(tk.INSERT, s+' in ')
                text.insert(tk.INSERT, c+'\n')
                print('Found',len(result), s, 'in',c)
                #if len(result) == 0:
                    #text.insert(tk.INSERT, 'Please go to Yelp.com and verify that you are not a robot')
                    #print('Went sleeping ...')
                    #time.sleep(10)
                    #result = lookup(s, c)
                    #totalSleep += 1
                lst.append(result)
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
    return 0
    
def confirmSearchProvider(name, text, displayArgs):
    dispName, dispAddr, dispPhone, dispFax, dispSpec, dispInfo = displayArgs
    try:
        text.delete(1.0,tk.END)
    except Exception as e:
        pass
    lst = []
    DB = connectToDB()
    lst = readFromProviderName(DB, name)
    print('Lengthe of list returned from Provider Database', len(lst))
    pand = readChartSwap('Washington')
    if lst:
        for elem in lst:
            try:
                text.insert(tk.INSERT, elem.NAME+ "\n")
                if dispAddr:
                    if elem.ADDRESS is not None:
                        text.insert(tk.INSERT, elem.ADDRESS)
                        text.insert(tk.INSERT, "\n")
                        text.insert(tk.INSERT, elem.CITY)
                        text.insert(tk.INSERT, "\n")
                    else:
                        text.insert(tk.INSERT, "Address: None\n")
                if dispPhone:
                    if elem.PHONE is not None:
                        text.insert(tk.INSERT, "General Phone: ")
                        text.insert(tk.INSERT, elem.PHONE)
                        text.insert(tk.INSERT, "\n")
                    else:
                        text.insert(tk.INSERT, "General Phone: None\n")
                if dispFax:
                    if elem.FAX is not None:
                        text.insert(tk.INSERT, "General Fax: ")
                        text.insert(tk.INSERT, elem.FAX)
                        text.insert(tk.INSERT, "\n")
                    else:
                        text.insert(tk.INSERT, "Fax: None\n")
                if dispInfo:
                    if elem.LINK is not None:
                        text.insert(tk.INSERT, "Link: ")
                        text.insert(tk.INSERT, elem.LINK)
                        text.insert(tk.INSERT, "\n")
                    else:
                        text.insert(tk.INSERT, "Link: None\n")
                if dispSpec:
                    if elem.SPECIALTY is not None:
                        text.insert(tk.INSERT, "Specialty: ")
                        text.insert(tk.INSERT, elem.SPECIALTY)
                        text.insert(tk.INSERT, "\n")
                    else:
                        text.insert(tk.INSERT, "Specialty: None\n")
                looking = findOnChartSwap(elem.NAME, pand, 0.85)
                if len(looking) > 0:
                    text.insert(tk.INSERT, 'ChartSwap: ')
                    text.insert(tk.INSERT, ''.join(str(looking)))
                text.insert(tk.INSERT,"\n")
                text.insert(tk.INSERT,"\n")
            except Exception as e:
                print(e)
    else:
        text.insert(tk.INSERT,"Nothing was found. Search again or update Yelp Database...")
        text.insert(tk.INSERT,"\n")
    

def confirmProvider(fileToRead, name, text, displayArgs, ratio):
    dispName, dispAddr, dispPhone, dispFax, dispSpec, dispInfo = displayArgs
    DB = connectToDB()
    umbr = {'SWEDISH': False, 'MULTICARE': False, 'PROVIDENCE': False, 'FRANCISACAN': False,
            'UW MEDICINE': False, 'PEACEHEALTH': False, 'CONFLUENCE': False}
    facility = ''
    lst = []
    try:
        text.delete(1.0,tk.END)
    except Exception as e:
        pass
    #providerDict, *args = processAll(fileToRead)
    #newList = providerDictToList(providerDict)
    for k,v in umbr.items():
        result = searchFirst(k, name.upper())
        if result:
            umbr[k] = True
            facility = k
            lst = readFromHospitalUmbrella(DB, facility)
    if len(lst) == 0:
        print('Going to Hospital DB')
        lst = readFromHospitalName(DB, name.upper())
    pand = readChartSwap('Washington')
    if not lst:
        print('Going to Needles DB')
        lst = readFromNeedlesName(DB, name.upper())
        print('Going to Provider DB')
        lst = readFromProviderName(DB, name.upper())
    if lst:
        for elem in lst:
            text.insert(tk.INSERT, elem.NAME+ "\n")
            if dispAddr:
                if elem.ADDRESS is not None:
                    text.insert(tk.INSERT, elem.ADDRESS+ "\n")
                else:
                    text.insert(tk.INSERT, "Address: None")
                try:
                    text.insert(tk.INSERT, elem.CITY+ "\n")
                except Exception as e:
                    print(e)
            if dispPhone:
                if elem.PHONE is not None:
                    text.insert(tk.INSERT, "General Phone: ")
                    text.insert(tk.INSERT, elem.PHONE)
                    text.insert(tk.INSERT, "\n")
                else:
                    text.insert(tk.INSERT, "Feneral Phone: None\n")
            if dispFax:
                if elem.FAX is not None:
                    text.insert(tk.INSERT, "General Fax: ")
                    text.insert(tk.INSERT, elem.FAX)
                    text.insert(tk.INSERT, "\n")
                else:
                    text.insert(tk.INSERT, "General Fax: None\n")
                try:
                    if elem.RECORDS is not None:
                        text.insert(tk.INSERT, "Records Fax: ")
                        text.insert(tk.INSERT, elem.RECORDS)
                        text.insert(tk.INSERT, "\n")
                    else:
                        text.insert(tk.INSERT, "Records Fax: None\n")
                    if elem.BILLING is not None:
                        text.insert(tk.INSERT, "Billing Fax: ")
                        text.insert(tk.INSERT, elem.BILLING)
                        text.insert(tk.INSERT, "\n")
                    else:
                        text.insert(tk.INSERT, "Billing Fax: None\n")
                except Exception as e:
                    print(e)
            if dispInfo:
                try:
                    if elem.LINK is not None:
                        text.insert(tk.INSERT, "Link: ")
                        text.insert(tk.INSERT, elem.LINK)
                        text.insert(tk.INSERT, "\n")
                    else:
                        text.insert(tk.INSERT, "Link: None\n ")
                except Exception as e:
                    print(e)
            if dispSpec:
                try:
                    if elem.UMBRELLA is not None:
                        text.insert(tk.INSERT, "Umbrella/Specialty: ")
                        text.insert(tk.INSERT, elem.UMBRELLA)
                        text.insert(tk.INSERT, "\n")
                    else:
                        text.insert(tk.INSERT, "Umbrella/Specialty: None\n ")
                except Exception as e:
                    print(e)
                try:
                    if elem.SPECIALTY is not None:
                        text.insert(tk.INSERT, "Umbrella/Specialty: ")
                        text.insert(tk.INSERT, elem.SPECIALTY)
                        text.insert(tk.INSERT, "\n")
                    else:
                        text.insert(tk.INSERT, "Umbrella/Specialty: None\n ")
                except Exception as e:
                    print(e)
            looking = findOnChartSwap(elem.NAME, pand, ratio)
            if len(looking) > 0:
                try:
                    text.insert(tk.INSERT, 'ChartSwap: ')
                    text.insert(tk.INSERT, ''.join(str(looking)))
                except Exception as e:
                    print(e)
            text.insert(tk.INSERT,"\n")
            text.insert(tk.INSERT,"\n")
    else:
        findProvider(fileToRead, name, ratio, text)
        text.insert(tk.INSERT,"Nothing was found. Search again...")
        text.insert(tk.INSERT,"\n")
        
def readED(fileToRead, hosp, name, n, ratio):
    args = processFacility(fileToRead, hosp, name, ratio)
    providerDict, newDict, needlesProvider, ed = createNX(*args, n)
    return ed, providerDict

def printOutProvider(providerDict, text, displayArgs):
    print('printOUTProvider launched!')
    dispName, dispAddr, dispPhone, dispFax, dispSpec, dispInfo = displayArgs
    DB = connectToDB()
    try:
        text.delete(1.0,tk.END)
    except Exception as e:
        pass
    lst = []
    name = None
    clearScreen(text)
    for k,v in providerDict.items():
        print('LOOKING FOR: ', k.Name)
        lst = readFromNeedlesNameExact(DB,k.Name)
    if not lst:
        print('Nothing was wound with EXACT name;')
    for elem in lst:
        text.insert(tk.INSERT, elem.NAME+ "\n")
        if dispAddr:
            if elem.ADDRESS is not None:
                text.insert(tk.INSERT, elem.ADDRESS+ "\n")
            else:
                text.insert(tk.INSERT, "Address: None")
        if dispPhone:
            if elem.PHONE is not None:
                text.insert(tk.INSERT, "General Phone: ")
                text.insert(tk.INSERT, elem.PHONE)
                text.insert(tk.INSERT, "\n")
            else:
                text.insert(tk.INSERT, "Feneral Phone: None\n")
        if dispFax:
             if elem.FAX is not None:
                 text.insert(tk.INSERT, "General Fax: ")
                 text.insert(tk.INSERT, elem.FAX)
                 text.insert(tk.INSERT, "\n")
             else:
                 text.insert(tk.INSERT, "General Fax: None\n")
        if dispInfo:
            try:
                if elem.LINK is not None:
                    text.insert(tk.INSERT, "Link: ")
                    text.insert(tk.INSERT, elem.LINK)
                    text.insert(tk.INSERT, "\n")
                else:
                    text.insert(tk.INSERT, "Link: None\n ")
            except Exception as e:
                print(e)
            try:
                if elem.WEIGHT is not None:
                    text.insert(tk.INSERT, "Popularity: ")
                    text.insert(tk.INSERT, elem.LINK)
                    text.insert(tk.INSERT, " clients served for the last 2 years\n")

            except Exception as e:
                print(e)
        text.insert(tk.INSERT, "\n")
    #text.insert(tk.INSERT,"Nothing was found with your search term\n")


def findProvider(fileToRead, name, ratio, text):
    providerDict, *rest = processAll(fileToRead)
    newList = providerDictToList(providerDict)
    possibleOptions = deepSearch(name, newList, 10, ratio)
    if len(possibleOptions) < 10:
        possibleOptions = deepSearch(name, newList, 10, 0.2)
    if len(possibleOptions) < 1:
        possibleOptions = searchFirstDict(name, providerDict)
    if len(possibleOptions) == 0:
        clearScreen(text)
        text.insert(tk.INSERT,"Nothing was found with your search term\n")
        text.insert(tk.INSERT, 'Please try again...\n')
        return
    else:
        clearScreen(text)
        try:
            possibleOptions = deepSearch(possibleOptions[0].Name, newList, 10, 0.2)
        except Exception as e:
            pass
    #try:
        #text.delete(1.0,tk.END)
    #except Exception as e:
        #pass
    text.insert(tk.INSERT, 'Is that what you are looking for...?\n\n')
    for i in possibleOptions:
        text.insert(tk.INSERT, i+ "\n")
    text.insert(tk.INSERT,"\n")
    text.insert(tk.INSERT, 'Please search again...\n')
    return possibleOptions
