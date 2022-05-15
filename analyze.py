import Constant
import Common


def update(data):
    # candels.append(data)
    # c = Candle()

    Common.topIndex = Common.topIndex+1
    global topIndex
    topIndex = Common.topIndex
    Common.tickData.append(Tick(data))
    if(topIndex > 0):
        Common.tickData[topIndex].indicator.cumulativeVolume = Common.tickData[topIndex -
                                                                               1].indicator.cumulativeVolume+Common.tickData[topIndex].indicator.volume
    else:
        Common.tickData[topIndex].indicator.cumulativeVolume = Common.tickData[topIndex].indicator.volume
    # candels[topIndex].append(candels[])
    calculateSMA()
    calculateEMA()
    if topIndex >= Constant.RSI_WINDOW:
        calculateRSI()
    # calculateVWAP()

    checkPatterns()

    # print(Common.tickData[topIndex].pattern)
    # print(Common.tickData[topIndex])

    return Common.tickData[topIndex]


def calculateSMA():
    top = Common.tickData[topIndex]
    avg = [0, 0, 0, 0]
    for t in Common.tickData[-Constant.MOVING_AVERAGE_SHORT_WINDOW:]:
        avg[0] = avg[0] + t.candle.open
        avg[1] = avg[1] + t.candle.close
        avg[2] = avg[2] + t.candle.low
        avg[3] = avg[3] + t.candle.high

    top.indicator.movingAverageShortOpen = avg[0] / \
        Constant.MOVING_AVERAGE_SHORT_WINDOW
    top.indicator.movingAverageShortClose = avg[1] / \
        Constant.MOVING_AVERAGE_SHORT_WINDOW
    top.indicator.movingAverageShortLow = avg[2] / \
        Constant.MOVING_AVERAGE_SHORT_WINDOW
    top.indicator.movingAverageShortHigh = avg[3] / \
        Constant.MOVING_AVERAGE_SHORT_WINDOW

    avg = [0, 0, 0, 0]
    for t in Common.tickData[-Constant.MOVING_AVERAGE_MEDIUM_WINDOW:]:
        avg[0] = avg[0] + t.candle.open
        avg[1] = avg[1] + t.candle.close
        avg[2] = avg[2] + t.candle.low
        avg[3] = avg[3] + t.candle.high

    top.indicator.movingAverageMediumOpen = avg[0] / \
        Constant.MOVING_AVERAGE_MEDIUM_WINDOW
    top.indicator.movingAverageMediumClose = avg[1] / \
        Constant.MOVING_AVERAGE_MEDIUM_WINDOW
    top.indicator.movingAverageMediumLow = avg[2] / \
        Constant.MOVING_AVERAGE_MEDIUM_WINDOW
    top.indicator.movingAverageMediumHigh = avg[3] / \
        Constant.MOVING_AVERAGE_MEDIUM_WINDOW

    avg = [0, 0, 0, 0]
    for t in Common.tickData[-Constant.MOVING_AVERAGE_LONG_WINDOW:]:
        avg[0] = avg[0] + t.candle.open
        avg[1] = avg[1] + t.candle.close
        avg[2] = avg[2] + t.candle.low
        avg[3] = avg[3] + t.candle.high

    top.indicator.movingAverageLongOpen = avg[0] / \
        Constant.MOVING_AVERAGE_LONG_WINDOW
    top.indicator.movingAverageLongClose = avg[1] / \
        Constant.MOVING_AVERAGE_LONG_WINDOW
    top.indicator.movingAverageLongLow = avg[2] / \
        Constant.MOVING_AVERAGE_LONG_WINDOW
    top.indicator.movingAverageLongHigh = avg[3] / \
        Constant.MOVING_AVERAGE_LONG_WINDOW


