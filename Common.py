import Constant

SymbolDict = {}
watchlist = []


class Tick:
    def __init__(self, data):
        self.info = {}
        self.info[Constant.KEY_DATE] = data['date']
        high = self.info[Constant.KEY_HIGH] = (float)(data['high'])
        low = self.info[Constant.KEY_LOW] = (float)(data['low'])
        open = self.info[Constant.KEY_OPEN] = (float)(data['open'])
        close = self.info[Constant.KEY_CLOSE] = (float)(data['close'])
        self.info[Constant.KEY_VOLUME] = (float)(data['VOLUME'])
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
