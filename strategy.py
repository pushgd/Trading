import Common
import Constant
import time
import datetime
import  analyze

class CandleCreator():
    def __init__(self, frequency, callback, localFrequency=Constant.LOCAL_CANDLE_FREQUENCY):
        self.tempCandleData = []
        self.callback = callback
        self.low = 9999999
        self.high = -1
        self.lastDataReceiveTime =  time.time()
        self.localTick = 0
        self.frequency = frequency
        self.localFrequency = localFrequency

    def createCandle(self, price, volume):
        # self.lastDataReceiveTime = time.time()
        self.tempCandleData.append(price)
        self.localTick = self.localTick + 1
        if self.high < price:
            self.high = price
        if self.low > price:
            self.low = price
        timeelapsed = time.time() - self.lastDataReceiveTime
        if timeelapsed > self.frequency or (Common.localFile and self.localTick > self.localFrequency):
            self.localTick = 0
            self.lastDataReceiveTime = time.time()
            candle = {Constant.KEY_HIGH: self.high, Constant.KEY_LOW: self.low,
                      Constant.KEY_CLOSE: self.tempCandleData[len(self.tempCandleData) - 1],
                      Constant.KEY_OPEN: self.tempCandleData[0], Constant.KEY_DATE: datetime.datetime.now(),
                      Constant.KEY_VOLUME: volume}
            self.high = -1
            self.low = 999999
            self.tempCandleData.clear()
            self.callback(candle)


class StrategyBaseClass:
    def __init__(self, symbolCallBack,trade,candleFrequency = 3 * 60):
        self.top = None
        self.tickData = []
        self.topIndex = -1
        self.candleCreator = CandleCreator(candleFrequency, self.onCandleComplete)
        self.symbolCallBack = symbolCallBack
        self.trade = trade

    def update(self, trade, lastTradedPrice):
        print("Update base class")

    def onCandleComplete(self, candle):
        self.symbolCallBack(Constant.EVENT_CANDLE_CREATED,candle,self)
        self.addNewTick(candle)
        self.candleCreated(candle)
    def candleCreated(self,candle):
        print("Need to Implement")

    def addNewTick(self, data):
        self.topIndex = self.topIndex + 1
        self.tickData.append(Common.Tick(data))
        self.top = self.tickData[self.topIndex]
        if self.topIndex > 0:
            if (self.top.info[Constant.KEY_CLOSE] > self.tickData[self.topIndex - 1].info[Constant.KEY_CLOSE]):
                self.top.info[Constant.KEY_GAIN] = self.top.info[Constant.KEY_CLOSE] - \
                                                   self.tickData[self.topIndex - 1].info[Constant.KEY_CLOSE]
                self.top.info[Constant.KEY_LOSS] = 0
            else:
                self.top.info[Constant.KEY_LOSS] = abs(
                    self.top.info[Constant.KEY_CLOSE] - self.tickData[self.topIndex - 1].info[Constant.KEY_CLOSE])
                self.top.info[Constant.KEY_GAIN] = 0
        analyze.update(self)

class GannAnalysis(StrategyBaseClass):

    def update(self, trade, currentPrice, volume):
        self.candleCreator.createCandle(currentPrice, volume)
        if trade.status == Constant.TRADE_LOOKING_FOR_ENTRY:
            if currentPrice > trade.buyTrigger:
                print("Buy ", trade.symbol.name, " on ", self.top.info[Constant.KEY_DATE], " for Price ",
                      currentPrice)
                trade.takeProfit = Common.getNextGannLevel(trade.buyTrigger + 3)
                trade.stopLoss = Common.getPreviousGannLevel(trade.buyTrigger - 3)
                trade.entryPrice = currentPrice
                print("TakeProfit ", trade.takeProfit, " Stoploss ", trade.stopLoss)
                print("____________________________________________")
                trade.status = Constant.TRADE_ENTERED
        elif trade.status == Constant.TRADE_ENTERED:
            if currentPrice > trade.takeProfit:
                print("Profit Sell ", trade.symbol.name, " on ", self.top.info[Constant.KEY_DATE], " for price ",
                      currentPrice, " with Profit ", (currentPrice - trade.entryPrice))
                print("____________________________________________")
                trade.exitPrice = currentPrice
                trade.status = Constant.TRADE_COMPLETED
                self.symbolCallBack(Constant.EVENT_TRADE_COMPLETED,None,self)
            if currentPrice < trade.stopLoss:
                print("Loss sell ", trade.symbol.name, " on ", self.top.info[Constant.KEY_DATE], " for price ",
                      currentPrice, " with loss ", (trade.entryPrice - currentPrice))
                print("____________________________________________")
                trade.exitPrice = currentPrice
                trade.status = Constant.TRADE_COMPLETED
                self.symbolCallBack(Constant.EVENT_TRADE_COMPLETED, None, self)

    def candleCreated(self, candle):
        if self.trade.status == Constant.TRADE_NOT_STARTED:
            self.trade.buyTrigger = Common.getNextGannLevel(candle[Constant.KEY_CLOSE])
            self.trade.status = Constant.TRADE_LOOKING_FOR_ENTRY
            print("Entering sell for ",self.trade.symbol.symbol)
        print("Candle Created for symbol ",self.trade.symbol.symbol," candle ",candle)


class MACrossover(StrategyBaseClass):
    def update(self, trade, lastTradedPrice):
        print("MAC update")


def init():
    # Common.strategyDict[Constant.STRATEGY_GANN_ANALYSIS] = GannAnalysis()
    # Common.strategyDict[Constant.STRATEGY_MA_CROSSOVER_UP] = MACrossover()
    print("Init Strategy")