def calculateEMA():
    top = Common.tickData[topIndex]
    smoothing = 2/(1+Constant.EXPONENTIAL_AVERAGE_WINDOW)
    if(topIndex != 0):
        lastAvg = Common.tickData[topIndex -
                                  1].indicator.exponentialAverageOpen
        top.indicator.exponentialAverageOpen = top.candle.open * \
            smoothing + lastAvg*(1-smoothing)

        lastAvg = Common.tickData[topIndex -
                                  1].indicator.exponentialAverageClose
        top.indicator.exponentialAverageClose = top.candle.close * \
            smoothing + lastAvg*(1-smoothing)

        lastAvg = Common.tickData[topIndex -
                                  1].indicator.exponentialAverageHigh
        top.indicator.exponentialAverageHigh = top.candle.high * \
            smoothing + lastAvg*(1-smoothing)

        lastAvg = Common.tickData[topIndex -
                                  1].indicator.exponentialAverageLow
        top.indicator.exponentialAverageLow = top.candle.low * \
            smoothing + lastAvg*(1-smoothing)
    else:
        top.indicator.exponentialAverageOpen = top.candle.open
        top.indicator.exponentialAverageClose = top.candle.close
        top.indicator.exponentialAverageLow = top.candle.low
        top.indicator.exponentialAverageHigh = top.candle.high


def calculateRSI():
    top = Common.tickData[topIndex]
    g = 0
    l = 0

    if topIndex == Constant.RSI_WINDOW:
        avg = [0, 0]
        for t in Common.tickData[-Constant.RSI_WINDOW:]:
            if t.candle.gain > 0:
                avg[0] = avg[0]+t.candle.gain
                g = g + 1
            else:
                avg[1] = avg[1]+abs(t.candle.gain)
                l = l+1

        top.candle.gainAverage = avg[0]/Constant.RSI_WINDOW
        top.candle.loseAverage = avg[1]/Constant.RSI_WINDOW
    else:
        top.candle.gainAverage = ((Common.tickData[topIndex-1].candle.gainAverage *
                                   (Constant.RSI_WINDOW-1))+top.candle.gain)/Constant.RSI_WINDOW

        top.candle.loseAverage = ((Common.tickData[topIndex-1].candle.loseAverage *
                                   (Constant.RSI_WINDOW-1))+top.candle.lose)/Constant.RSI_WINDOW
    if(top.candle.loseAverage != 0):
        top.indicator.relativeStrength = top.candle.gainAverage / top.candle.loseAverage
        top.indicator.RSI = 100 - \
            (100 / (1+top.indicator.relativeStrength))
    else:
        top.indicator.RSI = 100


def calculateVWAP():
    top = Common.tickData[topIndex]
    pv = ((top.candle.low+top.candle.high+top.candle.close)/3) * \
        top.indicator.volume
    if(topIndex == 0):
        top.indicator.cumulativePV = pv
    else:
        top.indicator.cumulativePV = pv + \
            Common.tickData[topIndex-1].indicator.cumulativePV
    top.indicator.VWAP = top.indicator.cumulativePV/top.indicator.cumulativeVolume


def checkPatterns():

    if(Common.tickData[topIndex].date == '13-Jul-2021'):
        print("stop")
    pattern = checkDoji()
    if checkDoji():
        Common.tickData[topIndex].pattern.append(pattern)
        return

    pattern = checkEngulfing()
    if pattern != False:
        Common.tickData[topIndex].pattern.append(pattern)

    pattern = checkHarami()
    if pattern != False:
        Common.tickData[topIndex].pattern.append(pattern)

    pattern = checkDarkCloud()
    if pattern != False:
        Common.tickData[topIndex].pattern.append(pattern)

    pattern = checkPiercing()
    if pattern != False:
        Common.tickData[topIndex].pattern.append(pattern)

    pattern = checkInvertedPiercing()
    if pattern != False:
        Common.tickData[topIndex].pattern.append(pattern)

    pattern = checkEveningStar()
    if pattern != False:
        Common.tickData[topIndex].pattern.append(pattern)

    pattern = checkMorningStar()
    if pattern != False:
        Common.tickData[topIndex].pattern.append(pattern)


