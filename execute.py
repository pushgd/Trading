import Constant
import Symbol
import Common
import time
import strategy
import json
import datetime
import DBHelper
import sys,itertools
spinner = itertools.cycle(['-', '/', '|', '\\'])
lastStrategyCheckTime = 0
tempCandleData = {}
lastDataReceiveTime = {}
high = {}
low = {}

symbolsList =['SILVER','CRUDEOIL','NATURALGAS']

symbolsIDList =['233041_MCX','235517_MCX','241002_MCX']
symbolMapping= dict(zip(symbolsIDList,symbolsList))
strategyList= []
def init():
    for s in symbolsList:
        Common.SymbolDict[s] = Symbol.Symbol(s, s,symbolsIDList[symbolsList.index(s)])
        Common.SymbolDict[s].setStrategy(Constant.STRATEGY_GANN_ANALYSIS )
    
    
    
    # Common.SymbolDict['2885_NSE'] = Symbol.Symbol('2885_NSE', 'RELINS','RELINS')
    # Common.SymbolDict['2643_NSE'] = Symbol.Symbol('2643_NSE', 'Phizer','PHIZER')
    print("Execute Init Done")

def update(symbol,data):
    lastStrategyCheckTime = 0
    # Common.SymbolDict[symbolMapping[symbol]].addNewTick(data)
    if (time.time() - lastStrategyCheckTime) >= Constant.STRATEGY_CHECK_DELAY:
        print("Check Strategy")
        lastStrategyCheckTime = time.time()
        Common.SymbolDict[symbolMapping[symbol]].update(data)
            # strategy.update(Common.SymbolDict[key])

    
temp ={}

def onNewData(message):
    sys.stdout.write(next(spinner))   # write the next character
    sys.stdout.flush()                # flush stdout buffer (actual character display)
    sys.stdout.write('\b')            # erase the last written char
    # if message.count('response') > 1 and message.endswith('3"}}\n'): 
    #     print(message.count('response'))
    message = message.strip()
    message = message.split("\n")
    for m in message:
        try:
            d = json.loads(m)
        except:
            print("error parsing")
            print(message)
            print("______________")
            return
        lastTradePrice = float(d['response']['data']['a9'])
        symbol =  d['response']['data']['z3']
        volume = float(d['response']['data']['c6'])
        createCandle(lastTradePrice, symbol,volume)
        # Common.SymbolDict[symbol].updateTrade(lastTradePrice)
        Common.SymbolDict[symbolMapping[symbol]].onNewData(lastTradePrice,volume)
    # try:
    #     temp[symbol]=temp[symbol]+1
    # except:
    #     temp[symbol]=1
    # print(len(temp.keys()))
    # print(temp)

    # for key in Common.SymbolDict.keys():
    #     Common.SymbolDict[key].updateTrade(float(d['response']['data']['a9']))
    # for key in Common.SymbolDict.keys():
    #     Common.SymbolDict[key].update(message)


def onCandleComplete(symbol, data):
    DBHelper.inertIntoTick(data[Constant.KEY_OPEN], data[Constant.KEY_HIGH], data[Constant.KEY_CLOSE],
                           data[Constant.KEY_LOW], data[Constant.KEY_VOLUME], symbol, data[Constant.KEY_DATE])
    update(symbol,data)


def createCandle(price, symbol, volume):

    if symbol not in tempCandleData:
        tempCandleData[symbol] = []
    if len(tempCandleData[symbol]) == 0:
        lastDataReceiveTime[symbol] = time.time()
    tempCandleData[symbol].append(price)
    if high.get(symbol, -1.0) < price:
        high[symbol] = price

    if low.get(symbol, 9999999.0) > price:
        low[symbol] = price
    timeelapsed = time.time()-lastDataReceiveTime[symbol]
    # print("Time since last candle Createed "+str(timeelapsed) +
    #       " last Cnadle Created "+str(lastDataReceiveTime[symbol])+"  "+str(len(tempCandleData[symbol])))
    if timeelapsed > Constant.CANDLE_CRATION_TIME:
        lastDataReceiveTime[symbol] = time.time()
        candle = {}
        candle[Constant.KEY_HIGH] = high[symbol]
        candle[Constant.KEY_LOW] = low[symbol]
        candle[Constant.KEY_CLOSE] = tempCandleData[symbol][len(
            tempCandleData[symbol])-1]
        candle[Constant.KEY_OPEN] = tempCandleData[symbol][0]
        candle[Constant.KEY_DATE] = datetime.datetime.now()
        candle[Constant.KEY_VOLUME] = volume
        onCandleComplete(symbol, candle)
        high[symbol] = -1
        low[symbol] = 999999
        tempCandleData[symbol].clear()
