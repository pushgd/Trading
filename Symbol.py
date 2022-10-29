import API
import Common
import Constant
import analyze
import csv
import time
import datetime
import DBHelper
import strategy
from strategy import GannAnalysis, MACrossover
import playsound
from constants.intraday_interval import IntradayIntervalEnum
from constants.order_type import OrderTypeEnum
from constants.exchange import ExchangeEnum
import json
import os
import storage
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
        self.lastUpdatedTime = None
        if not os.path.isfile(f"storage/symbol/{symbolName}.json"):
            with open(f"storage/symbol/{symbolName}.json", 'w') as f:
                print("Storage file not Exist creating ")
                json.dump({'symbolName':self.symbolName},f)





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
        trade = Common.Trade(self)
        trade.strategyName = strategy
        if strategy == Constant.STRATEGY_GANN_ANALYSIS:
            trade.strategy = GannAnalysis(self.OnStrategyEvent, trade,params=params)
        elif strategy == Constant.STRATEGY_MA_CROSSOVER_UP:

            trade.strategy = MACrossover(self.OnStrategyEvent, trade, params=params)

            if len(list(filter(lambda t: t.strategy == Constant.STRATEGY_MA_CROSSOVER_UP,self.tradeList))) == 0:  #check if there is any old trade for MAC
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
                trade.strategy.tickData = list(params[Constant.PARAMETER_TICK_DATA])
                trade.strategy.topIndex = len(trade.strategy.tickData)-1

        print("Strategy set to ", strategy," for ",self.symbolName)
        self.tradeList.append(trade)
        storage.setTradeInfo(self.symbolName,trade)
        return trade

    def onNewData(self, lastTradedPrice, volume):
        if self.lastTradedPrice != lastTradedPrice:
            self.lastUpdatedTime = datetime.datetime.now().time()
        self.lastTradedPrice = lastTradedPrice
        # self.createCandle(lastTradedPrice, volume)
        for t in self.tradeList:
            if not (t.status == Constant.TRADE_STATUS.COMPLETED or t.status == Constant.TRADE_STATUS.TIMED_OUT):
                t.strategy.update(t, lastTradedPrice, volume)

    def onCandleComplete(self, data):
        DBHelper.inertIntoTick(data[Constant.KEY_OPEN], data[Constant.KEY_HIGH], data[Constant.KEY_CLOSE],
                               data[Constant.KEY_LOW], data[Constant.KEY_VOLUME], self.symbolName,
                               data[Constant.KEY_DATE])
        # self.addNewTick(data)

    def OnStrategyEvent(self, event, params, strategy):
        if event == Constant.STRATEGY_EVENT.CANDLE_CREATED:
            self.onCandleComplete(params)
        if event == Constant.STRATEGY_EVENT.TRADE_COMPLETED or event == Constant.STRATEGY_EVENT.TRADE_TIMEOUT:
            self.setStrategy(strategy.trade.strategyName,params=params).simulate = self.tradeList[-1].simulate
            try:
                storage.setTradeInfo(self.symbolName,strategy.trade)
            except Exception as e:
                print(f"Error saving trade Info {self.symbolName} {e}")

    def exitTrade(self, ID):
        for t in self.tradeList:
            if t.ID == ID:
                t.status = Constant.TRADE_STATUS.FORCE_EXIT
                t.strategy.exitStrategy(t,self.lastTradedPrice)
                print("Exiting trade ", t.ID, " for symbol ", self.name)

    def buy(self, tradingSymbol, exchangeToken,quantity, limitPrice=0,exchange = ExchangeEnum.NSE ):
        try:
            r = API.placeOrder(tradingSymbol,  exchange, OrderTypeEnum.MARKET,
                               int(quantity), exchangeToken, limitPrice)
            if r == None:
                return False
            print("Purchase Completed")
            Common.LogAction(
                f"PurchaseCompleted,{tradingSymbol},{exchangeToken},{exchange},{OrderTypeEnum.MARKET},{limitPrice},{quantity},{r}")
            Common.playSound("purchase.wav")

            return True
        except Exception as e:
            print("Error Buying")
            print(str(e))
            Common.LogAction(
                f"PurchaseFailed,{tradingSymbol},{exchangeToken},{exchange},{OrderTypeEnum.MARKET},{limitPrice}")
            return False


    def sell(self, tradingSymbol, exchangeToken, quantity, limitPrice=0,exchange = ExchangeEnum.NSE):
        try:
            r = API.sellPosition(tradingSymbol, exchange, OrderTypeEnum.MARKET,
                                 int(quantity), exchangeToken, limitPrice)
            if r == None:
                return False
            print("sell Completed")
            Common.LogAction(
                f"SellCompleted,{tradingSymbol},{exchangeToken},{exchange},{OrderTypeEnum.MARKET},{limitPrice},{quantity},{r}")
            print(r)
            Common.playSound("sell.wav")
            return True
        except Exception as e:
            print("Error selling ", str(e))
            return False



    def gethHistoricalData(self, timeInterval, tillDateYear, tillDateMonth, tillDateDay):
        response = API.getHistoricalData(timeInterval, self.assetType, self.exchangeToken, self.exchange,
                                         tillDateYear + "-" + tillDateMonth + "-" + tillDateDay)
        return response

    # def getIntradayChart(self,timeInterval,tillDateYear,tillDateMonth,tillDateDay):
    #     API.getIntradayChart(timeInterval, self.assetType, self.exchangeToken, self.exchange,
    #                                      tillDateYear + "-" + tillDateMonth + "-" + tillDateDay)

    def initStrategy(self):
        if storage.isSymbolInfoExist(self.symbolName,Constant.STRATEGY_GANN_ANALYSIS):
            self.setStrategy(Constant.STRATEGY_GANN_ANALYSIS,storage.getSymbolInfo(self.symbolName,Constant.STRATEGY_GANN_ANALYSIS))
        if storage.isSymbolInfoExist(self.symbolName,Constant.STRATEGY_MA_CROSSOVER_UP):
            self.setStrategy(Constant.STRATEGY_MA_CROSSOVER_UP,storage.getSymbolInfo(self.symbolName,Constant.STRATEGY_MA_CROSSOVER_UP))