def checkDoji():
    if(Common.tickData[topIndex].candle.body/Common.tickData[topIndex].candle.length < Constant.DOJI_RATIO):
        return Constant.DOJI
    return False


def checkEngulfing():
    current = Common.tickData[topIndex]
    last = Common.tickData[topIndex-1]
    if (current.candle.type == last.candle.type):
        return False
    if(current.candle.isInsideLength(last.candle.high) and current.candle.isInsideLength(last.candle.low)):
        return Constant.ENGULFING
    return False


def checkHarami():
    current = Common.tickData[topIndex]
    last = Common.tickData[topIndex-1]
    if (current.candle.type == last.candle.type):
        return False
    if(last.candle.isInsideBody(current.candle.high) and last.candle.isInsideBody(current.candle.low)):
        return Constant.HARAMI
    return False


def checkDarkCloud():
    current = Common.tickData[topIndex]
    last = Common.tickData[topIndex-1]
    if (current.candle.type == last.candle.type):
        return False
    if(not last.isPattern(Constant.DOJI) and current.candle.isBear() and current.candle.open > last.candle.high and last.candle.mean > current.candle.close and current.candle.low > last.candle.low):
        return Constant.DARK_CLOUD
    return False


def checkPiercing():
    current = Common.tickData[topIndex]
    last = Common.tickData[topIndex-1]
    if (current.candle.type == last.candle.type):
        return False
    if(not last.isPattern(Constant.DOJI) and current.candle.isBull() and current.candle.open < last.candle.low and last.candle.mean < current.candle.close and current.candle.high < last.candle.high):
        return Constant.PIERCING
    return False


def checkInvertedPiercing():
    current = Common.tickData[topIndex]
    last = Common.tickData[topIndex-1]
    if (current.candle.type == last.candle.type):
        return False
    if(not last.isPattern(Constant.DOJI) and current.candle.isBull() and approxEqual(last.candle.bodyMean, current.candle.open, errorMargin=(0.1/100)) and current.candle.close > last.candle.high and current.candle.low > last.candle.low):
        return Constant.INVERTED_PIERCING
    return False
# current.candle.open > last.candle.close and current.candle.open < last.candle.bodyMean


def checkEveningStar():
    if topIndex < 2:
        return False
    c1 = Common.tickData[topIndex]
    c2 = Common.tickData[topIndex-1]
    c3 = Common.tickData[topIndex-2]
    if c1.candle.isBear() and not c1.isPattern(Constant.DOJI) and c2.isPattern(Constant.DOJI) and not c3.isPattern(Constant.DOJI) and c3.candle.isBull() and c1.candle.high < c2.candle.high and c3.candle.high < c2.candle.high:
        return Constant.EVENING_STAR
    return False


def checkMorningStar():
    if topIndex < 2:
        return False
    c1 = Common.tickData[topIndex]
    c2 = Common.tickData[topIndex-1]
    c3 = Common.tickData[topIndex-2]
    if c1.candle.isBull() and not c1.isPattern(Constant.DOJI) and c2.isPattern(Constant.DOJI) and not c3.isPattern(Constant.DOJI) and c3.candle.isBear() and c1.candle.low > c2.candle.low and c3.candle.low > c2.candle.low:
        return Constant.MORNING_STAR
    return False


def approxEqual(a, b, errorMargin=0.1):
    diff = abs(a-b)
    return diff <= a*errorMargin


