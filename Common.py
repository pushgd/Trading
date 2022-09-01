import Constant
import math
import time
import datetime
import csv
SymbolDict = {}
watchlist = []
strategyDict={}

localFile = False

def LogDataReceived(msg):
    Constant.LOGGER.dataReceived(msg)

def LogAction(msg):
    Constant.LOGGER.action(msg)
    print(str(datetime.datetime.now())+" "+msg)


def getNextGannLevel(n):
    return math.pow(math.ceil(math.sqrt(n)*4)/4,2)

def getPreviousGannLevel(n):
    return math.pow(math.floor(math.sqrt(n)*4)/4,2)

def getNextStrikePrice(price):
    return int((price/100))*100+100
def getPreviousStrikePrice(price):
    return int((price/100))*100-100

def getSymbolExchangeCode(symbol,strikePrice,option):
    # strikePrice = str(int((price/100))*100+100)

    daysTOAdd = 0
    match datetime.datetime.now().weekday():
        case 0:
            daysTOAdd = 3
        case 1:
            daysTOAdd = 2
        case 2:
            daysTOAdd = 1
        case 3:
            daysTOAdd = 7
        case 4:
            daysTOAdd = 6
    expirayDate =datetime.datetime.now()+ datetime.timedelta(days = daysTOAdd) # 4 for friday
    print(f"strike price {strikePrice} symbol {symbol} option {option} expiry {expirayDate}")
    # expirayDate = datetime.datetime.strptime(str(expirayDate.day)+"-"+str(expirayDate.month)+"-"+str(expirayDate.year), "%d-%m-%Y")
    with open('instruments.csv') as csvfile:
        fileReader = csv.DictReader(csvfile)
        for row in fileReader:
            if row['assettype'] == "OPTIDX":
                try:
                    d =datetime.datetime.strptime(row['expiry'], "%d-%b-%y")
                    # if row['symbolname'] == symbol and d.date() == expirayDate.date() and int(row['strikeprice']) == strikePrice:
                    #     print(f" strike price {row['strikeprice']}  type {row['optiontype']}")
                    if row['symbolname'] == symbol and int(row['strikeprice']) == strikePrice and row['optiontype'] == option and  d.date() == expirayDate.date():
                        return {'exchangetoken':row['exchangetoken'],'tradingsymbol':row['tradingsymbol']}
                except:
                    pass


def isUpwardPattern(t):
    return ((t.isPattern(Constant.HARAMI) and t.isBull())
            or (t.isPattern(Constant.ENGULFING) and t.isBull())
            or (t.isPattern(Constant.ENGULFING) and t.isBull())
            or t.isPattern(Constant.PIERCING)
            or t.isPattern(Constant.INVERTED_PIERCING)
            or t.isPattern(Constant.MORNING_STAR))


def getLowestValue(symbol):
    t = symbol.tickData[symbol.topIndex-1]
    if t.isPattern(Constant.MORNING_STAR) or t.isPattern(Constant.EVENING_STAR):
        l = symbol.tickData[symbol.topIndex-4:symbol.topIndex-1]
    else:
        l = symbol.tickData[symbol.topIndex-3:symbol.topIndex-1]
    min = 99999999
    for i in l:
        if i.info[Constant.KEY_LOW] < min:
            min = i.info[Constant.KEY_LOW]
    return min


def getSymbolByExchangeToken(exchangeToken):
    for s in SymbolDict.keys():
        if SymbolDict[s].exchangeToken == exchangeToken:
            return SymbolDict[s]

def getSymbolBySymbolName(symbolName):
    for s in SymbolDict.keys():
        if SymbolDict[s].symbolName == symbolName:
            return SymbolDict[s]

def getSymbolByTradingSymbol(tradingSymbol):
    for s in SymbolDict.keys():
        if SymbolDict[s].tradingSymbol == tradingSymbol:
            return SymbolDict[s]



class Trade:
    def __init__(self, symbol):
        self.status = Constant.TRADE_NOT_STARTED
        self.entryPrice = 0
        self.entryTime = 0
        self.exitPrice = 0
        self.exitTime = 0
        self.buyTriggerCall = -1
        self.buyTriggerPut = -1
        self.stopLoss = 0
        self.takeProfit = 0
        self.tick = None
        self.strategy = None
        self.symbol = symbol
        self.ID = str(time.time())[-10:].replace(".","")
        time.sleep(0.000001)
        self.strategyName = None
        self.gain = 0
        self.timeOfEntry = 0

    def serialize(self):
       return  {'status': self.status, 'entryPrice': self.entryPrice, 'entryTime': self.entryTime,
             'exitPrice': self.exitPrice, 'exitTime': self.exitTime, 'buyTriggerCall': self.buyTriggerCall, 'buyTriggerPut': self.buyTriggerPut,
             'stopLoss': self.stopLoss, 'takeProfit': self.takeProfit, 'ID': self.ID, 'strategyName': self.strategyName,
             'gain': self.gain}


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
