import sys
import os
from cx_Freeze import setup, Executable


#C:\Users\user\AppData\Local\Programs\Python\Python35-32
os.environ['TCL_LIBRARY'] = "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python35-32\\tcl\\tk8.6"
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["tkinter", "networkx", "pandas", "geocoder", "numpy",
                                  "email", "geopy", "googlemaps", "smtplib", "os"], "include_files": ["C:\\Users\\user\\Documents\\S\\Prov\\Provider\\app.log", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\ChartSwap.xlsx",
                     "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\ChartSwapSearching.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\find.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\HospitalFile.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\HospitalsBS.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\HospitalsInTheUS.xlsx",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\hospitalUpdate.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\log.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\myDB.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\needlesStat.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\net.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\netRace.xlsx", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\netFax.xlsx",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\part1.xlsx", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\part2.xlsx",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\searchHelp2.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\test.db",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\textMessage.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\ToolTip.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\yelp.py",
                                                                                     'C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python35-32\\DLLs\\tk86t.dll',
                                                                                     'C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python35-32\\DLLs\\tcl86t.dll',
                                                                                     'C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python35-32\\DLLs\\sqlite3.dll'],
                     "excludes": []}
'''"include_files" :
                     ["C:\\Users\\user\\Documents\\S\\Prov\\Provider\\app.log", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\ChartSwap.xlsx",
                     "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\ChartSwapSearching.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\find.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\HospitalFile.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\HospitalsBS.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\HospitalsInTheUS.xlsx",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\hospitalUpdate.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\log.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\myDB.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\needlesStat.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\net.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\netRace.xlsx", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\netFax.xlsx",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\part1.xlsx", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\part2.xlsx",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\searchHelp2.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\test.db",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\textMessage.py", "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\ToolTip.py",
                      "C:\\Users\\user\\Documents\\S\\Prov\\Provider\\yelp.py"],'''
#executables = [Executable("gui.py", base=base)]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "ProviderNetwork",
        version = "1.0",
        description = "Multifunctional application for Rubinstein Law Office",
        options = {"build_exe": build_exe_options},
        executables = [Executable("gui.py", base=base)])