class Tick:
    def __init__(self, data):
        self.date = data['date']
        self.candle = Candle(data['high'], data['low'],
                             data['open'], data['close'])
        self.pattern = []
        self.indicator = Indicator(data['VOLUME'])

    def __str__(self):

        s = "Date "+self.date + "  " + self.candle.type+"\n"
        s = s+"Open "+str(self.candle.open) + " Close " + \
            str(self.candle.close)+"\n"
        s = s + "High "+str(self.candle.high) + " Low "+str(self.candle.low)
        s = s + "\n--------------------------------\n"
        return s

    def isPattern(self, pattern):
        return pattern in self.pattern

    def serialize(self):
        dict = {}
        dict['date'] = self.date

        dict['open'] = self.candle.open
        dict['close'] = self.candle.close
        dict['high'] = self.candle.high
        dict['low'] = self.candle.low
        dict['gain'] = self.candle.low
        dict['loss'] = self.candle.low

        dict['volume'] = self.indicator.volume
        dict['RSI'] = self.indicator.RSI
        dict['movingAverageShortOpen'] = self.indicator.movingAverageShortOpen
        dict['movingAverageShortClose'] = self.indicator.movingAverageShortClose
        dict['movingAverageShortHigh'] = self.indicator.movingAverageShortHigh
        dict['movingAverageShortLow'] = self.indicator.movingAverageShortLow
        dict['movingAverageMediumOpen'] = self.indicator.movingAverageMediumOpen
        dict['movingAverageMediumClose'] = self.indicator.movingAverageMediumClose
        dict['movingAverageMediumHigh'] = self.indicator.movingAverageMediumHigh
        dict['movingAverageMediumLow'] = self.indicator.movingAverageMediumLow
        dict['movingAverageLongOpen'] = self.indicator.movingAverageLongOpen
        dict['movingAverageLongClose'] = self.indicator.movingAverageLongClose
        dict['movingAverageLongHigh'] = self.indicator.movingAverageLongHigh
        dict['movingAverageLongLow'] = self.indicator.movingAverageLongLow
        dict['exponentialAverageOpen'] = self.indicator.exponentialAverageOpen
        dict['exponentialAverageClose'] = self.indicator.exponentialAverageClose
        dict['exponentialAverageLow'] = self.indicator.exponentialAverageLow
        dict['exponentialAverageHigh'] = self.indicator.exponentialAverageHigh
        return dict


class Candle:
    def __init__(self, high, low, open, close):
        self.high = (float)(high)
        self.low = (float)(low)
        self.open = (float)(open)
        self.close = (float)(close)
        self.body = abs(self.open - self.close)
        self.length = abs(self.high - self.low)
        self.type = Constant.BULL if self.close > self.open else Constant.BEAR
        self.mean = (self.high + self.low)/2.0
        self.bodyMean = (self.open + self.close)/2.0
        self.gain = 0
        self.lose = 0
        if(topIndex > 0):
            if(self.close > Common.tickData[topIndex-1].candle.close):
                self.gain = self.close - \
                    Common.tickData[topIndex-1].candle.close
                self.lose = 0
            else:
                self.lose = abs(
                    self.close - Common.tickData[topIndex-1].candle.close)
                self.gain = 0
        self.gainAverage = 0
        self.loseAverage = 0

    def candleBodyInsideLength(self, other):
        return other.open <= self.high and other.open >= self.low and other.close <= self.high and other.close >= self.low

    def isInsideBody(self, value):
        if(self.isBull()):
            return value > self.open and value < self.close
        return value < self.open and value > self.close

    def isInsideLength(self, value):
        return value > self.low and value < self.high

    def isBull(self):
        return self.type == Constant.BULL

    def isBear(self):
        return self.type == Constant.BEAR


class Indicator:
    def __init__(self, volume):
        self.volume = (float)(volume)
        self.cumulativeVolume = 0
        self.cumulativePV = 0
        self.VWAP = 0

        self.RSI = 0
        self.relativeStrength = 0

        self.movingAverageShortOpen = 0
        self.movingAverageShortClose = 0
        self.movingAverageShortLow = 0
        self.movingAverageShortHigh = 0

        self.movingAverageMediumOpen = 0
        self.movingAverageMediumClose = 0
        self.movingAverageMediumLow = 0
        self.movingAverageMediumHigh = 0

        self.movingAverageLongOpen = 0
        self.movingAverageLongClose = 0
        self.movingAverageLongLow = 0
        self.movingAverageLongHigh = 0

        self.exponentialAverageOpen = 0
        self.exponentialAverageClose = 0
        self.exponentialAveragegLow = 0
        self.exponentialAverageHigh = 0
