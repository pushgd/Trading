import Constant
import Common


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
    if(Common.isUpwardPattern(last)):
        if(symbol.top.info[Constant.KEY_CLOSE] > symbol.top.info[Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] and last.info[Constant.KEY_HIGH] < last.info[Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] and symbol.top.info[Constant.KEY_RSI] >= 55):
            print("Can buy on ", symbol.top.info[Constant.KEY_DATE])
            symbol.addToWatchList(Constant.STRATEGY_MA_CROSSOVER_UP)
