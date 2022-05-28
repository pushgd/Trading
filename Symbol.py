from Common import Tick
import Constant
import analyze
import strategy
import csv


class Symbol:
    def __init__(self, name, symbol, riskfactor=2):
        print('symbol')
        self.name = name
        self.symbol = symbol
        self.tickData = []
        self.riskFactor = riskfactor
        self.topIndex = -1

    def update(self, data):
        self.topIndex = self.topIndex+1
        self.tickData.append(Tick(data))
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
