import Common
import Constant
import analyze
import strategy
import csv


class Symbol:
    def __init__(self, name, symbol, riskfactor=1):
        self.name = name
        self.symbol = symbol
        self.tickData = []
        self.riskFactor = riskfactor
        self.topIndex = -1
        self.watchList = []
        self.tradeList = []

    def update(self, data):
        self.topIndex = self.topIndex+1
        self.tickData.append(Common.Tick(data))
        self.top = self.tickData[self.topIndex]
        if(self.topIndex > 0):
            if(self.top.info[Constant.KEY_CLOSE] > self.tickData[self.topIndex-1].info[Constant.KEY_CLOSE]):
                self.top.info[Constant.KEY_GAIN] = self.top.info[Constant.KEY_CLOSE] - \
                    self.tickData[self.topIndex-1].info[Constant.KEY_CLOSE]
                self.top.info[Constant.KEY_LOSS] = 0
            else:
                self.top.info[Constant.KEY_LOSS] = abs(
                    self.top.info[Constant.KEY_CLOSE] - self.tickData[self.topIndex-1].info[Constant.KEY_CLOSE])
                self.top.info[Constant.KEY_GAIN] = 0

        analyze.update(self)
        strategy.update(self)

    def updateTrade(self, price):
        for trade in self.tradeList:
            if(trade.status == Constant.TRADE_NOT_STARTED):
                if price > trade.buyTrigger:
                    trade.status = Constant.TRADE_ENTRY
                    print("Buy for Trade at " +
                          trade.tick.info[Constant.KEY_DATE]+" at Price "+str(price)+" for BuyTrigger "+str(trade.buyTrigger)+" on "+self.top.info[Constant.KEY_DATE])
            if(trade.status == Constant.TRADE_ENTRY):
                if price > trade.takeProfit:
                    trade.status = Constant.TRADE_COMPLETED
                    print("Sell for Trade at " +
                          trade.tick.info[Constant.KEY_DATE]+" at Price "+str(price)+" for takeProfit "+str(trade.takeProfit)+" on "+self.top.info[Constant.KEY_DATE])
            if(trade.status != Constant.TRADE_COMPLETED):
                if price < trade.stopLoss:
                    trade.status = Constant.TRADE_COMPLETED
                    print("Exit for Trade at " +
                          trade.tick.info[Constant.KEY_DATE]+" at Price "+str(price)+" for stoploss "+str(trade.stopLoss)+" on "+self.top.info[Constant.KEY_DATE])

    def exportCSV(self, name, *columns):
        name = name+'_'+self.symbol+'.csv'
        with open(name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(columns)
            for tick in self.tickData:
                row = []
                for c in columns:
                    row.append(tick.info[c])
                csvwriter.writerow(row)

    def addToWatchList(self, strategy):
        self.top.info[Constant.KEY_STRATEGY].append(strategy)
        buyTrigger = self.top.info[Constant.KEY_HIGH]
        stopLoss = Common.getLowestValue(self)
        takeProfit = buyTrigger + abs(buyTrigger-stopLoss)*self.riskFactor
        self.tradeList.append(Common.Trade(
            buyTrigger, stopLoss, takeProfit, self.top))
