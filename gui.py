import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox
from net import *
from find import *
import networkx as nx
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import ToolTip as tt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import numpy as np
from os import path
from tkinter import filedialog as fd



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
        self.monty1.grid(column=0, row=0, padx=8, pady=4)

        self.monty = ttk.LabelFrame(self.tab1, text=' Monty1 Python ')
        self.monty.grid(column=0, row=1, padx=8, pady=4)

        self.mngFilesFrame = ttk.LabelFrame(self.tab1, text=' Manage Files: ')
        self.mngFilesFrame.grid(column=0, row=2, sticky='WE', padx=10, pady=5)

        self.browseButton = ttk.Button(self.mngFilesFrame, text="Browse ...",command=self.getFileName)
        self.browseButton.grid(column=0, row=0, sticky=tk.W)

        self.fName = None #name of a file to browse
        self.fDir = None #dir of a file

        self.file = tk.StringVar()
        self.entryLen = 60
        self.fileEntry = ttk.Entry(self.mngFilesFrame, width=self.entryLen,textvariable=self.file)
        self.fileEntry.grid(column=1, row=0, sticky=tk.W)
       


        self.monty2 = ttk.LabelFrame(self.tab2, text=' Provider Network')
        self.monty2.grid(column=0, row=0, padx=8, pady=4)

        self.aLabel = ttk.Label(self.monty1, text="Search Box") #label
        self.action = ttk.Button(self.monty1, text="Run", command=self.clickMe) #button
        self.name = tk.StringVar() #search name
        self.nameEntered = ttk.Entry(self.monty1, width=40, textvariable=self.name) #name entered

        self.aLabel2 = ttk.Label(self.monty1, text="Choose an action:").grid(column=1, row=0) #drop down box
        self.act = tk.StringVar()
        self.numberChosen = ttk.Combobox(self.monty1, width=12, textvariable=self.act)

        self.chVarUn = tk.IntVar() #checkbox 1
        self.chVarEn = tk.IntVar() #checkbox 2
        self.chVarEn2 = tk.IntVar() #checkbox 3

        self.radVar = tk.IntVar() #radio button

        self.scr = scrolledtext.ScrolledText(self.monty, width=50, height=4, wrap=tk.WORD)

        self.figure = Figure(figsize=(7,5), dpi=90)
        self.aPlot = self.figure.add_subplot(111)

        self.canvas = None
        self.toolbar = None

        
    def labels(self):
        self.aLabel.grid(column=0, row=0)

    def bottons(self):
        self.action.grid(column=2, row=1)

    def searchBar(self):
        self.nameEntered.grid(column=0, row=1, rowspan=3)
        self.nameEntered.focus()

    def dropDown(self):
        self.numberChosen['values'] = ('Find Provider', 'Build a network')
        self.numberChosen.grid(column=1, row=1, rowspan=2)
        self.numberChosen.current(0)

    def checkBox(self):
        self.check2 = tk.Checkbutton(self.monty, text="UnChecked", variable=self.chVarUn)
        self.check2.grid(column=0, row=4, sticky=tk.W)
        self.check2.deselect()

        self.check3 = tk.Checkbutton(self.monty, text="Enabled", variable=self.chVarEn)
        self.check3.grid(column=1, row=4, sticky=tk.W)
        self.check3.select()

        self.check1 = tk.Checkbutton(self.monty, text="Enabled", variable=self.chVarEn2)
        self.check1.select()
        self.check1.grid(column=2, row=4, sticky=tk.W)

    def radioButton(self):
        self.rad1 = tk.Radiobutton(self.monty, text='One', variable=self.radVar, value=1, command=self.radCall)
        self.rad1.grid(column=0, row=5, sticky=tk.W)

        self.rad2 = tk.Radiobutton(self.monty, text='Two', variable=self.radVar, value=2, command=self.radCall)
        self.rad2.grid(column=1, row=5, sticky=tk.W)

        self.rad3 = tk.Radiobutton(self.monty, text='Three', variable=self.radVar, value=3, command=self.radCall)
        self.rad3.grid(column=2, row=5, sticky=tk.W)

        self.rad4 = tk.Radiobutton(self.monty, text='Four', variable=self.radVar, value=4, command=self.radCall)
        self.rad4.grid(column=0, row=6, sticky=tk.W)

        self.rad5 = tk.Radiobutton(self.monty, text='Five', variable=self.radVar, value=5, command=self.radCall)
        self.rad5.grid(column=1, row=6, sticky=tk.W)

        self.rad6 = tk.Radiobutton(self.monty, text='Six', variable=self.radVar, value=6, command=self.radCall)
        self.rad6.grid(column=2, row=6, sticky=tk.W)

    def scrollableText(self):
        self.scr.grid(column=0, columnspan=3)

    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    def clickMe(self):
        
        if self.act.get() == 'Build a network':
            try:
                self.canvas.get_tk_widget().destroy()
                self.toolbar.destroy()
            except Exception as e:
                pass
            fileToRead = ''
            if self.fName == None:
                fileToRead ='net1h.xls'
            else:
                fileToRead = self.fName
            providerDict, newDict, ed = processFacility(fileToRead, None, self.name.get(), 7)
            if len(ed) == 0:
                while len(ed) == 0:
                    providerDict, *rest = processAll(fileToRead)
                    newList = providerDictToList(providerDict)
                    possibleOptions = deepSearch(self.name.get(), newList, 10, 0.5)
                    self.scr.insert(tk.INSERT, ''.join(str(possibleOptions)))
                    if len(possibleOptions) < 10:
                        possibleOptions = deepSearch(self.name.get(), newList, 10, 0.2)
                        providerDict, newDict, ed = processFacility(fileToRead, None, self.name.get(), 7)
                        self.scr.insert(tk.INSERT, ''.join(str(possibleOptions)))
    

            self.aPlot.clear()
            self.aPlot.set_xticks([])
            self.aPlot.set_yticks([])
        
            pos=nx.spring_layout(ed)
            nx.draw_networkx(ed, pos, arrows = True, with_labels = True, ax = self.aPlot, font_size = 10)
            #nx.draw_networkx(ed)
            #plt.show()

            self.canvas = FigureCanvasTkAgg(self.figure, master=self.monty2)
            self.canvas.show()
            self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.monty2)
            self.toolbar.update()
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            
        elif self.act.get() == 'Find Provider':
            pass

	
    def radCall(self):
        r = self.radVar.get()
        if r == 1:
                pass
        if r == 2:
                pass

    def _msgBox(self):
        mBox.showinfo('Provider Network info box','Created by Artem Kovtunenko\n Version 1.0')
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
w.mainloop()
