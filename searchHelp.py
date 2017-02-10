from net import *
from find import *
from myDB import *
import tkinter as tk
from ChartSwapSearching import *

def connectToDB():
    return setupDB()


def confirmProvider(fileToRead, name, n, text):
    DB = connectToDB()
    umbr = {'SWEDISH': False, 'MULTICARE': False, 'PROVIDENCE': False, 'FRANCISACAN': False,
            'UW MEDICINE': False, 'PEACEHEALTH': False, 'CONFLUENCE': False}
    facility = ''
    lst = []
    try:
        text.delete(1.0,tk.END)
    except Exception as e:
        pass
    providerDict, *rest = processAll(fileToRead)
    newList = providerDictToList(providerDict)
    for k,v in umbr.items():
        result = searchFirst(k, name.upper())
        if result:
            umbr[k] = True
            facility = k
            lst = readFromHospitalUmbrella(DB, facility)
    if len(lst) == 0:
        lst = readFromHospitalName(DB, name.upper())
    pand = readChartSwap('Washington')
    for elem in lst:
        text.insert(tk.INSERT, elem[0]+ "\n")
        text.insert(tk.INSERT, "General Phone: "+elem[3]+ "\n")
        text.insert(tk.INSERT, "Medical Records Fax: "+elem[3]+ "\n")
        text.insert(tk.INSERT, "Billing Records Fax: "+elem[3]+ "\n")
        text.insert(tk.INSERT, "Link: "+elem[4]+"\n", ('link', elem[4]))
        looking = findOnChartSwap(elem[0], pand, 0.80)
        if len(looking) > 0:
            text.insert(tk.INSERT, 'ChartSwap: ')
            text.insert(tk.INSERT, ''.join(str(looking)))
        text.insert(tk.INSERT,"\n")
        text.insert(tk.INSERT,"\n")
        


def findProvider(fileToRead, name, n, text):
    providerDict, *rest = processAll(fileToRead)
    newList = providerDictToList(providerDict)
    possibleOptions = deepSearch(name, newList, 10, 0.5)
    if len(possibleOptions) < 10:
        possibleOptions = deepSearch(name, newList, 10, 0.2)
    return possibleOptions
