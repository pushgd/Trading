import Common
import Constant
import time
import datetime
import analyze

class CandleCreator():
    def __init__(self, frequency, callback, localFrequency=Constant.LOCAL_CANDLE_FREQUENCY):
        self.tempCandleData = []
        self.callback = callback
        self.low = 9999999
        self.high = -1
        self.lastDataReceiveTime = time.time()
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
    def __init__(self, symbolCallBack, trade, candleFrequency=3 * 60, params=None):
        if params is None:
            params = {}
        self.top = None
        self.tickData = []
        self.topIndex = -1
        self.candleCreator = CandleCreator(candleFrequency, self.onCandleComplete)
        self.symbolCallBack = symbolCallBack
        self.trade = trade
        self.params = params


    def update(self, trade, lastTradedPrice):
        print("Update base class")

    def onCandleComplete(self, candle):
        self.symbolCallBack(Constant.EVENT_CANDLE_CREATED, candle, self)
        # print("Candle Created for symbol ", self.trade.symbol.symbol, " candle ", candle)
        Common.LogAction("candleCreated,"+str(candle)+","+self.trade.strategyName+","+self.trade.symbol.symbolName)
        self.addNewTick(candle)
        self.onNewCandleCreated(candle)

    def onNewCandleCreated(self, candle):
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
            if currentPrice > trade.buyTriggerCall:
                trade.status = Constant.TRADE_ENTERED
                trade.entryTime = time.time()
                trade.takeProfit = Common.getNextGannLevel(trade.buyTriggerCall + 1)
                trade.stopLoss = Common.getPreviousGannLevel(trade.buyTriggerCall - 1)
                trade.entryPrice = currentPrice
                trade.type  = Constant.TRADE_TYPE_CALL

                print("Buy ", trade.symbol.symbolName, "on ", str(datetime.datetime.now()), " for Price ",
                      currentPrice)
                print("TakeProfit ", trade.takeProfit, " Stoploss ", trade.stopLoss)
                print("____________________________________________")
                Common.LogAction("Buying," + str(self.trade.entryPrice) + "," + str(self.trade.takeProfit) + "," + str(self.trade.stopLoss) + "," + trade.strategyName +"," + str(self.trade.symbol.symbolName) +"," + self.trade.type +"," + str(Common.getNextStrikePrice(self.trade.entryPrice)) + "," + str(Common.getSymbolExchangeCode(self.trade.symbol.symbolName, Common.getNextStrikePrice(self.trade.entryPrice), trade.type)))
                trade.entryTime = time.time()

                # trade.symbol.buy()

            if currentPrice < trade.buyTriggerPut:
                trade.status = Constant.TRADE_ENTERED
                trade.takeProfit = Common.getPreviousGannLevel(trade.buyTriggerPut - 1)
                trade.stopLoss = Common.getNextGannLevel(trade.buyTriggerPut + 1)
                trade.entryPrice = currentPrice
                trade.type = Constant.TRADE_TYPE_PUT
                print("Buy ", trade.symbol.symbolName, "on ",  str(datetime.datetime.now()), " for Price ",
                      currentPrice)
                print("TakeProfit ", trade.takeProfit, " Stoploss ", trade.stopLoss)
                print("____________________________________________")
                Common.LogAction("Buying," + str(self.trade.entryPrice) + "," + str(self.trade.takeProfit) + "," + str(self.trade.stopLoss) + "," + trade.strategyName +"," + str(self.trade.symbol.symbolName) +"," + self.trade.type +"," + str(Common.getPreviousStrikePrice(self.trade.entryPrice)) + "," + str(Common.getSymbolExchangeCode(self.trade.symbol.symbolName, Common.getPreviousStrikePrice(self.trade.entryPrice), trade.type)))
                trade.entryTime = time.time()

        elif trade.status == Constant.TRADE_ENTERED:
            if (currentPrice > trade.takeProfit and trade.type == Constant.TRADE_TYPE_CALL) or (currentPrice < trade.takeProfit and trade.type == Constant.TRADE_TYPE_PUT):
                trade.status = Constant.TRADE_COMPLETED
                print("Profit Sell ", trade.symbol.symbolName, "on ",  str(datetime.datetime.now()), " for price ",
                      currentPrice, " with Profit ", (currentPrice - trade.entryPrice))
                print("____________________________________________")
                trade.exitPrice = currentPrice
                trade.gain = (currentPrice-trade.entryPrice)
                self.symbolCallBack(Constant.EVENT_TRADE_COMPLETED, None, self)
                Common.LogAction("SELL,PROFIT," + str(self.trade.exitPrice) + "," + str(self.trade.gain) + ","+trade.strategyName+","  + str(self.trade.symbol.symbolName))
            if (currentPrice < trade.stopLoss  and trade.type == Constant.TRADE_TYPE_CALL) or (currentPrice > trade.stopLoss  and trade.type == Constant.TRADE_TYPE_PUT):
                trade.status = Constant.TRADE_COMPLETED
                print("Loss sell ", trade.symbol.symbolName, "on ",  str(datetime.datetime.now()), " for price ",
                      currentPrice, " with loss ", (trade.entryPrice - currentPrice))
                print("____________________________________________")
                trade.exitPrice = currentPrice
                trade.gain = (currentPrice-trade.entryPrice)
                Common.LogAction("SELL,LOSS," + str(self.trade.exitPrice) + "," + str(self.trade.gain) + ","+trade.strategyName+","  + self.trade.symbol.symbolName)
                self.symbolCallBack(Constant.EVENT_TRADE_COMPLETED, None, self)
            if time.time() - trade.entryTime >= Constant.TRADE_TIMEOUT_TIME:
                self.trade.status = Constant.TRADE_TIMED_OUT
                self.trade.gain = currentPrice - trade.entryPrice
                self.trade.exitPrice = currentPrice
                print("Timeout Sell ", trade.symbol.symbolName, "on ", str(datetime.datetime.now()), " for price ",
                      currentPrice, " with gain ", self.trade.gain)
                print("____________________________________________")
                Common.LogAction("SELL,Timeout," + str(self.trade.exitPrice) + "," + str(
                    self.trade.gain) + "," + trade.strategyName + "," + self.trade.symbol.symbolName)
                self.symbolCallBack(Constant.EVENT_TRADE_TIMEOUT, None, self)

    def onNewCandleCreated(self, candle):
        if self.trade.status == Constant.TRADE_NOT_STARTED:
            self.trade.buyTriggerCall = Common.getNextGannLevel(candle[Constant.KEY_CLOSE])
            self.trade.buyTriggerPut = Common.getPreviousGannLevel(candle[Constant.KEY_CLOSE])
            self.trade.status = Constant.TRADE_LOOKING_FOR_ENTRY
            Common.LogAction("EnteringTrade," + str(self.trade.buyTriggerCall) +","+ str(self.trade.buyTriggerPut)+",," + str(self.trade.symbol.symbolName))
            print("Entering Trade for ", self.trade.symbol.symbolName," ",self.top.info[Constant.KEY_DATE])
        # print("Candle Created for symbol ",self.trade.symbol.symbol," candle ",candle)


