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
import logging

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
            # if (row['active'] == '1' and row['exchange'] == 'MCX' and row['assettype'] == 'FUTCOM'):
            if (row['active'] == '1' and row['exchange'] == 'NSE' and row['assettype'] == 'INDEX')\
                or (row['active'] == '1' and row['exchange'] == 'NSE' and row['series'] == 'EQ'):
                exchangeToken = row['exchangetoken']
                symbolname = row['symbolname']
                if symbolname == 'Nifty Bank':
                    symbolname = 'BANKNIFTY'

                tradingsymbol = row['tradingsymbol']
                symbolsIDList.append(id)
                # symbolsList.append(name)
                # symbolMapping[id] = name
                Common.SymbolDict[exchangeToken] = Symbol.Symbol(symbolname, tradingsymbol, exchangeToken)
                Common.SymbolDict[exchangeToken].setStrategy(Constant.STRATEGY_GANN_ANALYSIS)
    print(Common.SymbolDict.keys())
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
            Common.LogDataReceived(str(lastTradePrice) + "," + str(volume) + "," + symbol)
        except Exception:
            print("Error Parsing")
            return
        # logging.dataReceived(str(lastTradePrice)+","+str(volume)+","+symbolMapping[symbol])
        if Common.SymbolDict[symbol].isActive:
            Common.SymbolDict[symbol].onNewData(lastTradePrice, volume)
            DBHelper.addTradePrice(symbol,lastTradePrice,volume)


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
