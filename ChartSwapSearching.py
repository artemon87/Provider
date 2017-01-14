from collections import defaultdict
from collections import namedtuple
import pandas

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

def findOnChartSwap(location, myDict):
    looking = [value for key, value in myDict.items() if location in key]
    return looking

def findOnChartSwapStartsWith(location, myDict):
    looking = [value for key, value in myDict.items() if key.startswith(location)]
    return looking

