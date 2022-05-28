import Constant
import Symbol
import Common


def init():
    Common.SymbolDict['Nifty50'] = Symbol.Symbol('Nifty50', 'N50')


def update(data):
    for key in Common.SymbolDict.keys():
        Common.SymbolDict[key].update(data)