class MACrossover(StrategyBaseClass):
    def update(self, trade, currentPrice, volume):
        self.candleCreator.createCandle(currentPrice, volume)
        if trade.status == Constant.TRADE_LOOKING_FOR_ENTRY:
            if currentPrice > trade.buyTriggerCall:
                trade.status = Constant.TRADE_ENTERED
                print("MAC Buy ", trade.symbol.symbolName, "on ", self.top.info[Constant.KEY_DATE], " for Price ",
                      currentPrice)
                print("TakeProfit ", trade.takeProfit, " Stoploss ", trade.stopLoss)
                print("____________________________________________")
        elif trade.status == Constant.TRADE_ENTERED:
            if currentPrice > trade.takeProfit:
                trade.status = Constant.TRADE_COMPLETED
                print("Profit Sell ", trade.symbol.symbolName, "on ", self.top.info[Constant.KEY_DATE], " for price ",
                      currentPrice, " with Profit ", (currentPrice - trade.entryPrice))
                print("____________________________________________")
                trade.exitPrice = currentPrice
                trade.gain = (trade.entryPrice - currentPrice)
                trade.status = Constant.TRADE_COMPLETED
                self.symbolCallBack(Constant.EVENT_TRADE_COMPLETED, None, self)
            elif currentPrice < trade.stopLoss:
                print("Loss sell ", trade.symbol.symbolName, "on ", self.top.info[Constant.KEY_DATE], " for price ",
                      currentPrice, " with loss ", (trade.entryPrice - currentPrice))
                print("____________________________________________")
                trade.exitPrice = currentPrice
                trade.gain = (trade.entryPrice - currentPrice)
                trade.status = Constant.TRADE_COMPLETED
                self.symbolCallBack(Constant.EVENT_TRADE_COMPLETED, None, self)

    def onNewCandleCreated(self, candle):
        if self.trade.status == Constant.TRADE_NOT_STARTED:
            if self.topIndex < 2:
                return
            last = self.tickData[self.trade.symbol.topIndex - 1]
            if Common.isUpwardPattern(last) and self.top.info[Constant.KEY_CLOSE] > self.top.info[
                Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] and last.info[Constant.KEY_HIGH] < last.info[
                Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] and self.top.info[Constant.KEY_RSI] >= 55:
                self.trade.status = Constant.TRADE_LOOKING_FOR_ENTRY
                self.trade.buyTriggerCall = self.top.info[Constant.KEY_HIGH]
                self.trade.stopLoss = Common.getLowestValue(self)
                self.trade.takeProfit = self.trade.buyTriggerCall + abs(self.trade.buyTriggerCall - self.trade.stopLoss) * self.trade.symbol.riskFactor
                print("Entering Trade for ", self.trade.symbol.symbolName, " ", self.top.info[Constant.KEY_DATE])

def init():
    # Common.strategyDict[Constant.STRATEGY_GANN_ANALYSIS] = GannAnalysis()
    # Common.strategyDict[Constant.STRATEGY_MA_CROSSOVER_UP] = MACrossover()
    print("Init Strategy")
