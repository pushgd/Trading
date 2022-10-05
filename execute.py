import copy
import re

import API
import Constant
import Symbol
import Common
import time
import strategy
import json
import datetime
import DBHelper
import sys
import itertools
import csv
import logging
from constants.asset_type import AssetTypeEnum
from constants.chart_exchange import ChartExchangeEnum
from constants.intraday_interval import IntradayIntervalEnum

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
    with open('symbolConfig.csv') as csvfile:
        fileReader = csv.DictReader(csvfile)
        for row in fileReader:
            s = Symbol.Symbol(row['symbolname'])
            if row['optionSymbol']=='':
                s.optionSymbol = row['symbolname']
            else:
                s.optionSymbol = row['optionSymbol']

            if row['exchange'] == 'BSE':
                s.exchange = ChartExchangeEnum.BSE
            elif row['exchange'] == 'NSE':
                s.exchange = ChartExchangeEnum.NSE
            s.isActive = row['Active'] != ''
            print(s.symbolName)
            if s.isActive:
                symbolsList.append(s)
    for symbol in symbolsList:
        with open('instruments.csv') as csvfile:
            fileReader = csv.DictReader(csvfile)
            for row in fileReader:
                if row['symbolname'] == symbol.symbolName and row['exchange'] == symbol.exchange  and (
                        row['assettype'] == 'EQUITY' or row['assettype'] == 'INDEX'):
                    if symbol.isActive:
                        print("Active symbol: ",symbol.symbolName)
                    symbol.exchangeToken = row['exchangetoken']
                    symbol.quantity = row['lotsize']
                    symbol.tradingSymbol = row['tradingsymbol']
                    if row['assettype'] == 'EQUITY':
                        symbol.assetType = AssetTypeEnum.EQUITY
                    elif row['assettype'] == 'INDEX':
                        symbol.assetType = AssetTypeEnum.INDEX
                    Common.SymbolDict[symbol.exchangeToken] = symbol
                    # symbol.setStrategy(Constant.STRATEGY_MA_CROSSOVER_UP)
                    continue

    # with open('instruments.csv') as csvfile:
    #     fileReader = csv.DictReader(csvfile)
    #     for row in fileReader:
    #         # if (row['active'] == '1' and row['exchange'] == 'MCX' and row['assettype'] == 'FUTCOM'):
    #         if (row['active'] == '1'):
    #             exchangeToken = row['exchangetoken']
    #             symbolname = row['symbolname']
    #             if symbolname == 'Nifty Bank':
    #                 symbolname = 'BANKNIFTY'
    #             elif symbolname == 'Nifty 50':
    #                 symbolname = 'NIFTY'
    #
    #             tradingsymbol = row['tradingsymbol']
    #             symbolsIDList.append(id)
    #
    #
    #             Common.SymbolDict[exchangeToken] = Symbol.Symbol(
    #                 symbolname, tradingsymbol, exchangeToken)
    #             Common.SymbolDict[exchangeToken].setStrategy(
    #                 Constant.STRATEGY_GANN_ANALYSIS)
    #             Common.SymbolDict[exchangeToken].quantity = row['lotsize']
    #             Common.SymbolDict[exchangeToken].assetType = row['assettype']
    # symbol = Common.SymbolDict[exchangeToken]
    # print(str(Common.getSymbolExchangeCode(
    #     symbol.symbolName, Common.getNextStrikePrice(1530,stepsize=20), Constant.TRADE_TYPE_CALL,
    #     None if symbol.assetType != 'EQUITY' else datetime.datetime.now().date())))
    print(Common.SymbolDict.keys())
    simulate("HDFC","2022-09-01","2022-10-01",Constant.STRATEGY_MA_CROSSOVER_UP)
    print("Execute Init Done")
    exit()



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
            Common.LogDataReceived(
                str(lastTradePrice) + "," + str(volume) + "," + symbol)
        except Exception:
            print("------------------------------------------")
            print("Error Parsing")
            print(d)
            print("------------------------------------------")
            return
        # logging.dataReceived(str(lastTradePrice)+","+str(volume)+","+symbolMapping[symbol])
        if Common.SymbolDict[symbol].isActive:
            Common.SymbolDict[symbol].onNewData(lastTradePrice, volume)
            # DBHelper.addTradePrice(symbol, lastTradePrice, volume)


