from collections import defaultdict
from collections import namedtuple
import pandas
from find import *

def initChartSwap():
    ChartSwap = namedtuple('ChartSwap', 'File Dict')
    pandaFile = pandas.read_excel('ChartSwap.xlsx')
    pandaDict = defaultdict(list)
    return ChartSwap(pandaFile, pandaDict)
    
def readChartSwap(state):
    initiated = initChartSwap()
    pandaFile = initiated.File
    pandaDict = initiated.Dict
    for elem in pandaFile.index:
        if pandaFile['Account Site'][elem] == state:
            pandaDict[str(pandaFile['Attention'][elem])].append(str(pandaFile['Account Name'][elem]))
    return pandaDict

def findOnChartSwap(location, myDict, n):
    looking = []
    for key, value in myDict.items():
        result = searchRatio(key.upper(), location.upper(), n)
        if result:
            for i in value:
                looking.append(i)
    return looking

def findOnChartSwapStartsWith(location, myDict):
    looking = [value for key, value in myDict.items() if key.upper().startswith(location.upper())]
    return looking

