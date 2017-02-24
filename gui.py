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
from threading import Thread
from datetime import datetime
import time



class ProviderGUI:
    def __init__(self, root):
        self.win = root
        self.createWidgets()

    def createWidgets(self):
        self.tabControl = ttk.Notebook(self.win)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Main')
        self.tabControl.add(self.tab2, text='Network Graph')
        self.tabControl.add(self.tab3, text='Client Referrals')
        self.tabControl.add(self.tab4, text='Text Message')
        self.tabControl.pack(expand=1, fill="both")
        self.menuBar = Menu(self.win)
        self.win.config(menu=self.menuBar)
        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="About", command = self._msgBox)
        self.helpMenu.add_command(label="Exit", command = self._quit)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        self.monty1 = ttk.LabelFrame(self.tab1, text=' Monty Python ')
        self.monty = ttk.LabelFrame(self.tab1, text=' Monty1 Python ')
        self.mngFilesFrame = ttk.LabelFrame(self.tab1, text=' Manage Files: ')
        self.phoneNumber = ttk.LabelFrame(self.tab4, text=' Enter phone number here: ')
        self.messageTextEntry = ttk.LabelFrame(self.tab4, text=' Message')
        self.messageSentEntry = ttk.LabelFrame(self.tab4, text=' Sent Mesages')
        self.fileAttachmentEntry = ttk.LabelFrame(self.tab4, text=' File')
        self.infoZone = ttk.LabelFrame(self.tab1, text = ' Info ')
        #self.textMessagePhone = ttk.LabelFrame(self.tab4, text = ' Phone Number here ')
        self.browseButton = ttk.Button(self.mngFilesFrame, text="Browse ...",command=self.getFileName)
        self.browseButton2 = ttk.Button(self.fileAttachmentEntry, text="Browse ...",command=self.getFileNameForAttachment)
        self.fName = None #name of a file to browse
        self.fDir = None #dir of a file
        self.fName2 = None #name of a file to attach to txt message
        self.fDir2 = None #dir of an attachment
        self.file = tk.StringVar()
        self.file2 = tk.StringVar()
        self.entryLen = 60
        self.fileEntry = ttk.Entry(self.mngFilesFrame, width=60,textvariable=self.file)
        self.fileEntry.grid(column=1, row=0, padx = 40, pady = 5)
        self.fileEntry2 = ttk.Entry(self.fileAttachmentEntry, width=40,textvariable=self.file2)
        self.fileEntry2.grid(column=1, row=0, padx = 40, pady = 5)
        self.monty2 = ttk.LabelFrame(self.tab2, text=' Provider Network')
        self.client = ttk.LabelFrame(self.tab3, text=' Seach Box ')
        self.client2 = ttk.LabelFrame(self.tab3, text=' Filter')
        self.client3 = ttk.LabelFrame(self.tab3, text=' Plan ')
        self.time = ttk.Label(self.infoZone, text='Date and Time of Launch')
        self.timeZone = tk.StringVar()
        self.timeZoneLabel = ttk.Label(self.infoZone, textvariable=self.timeZone)
        self.aLabel = ttk.Label(self.monty1, text="Search Box") #label
        self.action = ttk.Button(self.monty1, text="Run", command=self.clickMe) #button
        self.updateDB = ttk.Button(self.infoZone, text='Update Database', comman=self.runUpdateDatabase)
        self.name = tk.StringVar() #search name
        self.name2 = tk.StringVar() #search location
        self.phone = tk.StringVar() #phonenumber
        self.nameEntered = ttk.Entry(self.monty1, width=40, textvariable=self.name) #name entered
        self.aLabel2 = ttk.Label(self.monty1, text="Choose an action:").grid(column=1, row=0) #drop down box
        self.netSizeLabel = ttk.Label(self.monty1, text="Network size:").grid(column=1, row=1) #drop down box
        self.clientLable1 = ttk.Label(self.client, text="Enter client's location:").grid(column=0, row=0) #drop down box
        self.clientLable2 = ttk.Label(self.client, text="Language").grid(column=1, row=0) #drop down box
        self.clientLable3 = ttk.Label(self.client, text="Travel Distance").grid(column=2, row=0) #drop down box
        #self.clientLable4 = ttk.Label(self.client, text="Check this box if you looking for Needles providers only").grid(column=0, row=2) #drop down box
        self.clientLocation = ttk.Entry(self.client, width=35, textvariable=self.name2) #name entered
        self.phoneEntered = ttk.Entry(self.phoneNumber, width=40, textvariable=self.phone) #name entered
        self.sentMessageButton = ttk.Button(self.phoneNumber, text="Send", command=self.sendText) 
        self.act = tk.StringVar()
        self.act2 = tk.StringVar()
        self.act3 = tk.StringVar()
        self.netSize = tk.StringVar()
        self.clientLanguageChooser = ttk.Combobox(self.client, width=8, textvariable=self.act2)
        self.clientDistanceChooser = ttk.Combobox(self.client, width=8, textvariable=self.act3)
        self.searchButton = ttk.Button(self.client, text="Search", command=self.searchMe) #button
        self.numberChosen = ttk.Combobox(self.monty1, width=12, textvariable=self.act)
        self.networkSize = ttk.Combobox(self.monty1, width=12, textvariable=self.netSize)
        self.labelCheckbox = ttk.Label(self.monty, text="Information to Display", font=("System", 12)).grid(column=1, row=0, padx = 10, pady = 10)
        self.labelCombo = ttk.Label(self.monty, text="Search Ratio", font=("System", 12)).grid(column=1, row=6, padx = 10, pady = 10)
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
        self.chClient = tk.IntVar() #checkbox10
        self.chClient2 = tk.IntVar() #checkbox11
        self.chClient3 = tk.IntVar() #checkbox12
        self.weightGraph = tk.IntVar() #checkbox13
        self.scr = scrolledtext.ScrolledText(self.monty, width=70, height=14, wrap=tk.WORD)
        self.scrClient = scrolledtext.ScrolledText(self.client3, width=70, height=30, wrap=tk.WORD)
        self.messageEntry = scrolledtext.ScrolledText(self.messageTextEntry, width=70, height=15, wrap=tk.WORD)
        self.sentMessages = scrolledtext.ScrolledText(self.messageSentEntry, width=70, height=5, wrap=tk.WORD)
        self.figure = Figure(figsize=(7,6), dpi=85)
        self.aPlot = self.figure.add_subplot(111)
        self.canvas = None
        self.toolbar = None

        
    def labels(self):
        self.aLabel.grid(column=0, row=0)
        self.time.grid(column=0, row=0)
        self.timeZoneLabel.grid(column=0,row=1, padx=20, pady=4)
        self.infoZone.grid(column = 0, row = 3 , sticky = 'WE', padx=20, pady=4)
        self.monty1.grid(column=0, row=0, padx=20, pady=4)
        self.monty2.grid(column=0, row=0, padx=20, pady=4)
        self.browseButton.grid(column=0, row=0)
        self.browseButton2.grid(column=0, row=0)
        self.monty.grid(column=0, row=1, padx=20, pady=4)
        self.mngFilesFrame.grid(column=0, row=2, sticky='WE', padx=20, pady=4)
        self.client.grid(column=0, row=0, padx=20, pady=4)
        self.client2.grid(column=0, row=2, padx=20, pady=4)
        self.client3.grid(column=0, row=4, padx=20, pady=4)
        self.phoneNumber.grid(column=0, row=0, padx=60, pady=4)
        self.messageTextEntry.grid(column=0, row=2, padx=20, pady=4)
        self.messageSentEntry.grid(column=0, row=4, padx=20, pady=4)
        self.fileAttachmentEntry.grid(column=0, row=3, padx=20, pady=4)
        #self.textMessagePhone.grid(column=0, row=0, padx=60, pady=4)
        self.tab4.bind("<Button-3>", self.tab4Call)

    def bottons(self):
        self.action.grid(column=2, row=1)
        self.updateDB.grid(column=3, row=1)
        self.searchButton.grid(column=3, row=1)
        self.sentMessageButton.grid(column=3, row=1)

    def searchBar(self):
        self.nameEntered.grid(column=0, row=1, rowspan=2)
        self.nameEntered.focus()
        self.nameEntered.bind('<Return>', self.clickMe)
        self.clientLocation.grid(column=0, row=1, rowspan=2)
        self.clientLocation.focus()
        self.clientLocation.bind('<Return>', self.searchMe)
        self.phoneEntered.grid(column=0, row=1, rowspan=2)
        self.phoneEntered.focus()
        self.phoneEntered.bind(self.sendText)

    def dropDown(self):
        self.numberChosen['values'] = ('Find Provider', 'Build a network')
        self.numberChosen.grid(column=1, row=1, rowspan=2)
        self.numberChosen.current(0)
        self.numberChosen.bind(self.addNetworkSizeChooser)
        self.networkSize['values'] = ('3 links', '5 links', '8 links', '10 links')
        self.networkSize.grid(column=1, row=3, rowspan=1)
        self.networkSize.current(1)
        self.clientLanguageChooser['values'] = ('Russian', 'Spanish', 'English', 'Unspecified')
        self.clientLanguageChooser.grid(column=1, row=1, rowspan=1)
        self.clientLanguageChooser.current(0)
        self.clientDistanceChooser['values'] = (1, 3, 5, 10, 15, 25)
        self.clientDistanceChooser.grid(column=2, row=1, rowspan=1)
        self.clientDistanceChooser.current(3)

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
        self.checkClient = tk.Checkbutton(self.client2, text="Only Needles providers", variable=self.chClient)
        self.checkClient.grid(column=0, row=0, sticky=tk.W)
        self.checkClient.select()
        self.checkClient2 = tk.Checkbutton(self.client2, text=" Avoid Phys/Rad", variable=self.chClient2)
        self.checkClient2.grid(column=2, row=0, sticky=tk.W)
        self.checkClient2.select()
        self.weighted = tk.Checkbutton(self.monty1, text=" Weighted", variable=self.weightGraph)
        self.weighted.grid(column=2, row=3, sticky=tk.W)
        self.weighted.select()

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
        self.scrClient.grid(column=0, columnspan=3)
        self.messageEntry.grid(column=0, columnspan=3)
        self.sentMessages.grid(column=0, columnspan=3)

    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    def getNetworkSize(self):
        if self.netSize.get() == '3 links':
            return 3
        elif self.netSize.get() == '5 links':
            return 5
        elif self.netSize.get() == '8 links':
            return 8
        elif self.netSize.get() == '10 links':
            return 10

    def clearCanvas(self):
        try:
            self.canvas.get_tk_widget().destroy()
            self.toolbar.destroy()
            self.aPlot.clear()
            self.aPlot.set_xticks([])
            self.aPlot.set_yticks([])
        except Exception as e:
            log.loggingDebug(e, 'gui.py', 'clearCanvas method')

    def addNetworkSizeChooser(self):
        if self.netSize.get() == 'Build a network':
            print('display option for network size')
            self.networkSize.grid(column=1, row=3, rowspan=1)
        pass

    def runUpdateDatabase(self):
        self.createThreadUpdateDatabase()

    def updateDatabase(self):
        mBox.showinfo('Database Information', 'Stay in touch.\nUpdating takes some time (1-10 minutes)')
        upNeedles = self.chAddl1.get()
        upYelp = self.chAddl2.get()
        upHospital = self.chAddl3.get()
        print('Needles: ',upNeedles, 'Yelp:', upYelp,'Hospital:', upHospital)
        self.updateDB.configure(text='Updating...')
        self.createLoadingBullet()
        result = fillinDB(upNeedles,upYelp, upHospital, self.scr)
        if result == 0:
            mBox.showinfo('Database Information', 'Database successfully finished updating.\n')
            self.updateDB.configure(text='Update Database')
        else:
            mBox.showinfo('Database Information', 'Please launch Yelp.com on your webbrowser.\nAnd confirm that you are not a robot')
        updateProviderMissingGeoLocation()

    def sendMessageProcess(self):
        '''sendMessageToClient'''
        msg = self.messageEntry.get('1.0', tk.END)
        sendMessageToClient(msg, self.phone.get(), self.fName2, mBox, self.fDir2)
        self.createThreadSentMessages()
        print('Sending text')

    def runMessageSentDB(self):
        self.createThreadSentMessages()

    def sendText(self):
        self.createThreadSendMessage()

    def loadMe(self):
        for i in range(20):
            time.sleep(3)
            self.scrClient.insert(tk.INSERT,".")

    def tab4Call(self, event=None):
        self.runMessageSentDB()

    
    def searchMe(self, evcent = None):
        clearScreen(self.scrClient)
        self.scrClient.insert(tk.INSERT,"Searching")
        #self.createLoadingBullet()
        self.createThreadSearchTreatment()
            
    def listOfSentMessages(self):
        clearScreen(self.sentMessages)
        displaySentMessages(self.sentMessages)
        

    def searchTXPlan(self):
        treatmentPlan(self.act2.get(), self.scrClient, self.name2.get(), self.act3.get(), self.chClient.get(), self.chClient2.get(), self.chClient3.get())


    def runSearchTab1(self):
        node_sizes = createNodeSize(self.getNetworkSize(), self.weightGraph.get()) #####################
        
        ratio = self.searchAccuracy() 
        displayArgs = self.getCheckbox()
        if self.act.get() == 'Build a network':
            self.clearCanvas()
            clearScreen(self.scr)
            self.scr.insert(tk.INSERT,"Creating Network")
            #self.createLoadingBullet()
            fileToRead = ''
            if self.fName == None:
                fileToRead ='netRace.xlsx'
            else:
                fileToRead = self.fName
            ed, providerDict = readED(fileToRead, None, self.name.get(), self.getNetworkSize(), ratio, self.weightGraph.get())
            if len(ed) == 0:
                clearScreen(self.scr)
                confirmProvider(fileToRead, self.name.get(), self.scr, displayArgs, ratio)
                #possibleOptions = findProvider(fileToRead, self.name.get(), ratio, self.scr)
            else:
                clearScreen(self.scr)
                #confirmProvider(fileToRead, self.name.get(), self.scr, displayArgs, ratio)
                printOutProvider(providerDict, self.scr, displayArgs,ratio)
                pos=nx.spring_layout(ed)
                nx.draw_networkx(ed, pos, arrows = True, with_labels = True, ax = self.aPlot, font_size = 9, node_size = node_sizes)
                self.canvas = FigureCanvasTkAgg(self.figure, master=self.monty2)
                self.canvas.show()
                self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
                self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.monty2)
                self.toolbar.update()
                self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
        elif self.act.get() == 'Find Provider':
            confirmSearchProvider(self.name.get(), self.scr, displayArgs)
        

    def clickMe(self, event = None):
        self.createThreadRun()


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

    def getFileNameForAttachment(self):
        self.fDir2 = path.dirname(__file__)
        self.fName2 = fd.askopenfilename(parent=self.win, initialdir=self.fDir2)
        self.fileEntry2.delete(0, tk.END)
        self.fileEntry2.insert(0, self.fName2)

    def createThreadRun(self):
        runT = Thread(target=self.runSearchTab1)
        runT.setDaemon(True)
        runT.start()
        print(runT)

    def createThreadUpdateDatabase(self):
        runUpdate = Thread(target=self.updateDatabase)
        runUpdate.setDaemon(True)
        runUpdate.start()
        print(runUpdate)

    def createThreadSearchTreatment(self):
        searchTX = Thread(target=self.searchTXPlan)
        searchTX.setDaemon(True)
        searchTX.start()
        print(searchTX)

    def createThreadSendMessage(self):
        sendMessage = Thread(target=self.sendMessageProcess)
        sendMessage.setDaemon(True)
        sendMessage.start()
        print(sendMessage)

    def createLoadingBullet(self):
        loading = Thread(target=self.loadMe)
        loading.setDaemon(True)
        loading.start()
        print(loading)

    def createThreadSentMessages(self):
        messages = Thread(target=self.listOfSentMessages)
        messages.setDaemon(True)
        messages.start()
        print(messages)




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
    log.loggingWarning(e, 'gui.py', 'running mainloop')
