from net import *
from find import *
from myDB import *
import tkinter as tk
from ChartSwapSearching import *
from HospitalsBS import *
from yelp import *

SETUP = False 

def createTablesInDB():
    global SETUP
    if not SETUP:
        DB = connectToDB()
        createHospitalDB(DB)
        createNeedlesDB(DB)
        createProviderDB(DB)
    SETUP = True

def connectToDB():
    return setupDB()

def createNeedlesList():
    needlesFile = 'netRace.xlsx'
    tupple = processAll(needlesFile)
    providerDict, dictWeighted, needlesProvider, ed = createNX(*tupple, 5)
    needlesList = createDicForDB(dictWeighted, needlesProvider)
    return needlesList

def fillinDB(upNeedles,upYelp, upHospital):
    createTablesInDB()
    DB = connectToDB()
    lst = []
    city = ['Federal Way,WA', 'Tacoma, WA', 'Seattle, WA', 'Bellevue, WA',
            'Everett, WA', 'Renton, WA', 'Lake City, WA', 'Sammamish, WA']
    spec = ['Chiropractic', 'Urgent Care', 'Orthopedic', 'Physical Therapy',
            'Pediatrics', 'Physicians', 'Massage Therapy', 'Diagnostic Imaging',
            'Medical Clinic', 'Family Practice']
    if upYelp:
        for c in city:
            for s in spec:
                result = lookup(s, c)
                print('Found',len(result), s, 'in',c)
                lst.append(result)
        for elem in lst:
            addProvider(elem, DB)
    if len(lst) == 0:
        return -1
    if upHospital:
        hosp = findAllHospitals()
        addHospital(hosp, DB)
    if upNeedles:
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
    else:
        pass
    

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
        lst = readFromHospitalName(DB, name.upper())
    if len(lst) == 0:
        lst = readFromHospitalName(DB, name.upper())
    pand = readChartSwap('Washington')
    for elem in lst:
        text.insert(tk.INSERT, elem.NAME+ "\n")
        if dispAddr:
            text.insert(tk.INSERT, elem.ADDRESS+ "\n")
            text.insert(tk.INSERT, elem.CITY+ "\n")
        if dispPhone:
            text.insert(tk.INSERT, "General Phone: "+elem.PHONE+ "\n")
        if dispFax:
            text.insert(tk.INSERT, "General Fax: "+elem.FAX+ "\n")
            text.insert(tk.INSERT, "Medical Records Fax: "+elem.RECORDS+ "\n")
            text.insert(tk.INSERT, "Billing Records Fax: "+elem.BILLING+ "\n")
        if dispInfo:
            text.insert(tk.INSERT, "Link: "+elem.LINK+"\n", ('link', elem.LINK))
        if dispSpec:
            text.insert(tk.INSERT, "Umbrella/Specialty: "+elem.UMBRELLA+"\n")
        looking = findOnChartSwap(elem.NAME, pand, ratio)
        if len(looking) > 0:
            text.insert(tk.INSERT, 'ChartSwap: ')
            text.insert(tk.INSERT, ''.join(str(looking)))
        text.insert(tk.INSERT,"\n")
        text.insert(tk.INSERT,"\n")
        
def readED(fileToRead, hosp, name, n, ratio):
    args = processFacility(fileToRead, hosp, name, ratio)
    providerDict, newDict, needlesProvider, ed = createNX(*args, n)
    return ed

def findProvider(fileToRead, name, n, text):
    providerDict, *rest = processAll(fileToRead)
    newList = providerDictToList(providerDict)
    possibleOptions = deepSearch(name, newList, 10, 0.5)
    if len(possibleOptions) < 10:
        possibleOptions = deepSearch(name, newList, 10, 0.2)
    try:
        text.delete(1.0,tk.END)
    except Exception as e:
        pass
    text.insert(tk.INSERT, 'Is that what you are looking for...?\n\n')
    for i in possibleOptions:
        text.insert(tk.INSERT, i+ "\n")
    text.insert(tk.INSERT,"\n")
    text.insert(tk.INSERT, 'Please search again...\n')
    return possibleOptions
