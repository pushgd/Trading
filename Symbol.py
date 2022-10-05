import API
import Common
import Constant
import analyze
import csv
import time
import datetime
import DBHelper
from strategy import GannAnalysis, MACrossover
import playsound
from constants.intraday_interval import IntradayIntervalEnum
import json

# playsound.playsound("purchase.mp3")


class Symbol:
    def __init__(self, symbolName):
        self.top = None
        self.symbolName = symbolName
        self.tradingSymbol = ""
        self.exchangeToken = ""
        self.tickData = []
        self.riskFactor = ""
        self.topIndex = -1
        self.watchList = []
        self.tradeList = []
        self.exchangeType = 'E'
        self.data = {}
        self.strategy = []
        self.lastTradedPrice = 0
        self.tempCandleData = []
        self.high = -1
        self.low = 99999
        self.parameters = {}
        self.isActive = True
        self.localTick = 0
        self.quantity = 1
        self.assetType = ''
        self.optionSymbol = ''
        self.exchange = ''

    # def __init__(self, symbolName, tradingSymbol, exchangeToken, riskfactor=1):
    #     self.top = None
    #     self.symbolName = symbolName
    #     self.tradingSymbol = tradingSymbol
    #     self.exchangeToken = exchangeToken
    #     self.tickData = []
    #     self.riskFactor = riskfactor
    #     self.topIndex = -1
    #     self.watchList = []
    #     self.tradeList = []
    #     self.exchangeType = 'E'
    #     self.data = {}
    #     self.strategy = []
    #     self.lastTradedPrice = 0
    #     self.tempCandleData = []
    #     self.high = -1
    #     self.low = 99999
    #     self.parameters = {}
    #     self.isActive = True
    #     self.localTick = 0
    #     self.quantity = 1
    #     self.assetType = ''

    def update(self, data):
        # self.addNewTick(data)
        self.checkStartegy(data)

    def activate(self):
        self.isActive = True

    def deactivate(self):
        self.isActive = False

    def exportCSV(self, name, *columns):
        name = name + '_' + self.symbolName + '.csv'
        with open(name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(columns)
            for tick in self.tickData:
                row = []
                for c in columns:
                    row.append(tick.info[c])
                csvwriter.writerow(row)

    def setStrategy(self, strategy,params=None,historicalData =None):
        self.strategy.append(strategy)
        trade = Common.Trade(self)
        trade.strategyName = strategy
        # trade.strategy = Common.strategyDict[strategy]
        if strategy == Constant.STRATEGY_GANN_ANALYSIS:
            s = GannAnalysis(self.OnStrategyEvent, trade)
            trade.strategy = GannAnalysis(self.OnStrategyEvent, trade,params=params)
        elif strategy == Constant.STRATEGY_MA_CROSSOVER_UP:

            trade.strategy = MACrossover(self.OnStrategyEvent, trade, params=params)

            if len(self.tradeList) == 0:
                print("Get historical data for ",self.symbolName)
                tillDate = Common.getTillDate()
                if historicalData == None:
                    historicalData = json.loads(
                    self.gethHistoricalData(IntradayIntervalEnum.M5, str(tillDate.year), str(tillDate.month),str(tillDate.day)))
                    data = historicalData['data']
                else:
                    data = historicalData
                print("Candles received ",len(data))
                for candle in data:
                    c = {
                              Constant.KEY_OPEN: candle[1],
                              Constant.KEY_HIGH: candle[2],
                              Constant.KEY_LOW: candle[3],
                              Constant.KEY_CLOSE: candle[4],
                              Constant.KEY_DATE: datetime.datetime.strptime(candle[0], "%Y-%m-%d %H:%M:%S"),
                              Constant.KEY_VOLUME: candle[5]}
                    trade.strategy.addNewTick(c)
                print("Indicators calculated for ", self.symbolName)
            else:
                trade.strategy.tickData = list(params)
                trade.strategy.topIndex = len(trade.strategy.tickData)-1
                # trade.strategy.exportCSV("indicators",list(trade.strategy.tickData[50].info.keys()))


            # s = MACrossover(self.OnStrategyEvent, trade)
            # trade.strategy = MACrossover(self.OnStrategyEvent, trade,params=params)
        print("Strategy set to ", strategy," for ",self.symbolName)
        self.tradeList.append(trade)
        return trade

    def onNewData(self, lastTradedPrice, volume):
        self.lastTradedPrice = lastTradedPrice
        # self.createCandle(lastTradedPrice, volume)
        for t in self.tradeList:
            if t.status != Constant.TRADE_COMPLETED:
                t.strategy.update(t, lastTradedPrice, volume)

    def onCandleComplete(self, data):
        DBHelper.inertIntoTick(data[Constant.KEY_OPEN], data[Constant.KEY_HIGH], data[Constant.KEY_CLOSE],
                               data[Constant.KEY_LOW], data[Constant.KEY_VOLUME], self.symbolName,
                               data[Constant.KEY_DATE])
        # self.addNewTick(data)

    def OnStrategyEvent(self, event, params, strategy):
        if event == Constant.EVENT_CANDLE_CREATED:
            self.onCandleComplete(params)
        if event == Constant.EVENT_TRADE_COMPLETED or event == Constant.EVENT_TRADE_TIMEOUT:
            self.setStrategy(strategy.trade.strategyName,params=params)

    def exitTrade(self, ID):
        for t in self.tradeList:
            if t.ID == ID:
                t.status = Constant.TRADE_FORCE_EXIT
                print("Exiting trade ", t.ID, " for symbol ", self.name)

    def buy(self, tradingSymbol, exchangeToken, exchange, orderType, quantity, limitPrice=0):
        try:
            r = API.placeOrder(tradingSymbol, exchange, orderType,
                               quantity, exchangeToken, limitPrice)
            print("Purchase Completed")
            Common.LogAction(
                f"PurchaseCompleted,{tradingSymbol},{exchangeToken},{exchange},{orderType},{limitPrice},{r}")
        except:
            print("Error Buying")
        try:
            playsound.playsound("purchase.mp3")
        except Exception as e:
            print("Error playing sound ", str(e))

    def sell(self, tradingSymbol, exchangeToken, exchange, orderType, quantity, limitPrice=0):
        if Common.simulate:
            return
        try:
            r = API.sellPosition(tradingSymbol, exchange, orderType,
                                 quantity, exchangeToken, limitPrice)
            print("sell Completed")
            Common.LogAction(
                f"SellCompleted,{tradingSymbol},{exchangeToken},{exchange},{orderType},{limitPrice},{r}")
            print(r)
        except Exception as e:
            print("Error selling ", str(e))
        try:
            playsound.playsound("sell.mp3")
        except Exception as e:
            print("Error playing sound ", str(e))

    def gethHistoricalData(self, timeInterval, tillDateYear, tillDateMonth, tillDateDay):
        response = API.getHistoricalData(timeInterval, self.assetType, self.exchangeToken, self.exchange,
                                         tillDateYear + "-" + tillDateMonth + "-" + tillDateDay)
        return response

    def getIntradayChart(self,timeInterval,tillDateYear,tillDateMonth,tillDateDay):
        API.getIntradayChart(timeInterval, self.assetType, self.exchangeToken, self.exchange,
                                         tillDateYear + "-" + tillDateMonth + "-" + tillDateDay)