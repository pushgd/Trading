import Constant
import analyze
import Common
top = 0
watchlist = []


def update():
    global topIndex
    topIndex = Common.topIndex
    global top
    top = Common.tickData[topIndex]
    checkStrategy()


def checkStrategy():
    MACrossover()

# after upward pattern is detected next candle should cross moving average
# stoplose  => pattern low


def MACrossover():
    global topIndex
    if(topIndex < 2):
        return
    last = Common.tickData[topIndex-1]
    if(isUpwardPattern(last)):
        if(top.candle.close > top.indicator.movingAverageShortClose and last.candle.high < last.indicator.movingAverageShortClose and top.indicator.RSI > 60):
            print("Can buy on ", top.date)


def isUpwardPattern(t):
    return ((t.isPattern(Constant.HARAMI) and t.candle.isBull())
            or (t.isPattern(Constant.ENGULFING) and t.candle.isBull())
            or (t.isPattern(Constant.ENGULFING) and t.candle.isBull())
            or t.isPattern(Constant.PIERCING)
            or t.isPattern(Constant.INVERTED_PIERCING)
            or t.isPattern(Constant.MORNING_STAR))
