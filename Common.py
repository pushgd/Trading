import Constant
import math
import time
SymbolDict = {}
watchlist = []
strategyDict={}

localFile = False


def getNextGannLevel(n):
    return math.pow(math.ceil(math.sqrt(n)*4)/4,2)

def getPreviousGannLevel(n):
    return math.pow(math.floor(math.sqrt(n)*4)/4,2)


def isUpwardPattern(t):
    return ((t.isPattern(Constant.HARAMI) and t.isBull())
            or (t.isPattern(Constant.ENGULFING) and t.isBull())
            or (t.isPattern(Constant.ENGULFING) and t.isBull())
            or t.isPattern(Constant.PIERCING)
            or t.isPattern(Constant.INVERTED_PIERCING)
            or t.isPattern(Constant.MORNING_STAR))


def getLowestValue(symbol):
    t = symbol.tickData[symbol.topIndex-1]
    if(t.isPattern(Constant.MORNING_STAR) or t.isPattern(Constant.EVENING_STAR)):
        l = symbol.tickData[symbol.topIndex-4:symbol.topIndex-1]
    else:
        l = symbol.tickData[symbol.topIndex-3:symbol.topIndex-1]
    min = 99999999
    for i in l:
        if i.info[Constant.KEY_LOW] < min:
            min = i.info[Constant.KEY_LOW]
    return min


class Trade:
    def __init__(self, symbol):
        self.status = Constant.TRADE_NOT_STARTED
        self.entryPrice = 0
        self.entryTime = 0
        self.exitPrice = 0
        self.exitTime = 0
        self.buyTrigger = -1
        self.stopLoss = 0
        self.takeProfit = 0
        self.tick = None
        self.strategy = None
        self.symbol = symbol
        self.ID = time.time()
        self.strategyName = None


class Tick:
    def __init__(self, data):
        self.info = {Constant.KEY_DATE: data['date']}
        high = self.info[Constant.KEY_HIGH] = float(data['high'])
        low = self.info[Constant.KEY_LOW] = float(data['low'])
        open = self.info[Constant.KEY_OPEN] = float(data['open'])
        close = self.info[Constant.KEY_CLOSE] = float(data['close'])
        self.info[Constant.KEY_VOLUME] = float(data['volume'])
        self.info[Constant.KEY_BODY_LENGTH] = abs(open - close)
        self.info[Constant.KEY_LENGTH] = abs(high - low)
        self.info[Constant.KEY_TYPE] = Constant.BULL if close > open else Constant.BEAR

        self.info[Constant.KEY_MEAN] = (high + low)/2.0
        self.info[Constant.KEY_BODY_MEAN] = (open + close)/2.0
        self.info[Constant.KEY_GAIN] = 0
        self.info[Constant.KEY_LOSS] = 0
        self.info[Constant.KEY_AVERAGE_GAIN] = 0
        self.info[Constant.KEY_AVERAGE_LOSS] = 0
        self.info[Constant.KEY_PATTERN] = []
        self.info[Constant.KEY_STRATEGY] = []

    def __str__(self):

        s = "Date "+self.info[Constant.KEY_DATE] + \
            "  " + self.info[Constant.KEY_TYPE]+"\n"
        s = s+"Open "+str(self.info[Constant.KEY_OPEN]) + " Close " + \
            str(self.info[Constant.KEY_CLOSE])+"\n"
        s = s + "High "+str(self.info[Constant.KEY_HIGH]) + \
            " Low "+str(self.info[Constant.KEY_LOW])
        s = s + "\n--------------------------------\n"
        return s

    def isPattern(self, pattern):
        return pattern in self.info[Constant.KEY_PATTERN]

    def candleBodyInsideLength(self, other):
        return other.tickInfo[Constant.KEY_OPEN] <= self.info[Constant.KEY_HIGH] and other.tickInfo[Constant.KEY_OPEN] >= self.info[Constant.KEY_LOW] and other.tickInfo[Constant.KEY_CLOSE] <= self.info[Constant.KEY_HIGH] and other.tickInfo[Constant.KEY_CLOSE] >= self.info[Constant.KEY_LOW]

    def isInsideBody(self, value):
        if(self.isBull()):
            return value > self.info[Constant.KEY_OPEN] and value < self.info[Constant.KEY_CLOSE]
        return value < self.info[Constant.KEY_OPEN] and value > self.info[Constant.KEY_CLOSE]

    def isInsideLength(self, value):
        return value > self.info[Constant.KEY_LOW] and value < self.info[Constant.KEY_HIGH]

    def isBull(self):
        return self.info[Constant.KEY_TYPE] == Constant.BULL

    def isBear(self):
        return self.info[Constant.KEY_TYPE] == Constant.BEAR

    def serialize(self):
        return self.info
