import Constant
import Symbol
import Common
import time
import strategy
import json
import datetime
import DBHelper
import sys, itertools
import csv

spinner = itertools.cycle(['-', '/', '|', '\\'])
lastStrategyCheckTime = 0
tempCandleData = {}
lastDataReceiveTime = {}
high = {}
low = {}

symbolsList = []

symbolsIDList = []
symbolMapping = {}
strategyList = []


def init():
    with open('instruments.csv') as csvfile:
        fileReader = csv.DictReader(csvfile)
        for row in fileReader:
            if (row['active'] == '1' and row['exchange'] == 'NSE' and row['assettype'] == 'INDEX')\
                or (row['active'] == '1' and row['exchange'] == 'NSE' and row['series'] == 'EQ'):
                id = row['exchangetoken']
                name = row['symbolname']
                symbolsIDList.append(id)
                symbolsList.append(name)
                symbolMapping[id] = name
    print(symbolMapping)
    for s in symbolsList:
        Common.SymbolDict[s] = Symbol.Symbol(s, s, symbolsIDList[symbolsList.index(s)])
        Common.SymbolDict[s].setStrategy(Constant.STRATEGY_GANN_ANALYSIS)
        # Common.SymbolDict[s].setStrategy(Constant.STRATEGY_GANN_ANALYSIS)
    # Common.SymbolDict['2885_NSE'] = Symbol.Symbol('2885_NSE', 'RELINS','RELINS')
    # Common.SymbolDict['2643_NSE'] = Symbol.Symbol('2643_NSE', 'Phizer','PHIZER')
    print("Execute Init Done")


def update(symbol, data):
    Common.SymbolDict[symbolMapping[symbol]].update(data)
    # strategy.update(Common.SymbolDict[key])


temp = {}


def onNewData(message):
    sys.stdout.write(next(spinner))  # write the next character
    sys.stdout.flush()  # flush stdout buffer (actual character display)
    sys.stdout.write('\b')  # erase the last written char
    # if message.count('response') > 1 and message.endswith('3"}}\n'): 
    #     print(message.count('response'))
    message = message.strip()
    message = message.split("\n")
    for m in message:
        try:
            d = json.loads(m)
        except:
            # print("error parsing")
            # # print(message)
            # print("______________")
            return
        try:
            lastTradePrice = float(d['response']['data']['a9'])
            symbol = d['response']['data']['z3']
            volume = float(d['response']['data']['c6'])

            if Common.SymbolDict[symbolMapping[symbol]].isActive:
                Common.SymbolDict[symbolMapping[symbol]].onNewData(lastTradePrice, volume)
        except:
            print("error after parsing")


def onNewDataLocal(lastTradePrice, volume, symbol):
    # createCandle(lastTradePrice, symbol, volume)
    # Common.SymbolDict[symbol].updateTrade(lastTradePrice)
    if Common.SymbolDict[symbolMapping[symbol]].isActive:
        Common.SymbolDict[symbolMapping[symbol]].onNewData(lastTradePrice, volume)



def activateSymbol(symbol):
    print("Activating symbol " + symbol)
    Common.SymbolDict[symbol].activate()


def deactivateSymbol(symbol):
    print("Deactivating symbol " + symbol)
    Common.SymbolDict[symbol].deactivate()