def onNewDataLocal(lastTradePrice, volume, symbol,candle):
    # createCandle(lastTradePrice, symbol, volume)
    # Common.SymbolDict[symbol].updateTrade(lastTradePrice)
    # if Common.SymbolDict[symbolMapping[symbol]].isActive:
    t = Common.SymbolDict[symbol].tradeList[-1]
    t.strategy.onCandleComplete(candle)
    t.strategy.update(t, candle[Constant.KEY_HIGH], candle[Constant.KEY_VOLUME])
    t.strategy.update(t, candle[Constant.KEY_LOW], candle[Constant.KEY_VOLUME])




def activateSymbol(symbol):
    print("Activating symbol " + symbol)
    Common.SymbolDict[symbol].activate()


def deactivateSymbol(symbol):
    print("Deactivating symbol " + symbol)
    Common.SymbolDict[symbol].deactivate()

def simulate(symbol,startDate,endDate,strategy,parames={}):
    Common.simulate = True

    lastDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    tillDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")
    tillDate2 = datetime.datetime.strptime(endDate, "%Y-%m-%d")

    s =  copy.deepcopy(Common.getSymbolByTradingSymbol(symbol))
    s.tradeList.clear()

    historicalData = []
    while tillDate > startDate:
        data = json.loads(s.gethHistoricalData(IntradayIntervalEnum.M5, str(tillDate.year), str(tillDate.month),str(tillDate.day)))
        tillDate = datetime.datetime.strptime(data['nextTillDate'], "%Y-%m-%d %H:%M:%S")
        data['data'].reverse()
        historicalData.extend( data['data'])
    historicalData.reverse()
    inBetweenHistoricalData = []
    while tillDate2 > startDate:
        data = json.loads(
            s.gethHistoricalData(IntradayIntervalEnum.M1, str(tillDate2.year), str(tillDate2.month), str(tillDate2.day)))
        tillDate2 = datetime.datetime.strptime(data['nextTillDate'], "%Y-%m-%d %H:%M:%S")
        data['data'].reverse()
        inBetweenHistoricalData.extend(data['data'])
    inBetweenHistoricalData.reverse()
    s.setStrategy(strategy,historicalData =  [i for i in historicalData if datetime.datetime.strptime(i[0], "%Y-%m-%d %H:%M:%S") < startDate])
    lastIndex = 0
    for candle in historicalData:

        trade = s.tradeList[-1]
        date = datetime.datetime.strptime(candle[0], "%Y-%m-%d %H:%M:%S")
        if date<startDate:
            continue
        for i in range(lastIndex,len(inBetweenHistoricalData)):
            c = inBetweenHistoricalData[i]
            lastIndex = lastIndex+1
            d = datetime.datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S")
            if d <= date and d > lastDate:
                trade.strategy.update(trade, c[1], c[5])
                trade.strategy.update(trade, c[2], c[5])
                trade.strategy.update(trade, c[3], c[5])
                trade.strategy.update(trade, c[4], c[5])
            if d > date:
                break
        c = {
            Constant.KEY_OPEN: candle[1],
            Constant.KEY_HIGH: candle[2],
            Constant.KEY_LOW: candle[3],
            Constant.KEY_CLOSE: candle[4],
            Constant.KEY_DATE: d,
            Constant.KEY_VOLUME: candle[5]}
        lastDate = datetime.datetime.strptime(candle[0], "%Y-%m-%d %H:%M:%S")
        # trade.strategy.update(trade, candle[Constant.KEY_HIGH], candle[Constant.KEY_VOLUME])
        trade.strategy.onCandleComplete(c)
        # print("Done for ",date)
        Common.simulate = False


        print("Simulation completed for ",symbol)


