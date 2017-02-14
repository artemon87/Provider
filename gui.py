import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox
from net import *
from find import *
from searchHelp import *
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
#import ToolTip as tt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
from os import path
from tkinter import filedialog as fd
import pytz
from tkinter import messagebox as mBox

from datetime import datetime



class ProviderGUI:
    def __init__(self, root):
        self.win = root
        self.createWidgets()

    def createWidgets(self):
        self.tabControl = ttk.Notebook(self.win)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Main')
        self.tabControl.add(self.tab2, text='Network Graph')
        self.tabControl.pack(expand=1, fill="both")
        self.menuBar = Menu(self.win)
        self.win.config(menu=self.menuBar)
        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="About", command = self._msgBox)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        self.monty1 = ttk.LabelFrame(self.tab1, text=' Monty Python ')
        self.monty = ttk.LabelFrame(self.tab1, text=' Monty1 Python ')
        self.mngFilesFrame = ttk.LabelFrame(self.tab1, text=' Manage Files: ')
        self.infoZone = ttk.LabelFrame(self.tab1, text = ' Info ')
        self.browseButton = ttk.Button(self.mngFilesFrame, text="Browse ...",command=self.getFileName)
        self.fName = None #name of a file to browse
        self.fDir = None #dir of a file
        self.file = tk.StringVar()
        self.entryLen = 60
        self.fileEntry = ttk.Entry(self.mngFilesFrame, width=60,textvariable=self.file)
        self.fileEntry.grid(column=1, row=0, sticky=tk.W)
        self.monty2 = ttk.LabelFrame(self.tab2, text=' Provider Network')
        self.time = ttk.Label(self.infoZone, text='Date and Time of Launch')
        self.timeZone = tk.StringVar()
        self.timeZoneLabel = ttk.Label(self.infoZone, textvariable=self.timeZone)
        self.aLabel = ttk.Label(self.monty1, text="Search Box") #label
        self.action = ttk.Button(self.monty1, text="Run", command=self.clickMe) #button
        self.updateDB = ttk.Button(self.infoZone, text='Update Database', comman=self.updateDatabase)
        self.name = tk.StringVar() #search name
        self.nameEntered = ttk.Entry(self.monty1, width=40, textvariable=self.name) #name entered
        self.aLabel2 = ttk.Label(self.monty1, text="Choose an action:").grid(column=1, row=0) #drop down box
        self.act = tk.StringVar()
        self.numberChosen = ttk.Combobox(self.monty1, width=12, textvariable=self.act)
        self.labelCheckbox = ttk.Label(self.monty, text="Information to Display", font=("Helvetica", 13)).grid(column=1, row=0, padx = 10, pady = 10)
        self.labelCombo = ttk.Label(self.monty, text="Search Ratio", font=("Helvetica", 13)).grid(column=1, row=6, padx = 10, pady = 10)
        #self.labelAddlInfo= ttk.Label(self.monty, text="Search Ratio", font=("Helvetica", 13)).grid(column=1, row=8, padx = 10, pady = 10)
        self.chVar1 = tk.IntVar() #checkbox 1
        self.chVar2 = tk.IntVar() #checkbox 2
        self.chVar3 = tk.IntVar() #checkbox 3
        self.chVar4 = tk.IntVar() #checkbox 4
        self.chVar5 = tk.IntVar() #checkbox 5
        self.chVar6 = tk.IntVar() #checkbox 6
        self.chAddl1 = tk.IntVar() #checkbox7
        self.chAddl2 = tk.IntVar() #checkbox8
        self.chAddl3 = tk.IntVar() #checkbox9
        self.radVar = tk.IntVar() #radio button
        self.scr = scrolledtext.ScrolledText(self.monty, width=80, height=14, wrap=tk.WORD)
        self.figure = Figure(figsize=(7,5), dpi=90)
        self.aPlot = self.figure.add_subplot(111)
        self.canvas = None
        self.toolbar = None

        
    def labels(self):
        self.aLabel.grid(column=0, row=0)
        self.time.grid(column=0, row=0)
        self.timeZoneLabel.grid(column=0,row=1)
        self.infoZone.grid(column = 0, row = 3 , sticky = 'WE', padx = 10, pady = 5)
        self.monty1.grid(column=0, row=0, padx=8, pady=4)
        self.monty2.grid(column=0, row=0, padx=8, pady=4)
        self.browseButton.grid(column=0, row=0, sticky=tk.W)
        self.monty.grid(column=0, row=1, padx=8, pady=4)
        self.mngFilesFrame.grid(column=0, row=2, sticky='WE', padx=10, pady=5)

    def bottons(self):
        self.action.grid(column=2, row=1)
        self.updateDB.grid(column=3, row=1)

    def searchBar(self):
        self.nameEntered.grid(column=0, row=1, rowspan=3)
        self.nameEntered.focus()
        self.nameEntered.bind('<Return>', self.clickMe)

    def dropDown(self):
        self.numberChosen['values'] = ('Find Provider', 'Build a network')
        self.numberChosen.grid(column=1, row=1, rowspan=2)
        self.numberChosen.current(0)

    def checkBox(self):
        self.check1 = tk.Checkbutton(self.monty, text="Display Name", variable=self.chVar1, state='disabled')
        self.check1.grid(column=0, row=4, sticky=tk.W)
        self.check1.select()
        self.check2 = tk.Checkbutton(self.monty, text="Display Address", variable=self.chVar2)
        self.check2.grid(column=1, row=4, sticky=tk.W)
        self.check2.select()
        self.check3 = tk.Checkbutton(self.monty, text="Display Phone", variable=self.chVar3)
        self.check3.select()
        self.check3.grid(column=2, row=4, sticky=tk.W)
        self.check4 = tk.Checkbutton(self.monty, text="Display Fax", variable=self.chVar4)
        self.check4.grid(column=0, row=5, sticky=tk.W)
        self.check4.deselect()
        self.check5 = tk.Checkbutton(self.monty, text="Display Specialty", variable=self.chVar5)
        self.check5.grid(column=1, row=5, sticky=tk.W)
        self.check5.deselect()
        self.check6 = tk.Checkbutton(self.monty, text="Display Add'l info", variable=self.chVar6)
        self.check6.deselect()
        self.check6.grid(column=2, row=5, sticky=tk.W)
        self.check7 = tk.Checkbutton(self.infoZone, text="Update Needles", variable=self.chAddl1)
        self.check7.deselect()
        self.check7.grid(column=4, row=1, sticky=tk.W)
        self.check8 = tk.Checkbutton(self.infoZone, text="Update Yelp", variable=self.chAddl2)
        self.check8.deselect()
        self.check8.grid(column=5, row=1, sticky=tk.W)
        self.check9 = tk.Checkbutton(self.infoZone, text="Update Hospitals", variable=self.chAddl3)
        self.check9.deselect()
        self.check9.grid(column=6, row=1, sticky=tk.W)

    def radioButton(self):
        self.rad1 = tk.Radiobutton(self.monty, text='Somehow Accurate', variable=self.radVar, value=1, command=self.radCall)
        self.rad1.grid(column=0, row=7, sticky=tk.W)
        self.rad4 = tk.Radiobutton(self.monty, text='Very Accurate', variable=self.radVar, value=2, command=self.radCall)
        self.rad4.grid(column=1, row=7, sticky=tk.W)
        self.rad5 = tk.Radiobutton(self.monty, text='Most Acurate', variable=self.radVar, value=3, command=self.radCall)
        self.rad5.grid(column=2, row=7, sticky=tk.W)
        self.rad5.select()

    def scrollableText(self):
        self.scr.grid(column=0, columnspan=3)

    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    def clearCanvas(self):
        try:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
            self.aPlot.clear()
            self.aPlot.set_xticks([])
            self.aPlot.set_yticks([])
        except Exception as e:
            pass

    def updateDatabase(self):
        mBox.showinfo('Database Information', 'Stay in touch.\nUpdating takes some time (5-15 minutes)')
        upNeedles = self.chAddl1.get()
        upYelp = self.chAddl2.get()
        upHospital = self.chAddl3.get()
        print('Needles: ',upNeedles, 'Yelp:', upYelp,'Hospital:', upHospital)
        self.updateDB.configure(text='Updating...')
        result = fillinDB(upNeedles,upYelp, upHospital, self.scr)
        if result == 0:
            mBox.showinfo('Database Information', 'Database successfully finished updating.\n')
            self.updateDB.configure(text='Update Database')
        else:
            mBox.showinfo('Database Information', 'Please launch Yelp.com on your webbrowser.\nAnd confirm that you are not a robot')
        
    def clickMe(self, event=None):
        ratio = self.searchAccuracy()
        displayArgs = self.getCheckbox()
        if self.act.get() == 'Build a network':
            self.clearCanvas()
            fileToRead = ''
            if self.fName == None:
                fileToRead ='netRace.xlsx'
            else:
                fileToRead = self.fName
            ed, providerDict = readED(fileToRead, None, self.name.get(), 7, ratio)
            if len(ed) == 0:
                try:
                    self.scr.delete(1.0,tk.END)
                except Exception as e:
                    pass
                confirmProvider(fileToRead, self.name.get(), self.scr, displayArgs, ratio)
                #possibleOptions = findProvider(fileToRead, self.name.get(), ratio, self.scr)
            else:
                try:
                    self.scr.delete(1.0,tk.END)
                except Exception as e:
                    pass
                #confirmProvider(fileToRead, self.name.get(), self.scr, displayArgs, ratio)
                printOutProvider(providerDict, self.scr, displayArgs)
                pos=nx.spring_layout(ed)
                nx.draw_networkx(ed, pos, arrows = True, with_labels = True, ax = self.aPlot, font_size = 10)
                self.canvas = FigureCanvasTkAgg(self.figure, master=self.monty2)
                self.canvas.show()
                self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.monty2)
                self.toolbar.update()
                self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
        elif self.act.get() == 'Find Provider':
            confirmSearchProvider(self.name.get(), self.scr, displayArgs)

    def getCheckbox(self):
        return self.chVar1.get(), self.chVar2.get(), self.chVar3.get(), self.chVar4.get(), self.chVar5.get(), self.chVar6.get()
    
    def searchAccuracy(self):
        accuracy = self.radVar.get()
        ratio = float
        if accuracy == 1:
            ratio = 0.50
        elif accuracy == 2:
            ratio = 0.75
        elif accuracy == 3:
            ratio = 0.90
        return ratio
            
	
    def radCall(self):
        r = self.radVar.get()
        if r == 1:
                pass
        if r == 2:
                pass

    def _msgBox(self):
        mBox.showinfo('Provider Network info box','Created by Artem Kovtunenko\n Version 1.0')

    def getDateTime(self):
        fmtStrZone = '''%Y-%m-%d %H:%M'''
        self.timeZone.set(datetime.now().strftime(fmtStrZone))
        
    def getFileName(self):
        self.fDir = path.dirname(__file__)
        self.fName = fd.askopenfilename(parent=self.win, initialdir=self.fDir)
        self.fileEntry.delete(0, tk.END)
        self.fileEntry.insert(0, self.fName)




w = tk.Tk()
w.title("Python GUI")
gui = ProviderGUI(w)
gui.labels()
gui.bottons()
gui.searchBar()
gui.dropDown()
gui.checkBox()
gui.radioButton()
gui.scrollableText()
gui.getDateTime()
try:
    w.mainloop()
except Exception as e:
    print(e)
