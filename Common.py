import Common
import Constant
import math
import time
import datetime
import csv
import playsound
SymbolDict = {}
watchlist = []
strategyDict = {}

simulateLog = []


def playSound(sound):
    try:
        playsound.playsound(sound)
    except Exception as e:
        print("Error playing sound ", str(e))

def getStartTime():
    t = datetime.datetime.now()
    timeDelta = 5
    if t.minute % timeDelta != 0:
        t = t + datetime.timedelta(minutes=(timeDelta - t.minute % timeDelta))
    t = t.replace(second=0, microsecond=0)
    # Constant.START_TIME = t

    print(f"start time set to {t}")
    return t

def waitSomeTime():
    t = datetime.datetime.now()
    if t.minute % 5 != 0:
        t = t + datetime.timedelta(minutes=(15 - t.minute % 15))
    t = t.replace(second=0, microsecond=0)
    time.sleep((t - datetime.datetime.now()).total_seconds())

def LogDataReceived(msg):
    Constant.LOGGER.dataReceived(msg)


def LogAction(msg):
    Constant.LOGGER.action(msg)
    print(str(datetime.datetime.now())+" "+msg)


def getTillDate():
    return datetime.datetime.now()


def getNextGannLevel(n):
    return math.pow(math.ceil(math.sqrt(n)*4)/4, 2)


def getPreviousGannLevel(n):
    return math.pow(math.floor(math.sqrt(n)*4)/4, 2)


def getNextStrikePrice(price, stepsize=100):
    return int((price/stepsize))*stepsize+stepsize


def getPreviousStrikePrice(price, stepsize=100):
    return int((price/stepsize))*stepsize

def getExpiryDate(date:datetime.date):
    if date < Constant.EXPIRY_DATES[date.month]:
        return Constant.EXPIRY_DATES[date.month]
    else:
        return Constant.EXPIRY_DATES[date.month+1 if date.month+1 < 12 else 1]

def getOptionForStock(symbol,strikePrice,option):
    expiryDate = getExpiryDate(datetime.datetime.now().date())
    with open('instruments.csv') as csvfile:
        fileReader = csv.DictReader(csvfile)
        for row in fileReader:
            if row['assettype'] == "OPTSTK":
                try:
                    d = datetime.datetime.strptime(row['expiry'], "%d/%b/%y")
                    #     print(f" strike price {row['strikeprice']}  type {row['optiontype']}")
                    if row['symbolname'] == symbol and float(row['strikeprice']) == strikePrice and row['optiontype'] == option and d.date() == expiryDate:
                        return {'exchangetoken': row['exchangetoken'], 'tradingsymbol': row['tradingsymbol'], 'lotsize': row['lotsize']}
                except Exception:

                    pass

def getOptionForIndex(symbol,strikePrice,option):
    daysToAdd = 0
    if datetime.datetime.now().weekday() == 0:
        daysToAdd = 3
    elif datetime.datetime.now().weekday() == 1:
        daysToAdd = 2
    elif datetime.datetime.now().weekday() == 2:
        daysToAdd = 1
    elif datetime.datetime.now().weekday() == 3:
        daysToAdd = 7
    elif datetime.datetime.now().weekday() == 4:
        daysToAdd = 6
    expiryDate = datetime.datetime.now(
    ) + datetime.timedelta(days=daysToAdd)  # 4 for friday
    with open('instruments.csv') as csvfile:
        fileReader = csv.DictReader(csvfile)
        for row in fileReader:
            if row['assettype'] == "OPTIDX":
                try:
                    d = datetime.datetime.strptime(row['expiry'], "%d/%b/%y")
                    if row['symbolname'] == symbol and float(row['strikeprice']) == strikePrice and row[
                        'optiontype'] == option and d.date() == expiryDate.date():
                        return {'exchangetoken': row['exchangetoken'], 'tradingsymbol': row['tradingsymbol'],
                                'lotsize': row['lotsize']}
                except Exception:
                    pass


def getSymbolExchangeCodeForStock(symbol,strikePrice,option,expiryDate):
    with open('instruments.csv') as csvfile:
        fileReader = csv.DictReader(csvfile)
        for row in fileReader:
            if row['assettype'] == "OPTIDX" or row['assettype'] == "OPTSTK":
                try:
                    d = datetime.datetime.strptime(row['expiry'], "%d-%b-%y")
                    #     print(f" strike price {row['strikeprice']}  type {row['optiontype']}")
                    if row['symbolname'] == symbol and int(row['strikeprice']) == strikePrice and row['optiontype'] == option and d.date() == expiryDate:
                        return {'exchangetoken': row['exchangetoken'], 'tradingsymbol': row['tradingsymbol'], 'lotsize': row['lotsize']}
                except:
                    pass


def getSymbolExchangeCode(symbol, strikePrice, option,expiryDate):
    if expiryDate != None:
        return getSymbolExchangeCodeForStock(symbol,strikePrice,option,expiryDate)

    daysToAdd = 0
    if datetime.datetime.now().weekday() == 0:
        daysToAdd = 3
    elif datetime.datetime.now().weekday() == 1:
        daysToAdd = 2
    elif datetime.datetime.now().weekday() == 2:
        daysToAdd = 1
    elif datetime.datetime.now().weekday() == 3:
        daysToAdd = 7
    elif datetime.datetime.now().weekday() == 4:
        daysToAdd = 6
    expiryDate = datetime.datetime.now(
    ) + datetime.timedelta(days=daysToAdd)  # 4 for friday
    with open('instruments.csv') as csvfile:
        fileReader = csv.DictReader(csvfile)
        for row in fileReader:
            if row['assettype'] == "OPTIDX" or row['assettype'] == "OPTSTK":
                try:
                    d = datetime.datetime.strptime(row['expiry'], "%d-%b-%y")
                    # if row['symbolname'] == symbol and d.date() == expirayDate.date() and int(row['strikeprice']) == strikePrice:
                    #     print(f" strike price {row['strikeprice']}  type {row['optiontype']}")
                    if row['symbolname'] == symbol and int(row['strikeprice']) == strikePrice and row['optiontype'] == option and d.date() == expiryDate.date():
                        return {'exchangetoken': row['exchangetoken'], 'tradingsymbol': row['tradingsymbol'], 'lotsize': row['lotsize']}
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
        self.ID = str(time.time())[-10:].replace(".", "")
        time.sleep(0.000001)
        self.strategyName = None
        self.gain = 0
        self.timeOfEntry = 0
        self.startDate = None
        self.buyDate = None
        self.exitDate = None
        self.timeOutDate = None
        self.simulate = False
        self.startTime = Common.getStartTime()
        self.quantity = 1

    def serialize(self):
        return {'status': self.status, 'entryPrice': self.entryPrice, 'entryTime': self.entryTime,
                'exitPrice': self.exitPrice, 'exitTime': self.exitTime, 'buyTriggerCall': self.buyTriggerCall, 'buyTriggerPut': self.buyTriggerPut,
                'stopLoss': self.stopLoss, 'takeProfit': self.takeProfit, 'ID': self.ID, 'strategyName': self.strategyName,
                'gain': self.gain,"startDate":self.startDate,"buyDate":self.buyDate,"exitDate":self.exitDate,"timeOutDate":self.timeOutDate}




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
