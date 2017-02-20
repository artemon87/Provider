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
        '''print('Going to Provider DB')
        lst = readFromProviderName(DB, name.upper())'''
    if lst:
        clearScreen(text)
        text.insert(tk.INSERT, "Is that what you are looking for?\n\n")
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

def treatmentPlan(language, text, location, radius, needlesOnly, avoidPhys, onlyChiro):
    radius = float(radius)
    #gmaps = googlemaps.Client(key='AIzaSyCsATCl3uaPZGRcamcl11Nd1NnaLD8SIew')
    #   AIzaSyCsATCl3uaPZGRcamcl11Nd1NnaLD8SIew
    print(radius)
    lst = []
    lst2 = []
    lst3 = []
    check = True
    allProviders = True
    places = ['Phys', 'Physician', 'Physicians', 'Rad', 'Radiology', 'ER', 'Emergency', 'Imaging', 'Ambulance', 'Fire']
    languageDict = {'Russian': 1, 'Spanish': 2, 'English' : 3, 'Unspecified': 4}
    txPlanDict = {}
    if ', WA' not in location.upper() or ',WA' not in location.upper() or ' WA' not in location.upper():
        location = location + ' WA'
        print(location)
    DB = connectToDB()
    if not needlesOnly:
        lst2 = readFromHospital(DB)
        lst3 = readFromProvider(DB)
    lst = readFromNeedlesAll(DB)
    loc1 = geocoder.google(location)
    if loc1 is None:
        text.insert(tk.INSERT,"Cant find this location. Please try again...\n")
        text.insert(tk.INSERT,"Either enter full address or in this format: [city, state]...\n")
        return
    loc2 = None
    distance = float
    for elem in lst:
        try:
            if elem.GEO is not 'NONE' or elem.GEO is not None:
                loc2 = elem.GEO
                distance = great_circle(loc1.latlng, loc2).miles
                if distance < radius:
                    txPlanDict[elem] = distance
            else:
                pass
        except Exception as e:
            print(e)
    if lst2:
        for elem in lst2:
            try:
                if elem.GEO is not 'NONE' or elem.GEO is not None:
                    loc2 = elem.GEO
                    distance = great_circle(loc1.latlng, loc2).miles
                    if distance < radius:
                        txPlanDict[elem] = distance
                else:
                    pass
            except Exception as e:
                print(e)
    if lst3:
        for elem in lst3:
            try:
                if elem.GEO is not 'NONE' or elem.GEO is not None:
                    loc2 = elem.GEO
                    distance = great_circle(loc1.latlng, loc2).miles
                    if distance < radius:
                        txPlanDict[elem] = distance
                else:
                    pass
            except Exception as e:
                print(e)
    clearScreen(text)
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
                        printProviderTX(text, key, value, language)
                        #print(key.NAME, 'is only', value,'miles away.', key.ADDRESS)
                except Exception as e:
                    print(e)
                    printProviderTX(text, key, value, language)
            elif languageDict[language] == 2:
                try:
                    if key.ES > 3:
                        printProviderTX(text, key, value, language)
                        #print(key.NAME, 'is only', value,'miles away.', key.ADDRESS)
                except Exception as e:
                    print(e)
                    printProviderTX(text, key, value, language)
            elif languageDict[language] == 3:
                try:
                    if key.EN > 3:
                        printProviderTX(text, key, value, language)
                        #print(key.NAME, 'is only', value,'miles away.', key.ADDRESS)
                except Exception as e:
                    print(e)
                    printProviderTX(text, key, value, language)
            elif languageDict[language] == 3:
                try:
                    if key.RU >= 0 or key.ES >= 0 or key.EN >= 0:
                        printProviderTX(text, key, value, language)
                        #print(key.NAME, 'is only', value,'miles away.', key.ADDRESS)
                except Exception as e:
                    print(e)
                    printProviderTX(text, key, value, language)
            
            
    return True

def printProviderTX(text, provider, value, language):
    text.insert(tk.INSERT,provider.NAME)
    text.insert(tk.INSERT," is only ")
    text.insert(tk.INSERT,round(value, 2))
    text.insert(tk.INSERT," miles away from you\n")
    try:
        if provider.WEIGHT:
            text.insert(tk.INSERT,"There were ")
            text.insert(tk.INSERT,provider.WEIGHT)
            text.insert(tk.INSERT," ")
            text.insert(tk.INSERT, language)
            text.insert(tk.INSERT," speeking clients in the past 2 years\n")
    except Exception as e:
        print(e)
    text.insert(tk.INSERT,"Full address: ")
    text.insert(tk.INSERT,provider.ADDRESS)
    try:
        if provider.CITY:
            text.insert(tk.INSERT,", ")
            text.insert(tk.INSERT,provider.CITY)
    except Exception as e:
        print(e)
    text.insert(tk.INSERT,"\n")
    text.insert(tk.INSERT,"Phone: ")
    text.insert(tk.INSERT,provider.PHONE)
    try:
        if provider.SPECIALTY:
            text.insert(tk.INSERT,"\n")
            text.insert(tk.INSERT,"Specialty: ")
            text.insert(tk.INSERT,provider.SPECIALTY)
    except Exception as e:
        print(e)
    text.insert(tk.INSERT,"\n\n")

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
                print(e)
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
                    print(e)
                inst = P(i.NAME, i.PHONE, geo)
                lstWithGeo.append(inst)
                if n >= 2000:
                    break
    updateProviderGEO(DB, lstWithGeo)

def sendMessageToClient(msg, number, filePath, attachment, popUp):
    newMessage = textMessage()
    newMessage.fillInList(number)
    result = newMessage.sendText(msg, filePath, attachment)
    if result:
        popUp.showinfo('Confirmation', 'Message sent')
    else:
        popUp.showinfo('Confirmation', 'Message failed')
    
    

    
        
        
        
    
    
    
