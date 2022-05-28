import Constant


def update(symbol):
    checkStrategy(symbol)


def checkStrategy(symbol):
    MACrossover(symbol)

# after upward pattern is detected next candle should cross moving average
# stoplose  => pattern low


def MACrossover(symbol):
    if(symbol.topIndex < 2):
        return
    last = symbol.tickData[symbol.topIndex-1]
    if(isUpwardPattern(last)):
        if(symbol.top.info[Constant.KEY_CLOSE] > symbol.top.info[Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] and last.info[Constant.KEY_HIGH] < last.info[Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] and symbol.top.info[Constant.KEY_RSI] > 60):
            print("Can buy on ", symbol.top.date)


def isUpwardPattern(t):
    return ((t.isPattern(Constant.HARAMI) and t.isBull())
            or (t.isPattern(Constant.ENGULFING) and t.isBull())
            or (t.isPattern(Constant.ENGULFING) and t.isBull())
            or t.isPattern(Constant.PIERCING)
            or t.isPattern(Constant.INVERTED_PIERCING)
            or t.isPattern(Constant.MORNING_STAR))
