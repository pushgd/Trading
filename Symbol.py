import Common
import Constant
import analyze
import csv
import time
import datetime
import DBHelper
from strategy import GannAnalysis, MACrossover


class Symbol:
    def __init__(self, name, symbol, scripCode, riskfactor=1):
        self.top = None
        self.name = name
        self.symbol = symbol
        self.scripCode = scripCode
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

    def update(self, data):
        # self.addNewTick(data)
        self.checkStartegy(data)

    def activate(self):
        self.isActive = True

    def deactivate(self):
        self.isActive = False

    def exportCSV(self, name, *columns):
        name = name + '_' + self.symbol + '.csv'
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
        elif strategy == Constant.STRATEGY_MA_CROSSOVER_UP:
            s = MACrossover(self.OnStrategyEvent, trade)
        trade.strategy = GannAnalysis(self.OnStrategyEvent, trade)
        self.tradeList.append(trade)

    def onNewData(self, lastTradedPrice, volume):
        self.lastTradedPrice = lastTradedPrice
        # self.createCandle(lastTradedPrice, volume)
        for t in self.tradeList:
            if t.status != Constant.TRADE_COMPLETED:
                t.strategy.update(t,lastTradedPrice,volume)

    def onCandleComplete(self, data):
        DBHelper.inertIntoTick(data[Constant.KEY_OPEN], data[Constant.KEY_HIGH], data[Constant.KEY_CLOSE],
                               data[Constant.KEY_LOW], data[Constant.KEY_VOLUME], self.symbol, data[Constant.KEY_DATE])
        # self.addNewTick(data)
    def OnStrategyEvent(self, event, data, strategy):
        if event == Constant.EVENT_CANDLE_CREATED:
            self.onCandleComplete(data)
        if event == Constant.EVENT_TRADE_COMPLETED:
            self.setStrategy(strategy.trade.strategyName)





