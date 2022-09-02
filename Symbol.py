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
# playsound.playsound("purchase.mp3")


class Symbol:
    def __init__(self, symbolName, tradingSymbol, exchangeToken, riskfactor=1):
        self.top = None
        self.symbolName = symbolName
        self.tradingSymbol = tradingSymbol
        self.exchangeToken = exchangeToken
        self.tickData = []
        self.riskFactor = riskfactor
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

    def setStrategy(self, strategy):
        self.strategy.append(strategy)
        trade = Common.Trade(self)
        trade.strategyName = strategy
        # trade.strategy = Common.strategyDict[strategy]
        if strategy == Constant.STRATEGY_GANN_ANALYSIS:
            s = GannAnalysis(self.OnStrategyEvent, trade)
            trade.strategy = GannAnalysis(self.OnStrategyEvent, trade)
        elif strategy == Constant.STRATEGY_MA_CROSSOVER_UP:
            s = MACrossover(self.OnStrategyEvent, trade)
            trade.strategy = MACrossover(self.OnStrategyEvent, trade)

        self.tradeList.append(trade)

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

    def OnStrategyEvent(self, event, data, strategy):
        if event == Constant.EVENT_CANDLE_CREATED:
            self.onCandleComplete(data)
        if event == Constant.EVENT_TRADE_COMPLETED:
            self.setStrategy(strategy.trade.strategyName)

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
