import Common
import Constant
import analyze
import csv
import time
import datetime
import DBHelper


class Symbol:
    def __init__(self, name, symbol, scripCode, riskfactor=1):
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
        self.strategy =[]
        self.lastTradedPrice = 0
        self.tempCandleData = []
        self.high = -1
        self.low = 99999
        self.parameters = {}

    def update(self, data):
        self.addNewTick(data)
        self.checkStartegy()


    def old_updateTrade(self, price):
        for trade in self.tradeList:
            if(trade.status == Constant.TRADE_NOT_STARTED):
                if price > trade.buyTrigger:
                    trade.status = Constant.TRADE_ENTRY
                    print("Buy for Trade at " +
                          str(trade.tick.info[Constant.KEY_DATE])+" at Price "+str(price)+" for BuyTrigger "+str(trade.buyTrigger)+" on "+self.top.info[Constant.KEY_DATE])
            if(trade.status == Constant.TRADE_ENTRY):
                if price > trade.takeProfit:
                    trade.status = Constant.TRADE_COMPLETED
                    print("Sell for Trade at " +
                          str(trade.tick.info[Constant.KEY_DATE])+" at Price "+str(price)+" for takeProfit "+str(trade.takeProfit)+" on "+self.top.info[Constant.KEY_DATE])
            if(trade.status != Constant.TRADE_COMPLETED):
                if price < trade.stopLoss:
                    trade.status = Constant.TRADE_COMPLETED
                    print("Exit for Trade at " +
                          str(trade.tick.info[Constant.KEY_DATE])+" at Price "+str(price)+" for stoploss "+str(trade.stopLoss)+" on "+self.top.info[Constant.KEY_DATE])

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

    def old_addToWatchList(self, strategy,data = None):
        self.top.info[Constant.KEY_STRATEGY].append(strategy)
        buyTrigger = self.top.info[Constant.KEY_HIGH]
        stopLoss = Common.getLowestValue(self)
        takeProfit = buyTrigger + abs(buyTrigger-stopLoss)*self.riskFactor
        self.tradeList.append(Common.Trade())

    def addNewTick(self, data):
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


    def exitTrade(self,trade,lastTradedPrice):
        trade.exitPrice = lastTradedPrice
        trade.exitTime = datetime.datetime.now()
        trade.status = Constant.TRADE_COMPLETED
        print("Exiting Trade")
         
    
    def enterTrade(self,trade):
        trade.entryPrice = self.top.info[Constant.KEY_CLOSE]
        trade.entryTime = self.top.info[Constant.KEY_DATE]
        trade.strategy.onEnter(trade)
        trade.status = Constant.TRADE_ENTRY
        
        print("Entering Trade")

    def setStrategy(self,strategy):
        self.strategy.append(strategy)
        trade = Common.Trade(self)
        trade.strategy =  Common.strategyDict[strategy]
        self.tradeList.append(trade)
    
    def checkStartegy(self):
        for t in self.tradeList:
            if t.status == Constant.TRADE_LOOKING_FOR_ENTRY or t.status == Constant.TRADE_NOT_STARTED:
                if t.strategy.checkForEntry(t) == 1:
                    self.enterTrade(t)

    def onNewData(self,lastTradedPrice,volume):
        self.lastTradedPrice = lastTradedPrice
        self.createCandle(lastTradedPrice,volume)
        for t in self.tradeList:
            if t.status == Constant.TRADE_ENTRY :
                if t.strategy.checkForExit(t) == 1:
                    self.exitTrade(t,lastTradedPrice)


    def onCandleComplete(self, data):
        DBHelper.inertIntoTick(data[Constant.KEY_OPEN], data[Constant.KEY_HIGH], data[Constant.KEY_CLOSE],
                           data[Constant.KEY_LOW], data[Constant.KEY_VOLUME], self.symbol, data[Constant.KEY_DATE])
        self.update(data)


    def createCandle(self,price, volume):

        self.lastDataReceiveTime = time.time()
        self.tempCandleData.append(price)
        if self.high < price:
            self.high = price

        if self.low > price:
            self.low = price
        timeelapsed = time.time()-self.lastDataReceiveTime
    # print("Time since last candle Createed "+str(timeelapsed) +
    #       " last Cnadle Created "+str(lastDataReceiveTime[symbol])+"  "+str(len(tempCandleData[symbol])))
        if timeelapsed > Constant.CANDLE_CRATION_TIME:
            self.lastDataReceiveTime= time.time()
            candle = {}
            candle[Constant.KEY_HIGH] = self.high
            candle[Constant.KEY_LOW] = self.low
            candle[Constant.KEY_CLOSE] = self.tempCandleData[len(self.tempCandleData)-1]
            candle[Constant.KEY_OPEN] = self.tempCandleData[0]
            candle[Constant.KEY_DATE] = datetime.datetime.now()
            candle[Constant.KEY_VOLUME] = volume
            self.onCandleComplete( candle)
            self.high= -1
            self.low = 999999
            self.tempCandleData.clear()

