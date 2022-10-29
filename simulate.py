import copy

from constants.intraday_interval import IntradayIntervalEnum

import Common
import datetime
import Constant
import json

def simulate(symbol,startDate,endDate,strategy,parames={}):
    Common.simulate = True

    lastDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    tillDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")
    tillDate2 = datetime.datetime.strptime(endDate, "%Y-%m-%d")

    # s =  Common.getSymbolBySymbolName(symbol)
    s =  copy.deepcopy(Common.getSymbolBySymbolName(symbol))
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

    if strategy == Constant.STRATEGY_MA_CROSSOVER_UP:
        simulateMACrossoverUp(historicalData, inBetweenHistoricalData, lastDate, s, startDate, strategy)
    elif strategy == Constant.STRATEGY_GANN_ANALYSIS:
        simulateGANN(historicalData, inBetweenHistoricalData, lastDate, s, startDate, strategy)

    Common.simulate = False
    replay = []
    for t in s.tradeList:
        replay.append(t.serialize())
    print("Simulation completed for ", symbol)

    return replay


def simulateMACrossoverUp(historicalData, inBetweenHistoricalData, lastDate, s, startDate, strategy):
    oldData = [i for i in historicalData if
                      datetime.datetime.strptime(i[0], "%Y-%m-%d %H:%M:%S") < startDate]
    s.setStrategy(strategy ).simulate =True
    lastIndex = 0
    for candle in historicalData:

        date = datetime.datetime.strptime(candle[0], "%Y-%m-%d %H:%M:%S")
        if date < startDate:
            continue
        for i in range(lastIndex, len(inBetweenHistoricalData)):
            c = inBetweenHistoricalData[i]
            lastIndex = lastIndex + 1
            d = datetime.datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S")
            if d <= date and d > lastDate:
                s.tradeList[-1].strategy.update(s.tradeList[-1], c[1], c[5])
                s.tradeList[-1].strategy.update(s.tradeList[-1], c[2], c[5])
                s.tradeList[-1].strategy.update(s.tradeList[-1], c[3], c[5])
                s.tradeList[-1].strategy.update(s.tradeList[-1], c[4], c[5])
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
        s.tradeList[-1].strategy.onCandleComplete(c)
        # print("Done for ",date)
def simulateGANN(historicalData, inBetweenHistoricalData, lastDate, s, startDate, strategy):
    s.setStrategy(strategy).simulate = True
    lastIndex = 0
    for candle in historicalData:

        date = datetime.datetime.strptime(candle[0], "%Y-%m-%d %H:%M:%S")
        if date < startDate:
            continue
        for i in range(lastIndex, len(inBetweenHistoricalData)):
            c = inBetweenHistoricalData[i]
            lastIndex = lastIndex + 1
            d = datetime.datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S")
            if d <= date and d > lastDate:
                s.tradeList[-1].strategy.update(s.tradeList[-1], c[1], c[5])
                s.tradeList[-1].strategy.update(s.tradeList[-1], c[2], c[5])
                s.tradeList[-1].strategy.update(s.tradeList[-1], c[3], c[5])
                s.tradeList[-1].strategy.update(s.tradeList[-1], c[4], c[5])
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
        s.tradeList[-1].strategy.onCandleComplete(c)
