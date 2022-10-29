from constants.asset_type import AssetTypeEnum

import Common
import Constant
import time
import datetime
import analyze
import csv
import abc
from constants.exchange import ExchangeEnum


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
        if timeelapsed > self.frequency:
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
    def __init__(self, symbolCallBack, trade, params=None):
        if params is None:
            params = {}
        self.top = None
        self.quantity = int(params.get(Constant.PARAMETER_QUANTITY,1))
        if Constant.KEY_TICK_DATA in params:
            self.tickData = params[Constant.KEY_TICK_DATA].copy()
        else:
            self.tickData = {}
        self.tickData = []
        self.topIndex = -1
        self.candleCreator = CandleCreator(
            int(params.get(Constant.PARAMETER_CANDLE_FREQUENCY,5*60)), self.onCandleComplete)
        self.symbolCallBack = symbolCallBack
        self.trade = trade
        self.params = params
        self.exchangeToken = ''
        self.tradingSymbol = ''
        # self.quantity = params.get(Constant.PARAMETER_QUANTITY)


    def update(self, trade, lastTradedPrice, volume):
        self.candleCreator.createCandle(lastTradedPrice, volume)
        if self.trade.startDate != None and self.trade.startDate.date() < self.top.info[Constant.KEY_DATE].date() and  self.trade.status != Constant.TRADE_STATUS.COMPLETED:
            trade.status = Constant.TRADE_STATUS.TIMED_OUT
            trade.exitDate = self.top.info[Constant.KEY_DATE]
            trade.exitPrice = lastTradedPrice
            trade.gain = trade.entryPrice - trade.exitPrice
            self.params[Constant.PARAMETER_QUANTITY] = self.quantity
            self.params[Constant.PARAMETER_TICK_DATA] = self.tickData
            self.symbolCallBack(Constant.STRATEGY_EVENT.TRADE_TIMEOUT, self.params, self)
            print("timeout ", trade.symbol.symbolName, " on ", trade.timeOutDate, " startDate ",
                  self.trade.startDate)
            return
        self.updateStrategy(trade, lastTradedPrice, volume)

    @abc.abstractmethod
    def updateStrategy(self, trade, lastTradedPrice, volume):
        print("Update base class")

    def onCandleComplete(self, candle):
        self.symbolCallBack(Constant.STRATEGY_EVENT.CANDLE_CREATED, candle, self)
        # print("Candle Created for symbol ", self.trade.symbol.symbol, " candle ", candle)
        if not self.trade.simulate:
            Common.LogAction("candleCreated," + str(candle) + "," +
                             self.trade.strategyName + "," + self.trade.symbol.symbolName)
        self.addNewTick(candle)
        self.onNewCandleCreated(candle)

    @abc.abstractmethod
    def onNewCandleCreated(self, candle):
        print("Need to Implement")

    def addNewTick(self, candle):
        self.topIndex = self.topIndex + 1
        self.tickData.append(Common.Tick(candle))
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

    def exportCSV(self, name, columns):
        name = name + '_' + self.trade.symbol.symbolName + '.csv'
        with open(name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(columns)
            for tick in self.tickData:
                row = []
                for c in columns:
                    try:
                        row.append(tick.info[c])
                    except:
                        row.append("Error_" + str(c))
                csvwriter.writerow(row)

    @abc.abstractmethod
    def exitStrategy(self, trade, currentPrice):
        print("Need to Implement")

    @abc.abstractmethod
    def enterStrategy(self, trade, currentPrice):
        print("Need to Implement")


class GannAnalysis(StrategyBaseClass):

    def updateStrategy(self, trade, currentPrice, volume):

        if trade.status == Constant.TRADE_STATUS.LOOKING_FOR_ENTRY:
            if currentPrice > trade.buyTriggerCall:

                # trade.entryTime = time.time()
                trade.takeProfit = Common.getNextGannLevel(
                    trade.buyTriggerCall + 1)
                trade.stopLoss = Common.getPreviousGannLevel(
                    trade.buyTriggerCall - 1)
                trade.entryPrice = currentPrice
                trade.type = Constant.TRADE_TYPE_CALL
                self.enterStrategy(trade, currentPrice)
                print("Buy ", trade.symbol.symbolName, "on ", str(datetime.datetime.now()), " for Price ",
                      currentPrice)
                print("TakeProfit ", trade.takeProfit,
                      " Stoploss ", trade.stopLoss)
                print("____________________________________________")

            if currentPrice < trade.buyTriggerPut:
                trade.takeProfit = Common.getPreviousGannLevel(
                    trade.buyTriggerPut - 1)
                trade.stopLoss = Common.getNextGannLevel(
                    trade.buyTriggerPut + 1)
                trade.entryPrice = currentPrice
                trade.type = Constant.TRADE_TYPE_PUT
                self.enterStrategy(trade, currentPrice)
                print("Buy ", trade.symbol.symbolName, "on ", str(datetime.datetime.now()), " for Price ",
                      currentPrice)
                print("TakeProfit ", trade.takeProfit,
                      " Stoploss ", trade.stopLoss)
                print("____________________________________________")


        elif trade.status == Constant.TRADE_STATUS.ENTERED:
            if (currentPrice > trade.takeProfit and trade.type == Constant.TRADE_TYPE_CALL) or (
                    currentPrice < trade.takeProfit and trade.type == Constant.TRADE_TYPE_PUT):

                self.exitStrategy(trade, currentPrice)
            if (currentPrice < trade.stopLoss and trade.type == Constant.TRADE_TYPE_CALL) or (
                    currentPrice > trade.stopLoss and trade.type == Constant.TRADE_TYPE_PUT):

                self.exitStrategy(trade, currentPrice)

            # if not trade.simulate and datetime.datetime.now() > Constant.EXIT_TIME :
            #     print(f"looking for Exit {trade.symbol.symbolName}")
            #     trade.status = Constant.TRADE_LOOKING_FOR_EXIT
        elif trade.status == Constant.TRADE_STATUS.LOOKING_FOR_EXIT:
            if trade.entryPrice > currentPrice:
                trade.exitPrice = currentPrice
                print(
                    f" Exiting trade {trade.symbol.symbolName} on {datetime.datetime.now()} for price {trade.exitPrice} gain {trade.exitPrice - trade.entryPrice}")
                Common.LogAction("ExitTrade, exit," + str(self.trade.exitPrice) + "," + str(
                    self.trade.gain) + "," + trade.strategyName + "," + str(self.trade.symbol.symbolName))
                trade.status = Constant.TRADE_STATUS.COMPLETED

    def onNewCandleCreated(self, candle):
        if self.trade.status == Constant.TRADE_STATUS.NOT_STARTED:
            self.trade.buyTriggerCall = Common.getNextGannLevel(
                candle[Constant.KEY_OPEN])
            self.trade.buyTriggerPut = Common.getPreviousGannLevel(
                candle[Constant.KEY_OPEN])
            self.trade.status = Constant.TRADE_STATUS.LOOKING_FOR_ENTRY
            if not self.trade.simulate:
                Common.LogAction("EnteringTrade, " + str(self.trade.buyTriggerCall) + "," + str(
                    self.trade.buyTriggerPut) + ",," + str(self.trade.symbol.symbolName))
            self.trade.startDate = self.top.info[Constant.KEY_DATE]
            print("Entering Trade for ", self.trade.symbol.symbolName,
                  " ", self.top.info[Constant.KEY_DATE])
        # print("Candle Created for symbol ",self.trade.symbol.symbol," candle ",candle)

    def enterStrategy(self, trade, currentPrice):
        trade.entryTime = datetime.datetime.now()
        trade.buyDate = self.top.info[Constant.KEY_DATE]
        if trade.simulate:
            trade.status = Constant.TRADE_STATUS.ENTERED
            return

        Common.LogAction(
            "Buying," + str(self.trade.entryPrice) + "," + str(self.trade.takeProfit) + "," + str(
                self.trade.stopLoss) + "," + trade.strategyName + "," + str(
                self.trade.symbol.symbolName) + "," +
            self.trade.type + "," + str(Common.getNextStrikePrice(self.trade.entryPrice)) + "," + str(
                Common.getSymbolExchangeCode(
                    self.trade.symbol.symbolName, Common.getNextStrikePrice(self.trade.entryPrice),
                    trade.type,
                    None if self.trade.symbol.assetType == 'EQUITY' else datetime.datetime.now().date())))
        if self.trade.symbol.assetType == AssetTypeEnum.EQUITY:
            o = Common.getOptionForStock(
                self.trade.symbol.optionSymbol, Common.getNextStrikePrice(self.trade.entryPrice), trade.type)
        elif self.trade.symbol.assetType == AssetTypeEnum.INDEX:
            o = Common.getOptionForIndex(
                self.trade.symbol.optionSymbol, Common.getNextStrikePrice(self.trade.entryPrice), trade.type)
        self.trade.tradingSymbol = o['tradingsymbol']
        self.trade.exchangeToken = o['exchangetoken']
        self.trade.quantity = int(o['lotsize'])*self.quantity #int(o['lotsize']) * int(self.trade.quantity)
        if trade.symbol.buy(self.trade.tradingSymbol,
                         self.trade.exchangeToken, self.trade.quantity, exchange=ExchangeEnum.NFO):
            trade.status = Constant.TRADE_STATUS.ENTERED

    def exitStrategy(self, trade, currentPrice):
        trade.exitPrice = currentPrice
        trade.gain = (currentPrice - trade.entryPrice)
        trade.exitDate = self.top.info[Constant.KEY_DATE]

        if trade.simulate:
            trade.status = Constant.TRADE_STATUS.COMPLETED
            self.symbolCallBack(Constant.STRATEGY_EVENT.TRADE_COMPLETED, self.params, self)
            return

        if trade.gain > 0:
            Common.LogAction("SELL,PROFIT," + str(self.trade.exitPrice) + "," + str(
                self.trade.gain) + "," + trade.strategyName + "," + str(self.trade.symbol.symbolName))
        else:
            Common.LogAction("SELL,LOSE," + str(self.trade.exitPrice) + "," + str(
                self.trade.gain) + "," + trade.strategyName + "," + str(self.trade.symbol.symbolName))
        if trade.symbol.sell(self.trade.tradingSymbol,
                          self.trade.exchangeToken, self.trade.quantity,exchange=ExchangeEnum.NFO):
            trade.status = Constant.TRADE_STATUS.COMPLETED
        self.symbolCallBack(Constant.STRATEGY_EVENT.TRADE_COMPLETED,self.params, self)


class MACrossover(StrategyBaseClass):

    def updateStrategy(self, trade, currentPrice, volume):
        if trade.status == Constant.TRADE_STATUS.LOOKING_FOR_ENTRY:
            if currentPrice > trade.buyTriggerCall:
                self.enterStrategy(trade, currentPrice)

        elif trade.status == Constant.TRADE_STATUS.ENTERED:
            if currentPrice > trade.takeProfit:
                self.exitStrategy(trade, currentPrice)
                print("Profit Sell ", trade.symbol.symbolName, "on ", self.top.info[Constant.KEY_DATE], " for price ",
                      currentPrice, " with Profit ", (currentPrice - trade.entryPrice))
                print("               *************************                 ")


            elif currentPrice < trade.stopLoss:
                self.exitStrategy(trade, currentPrice)
                print("Loss sell ", trade.symbol.symbolName, "on ", self.top.info[Constant.KEY_DATE], " for price ",
                      currentPrice, " with loss ", (trade.entryPrice - currentPrice))
                print("               *************************                 ")

    def onNewCandleCreated(self, candle):
        if self.trade.status == Constant.TRADE_STATUS.NOT_STARTED and( self.trade.simulate or datetime.datetime.now() > self.trade.startTime):
            if self.topIndex < 2:
                return
            last = self.tickData[self.trade.symbol.topIndex - 1]
            if self.top.info[Constant.KEY_CLOSE] > self.top.info[Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] and \
                    last.info[Constant.KEY_CLOSE] < last.info[Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] and \
                    self.top.info[Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] >= self.top.info[
                Constant.KEY_MOVING_AVERAGE_MEDUIM_CLOSE] and \
                    self.top.info[Constant.KEY_RSI] >= 55:
                self.trade.status = Constant.TRADE_STATUS.LOOKING_FOR_ENTRY
                self.trade.buyTriggerCall = self.top.info[Constant.KEY_HIGH]
                self.trade.stopLoss = Common.getLowestValue(self)
                self.trade.takeProfit = self.trade.buyTriggerCall + \
                                        abs(self.trade.buyTriggerCall - self.trade.stopLoss)
                self.trade.startDate = self.top.info[Constant.KEY_DATE]
                print("")
                print("")
                print("")
                print("")
                print("")
                print("          *****************************       ")

                print("Entering Trade for ", self.trade.symbol.symbolName,
                      " ", self.top.info[Constant.KEY_DATE])

    def enterStrategy(self, trade, currentPrice):
        trade.status = Constant.TRADE_STATUS.ENTERED
        trade.entryPrice = currentPrice
        trade.buyDate = self.top.info[Constant.KEY_DATE]
        print("MAC Buy ", trade.symbol.symbolName, "on ", self.top.info[Constant.KEY_DATE], " for Price ",
              currentPrice)
        print("TakeProfit ", trade.takeProfit,
              " Stoploss ", trade.stopLoss)
        print("____________________________________________")

    def exitStrategy(self, trade, currentPrice):
        trade.status = Constant.TRADE_STATUS.COMPLETED
        trade.exitPrice = currentPrice
        trade.gain = (trade.exitPrice - trade.entryPrice)

        trade.exitDate = self.top.info[Constant.KEY_DATE]
        self.params[Constant.PARAMETER_TICK_DATA] = self.tickData
        # self.params[Constant.PARAMETER_TICK_DATA] = self.tickData
        self.symbolCallBack(Constant.STRATEGY_EVENT.TRADE_COMPLETED, self.params, self)


def init():
    # Common.strategyDict[Constant.STRATEGY_GANN_ANALYSIS] = GannAnalysis()
    # Common.strategyDict[Constant.STRATEGY_MA_CROSSOVER_UP] = MACrossover()
    print("Init Strategy")
