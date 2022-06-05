import Constant
import Symbol
import Common
import time
import strategy
import json
import datetime
import DBHelper

lastStrategyCheckTime = 0
tempCandleData = {}
lastDataReceiveTime = {}
high = {}
low = {}


def init():
    Common.SymbolDict['Nifty50'] = Symbol.Symbol('Nifty50', 'N50')


def update(data):
    lastStrategyCheckTime = 0
    while(1):
        diff = time.time() - lastStrategyCheckTime
        if (time.time() - lastStrategyCheckTime) >= Constant.STRATEGY_CHECK_DELAY:
            print("Check Strategy")
            lastStrategyCheckTime = time.time()
            for key in Common.SymbolDict.keys():
                Common.SymbolDict[key].update(data)
                strategy.update(Common.SymbolDict[key])

    for key in Common.SymbolDict.keys():
        Common.SymbolDict[key].updateTrade(float(data['close']))


def onNewData(message):
    try:
        d = json.loads(message)
    except:
        print("error parsing")
        return
    createCandle(float(d['response']['data']['a9']), d['response']
                 ['data']['z3'], float(d['response']['data']['c6']))
    # for key in Common.SymbolDict.keys():
    #     Common.SymbolDict[key].update(message)


def onCandleComplete(symbol, data):
    DBHelper.inertIntoTick(data[Constant.KEY_OPEN], data[Constant.KEY_HIGH], data[Constant.KEY_CLOSE],
                           data[Constant.KEY_LOW], data[Constant.KEY_VOLUME], symbol, data[Constant.KEY_DATE])


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
