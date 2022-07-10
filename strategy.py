import Constant
import Common


def MACrossoverEntry(trade):
    if (trade.symbol.topIndex < 2):
        return
    last = trade.symbol.tickData[trade.symbol.topIndex - 1]
    if (Common.isUpwardPattern(last)):
        if trade.symbol.top.info[Constant.KEY_CLOSE] > trade.symbol.top.info[
            Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] and last.info[Constant.KEY_HIGH] < last.info[
            Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] and trade.symbol.top.info[Constant.KEY_RSI] >= 55:
            print("Can buy on ", trade.symbol.top.info[Constant.KEY_DATE])
            return 1
    return 0


def MACCrossoverExit(trade, price):
    if trade.status == Constant.TRADE_ENTRY:
        if price > trade.takeProfit:
            trade.status = Constant.TRADE_COMPLETED
            print("Sell for Trade at " +
                  str(trade.tick.info[Constant.KEY_DATE]) + " at Price " + str(price) + " for takeProfit " + str(
                trade.takeProfit) + " on " + trade.symbol.top.info[Constant.KEY_DATE])
            return 1
    if trade.status != Constant.TRADE_COMPLETED:
        if price < trade.stopLoss:
            trade.status = Constant.TRADE_COMPLETED
            print("Exit for Trade at " +
                  str(trade.tick.info[Constant.KEY_DATE]) + " at Price " + str(price) + " for stoploss " + str(
                trade.stopLoss) + " on " + trade.symbol.top.info[Constant.KEY_DATE])
            return 1
    return 0


def MACrossoverOnEnter(trade):
    trade.buyTrigger = trade.symbol.top.info[Constant.KEY_HIGH]
    trade.stopLoss = Common.getLowestValue(trade.symbol)
    trade.takeProfit = trade.buyTrigger + abs(trade.buyTrigger - trade.stopLoss) * trade.symbol.riskFactor


def init():
    s = Strategy(Constant.STRATEGY_MA_CROSSOVER_UP, MACrossoverEntry, MACrossoverOnEnter, MACCrossoverExit)
    Common.strategyDict[Constant.STRATEGY_MA_CROSSOVER_UP] = s
    s = Strategy(Constant.STRATEGY_GANN_ANALYSIS, GannAnalysisCheckForEntry, GannAnalysisOnEnter,
                 GannAnalysisCheckForExit)
    Common.strategyDict[Constant.STRATEGY_GANN_ANALYSIS] = s


def update(symbol):
    checkStrategy(symbol)


def checkStrategy(symbol):
    MACrossoverEntry(symbol)


# after upward pattern is detected next candle should cross moving average
# stoplose  => pattern low


def GannAnalysis(symbol):
    try:
        ref = symbol.data[Constant.KEY_GANN_REFERENCE]
    except:
        ref = symbol.tickData[symbol.topIndex].info[Constant.KEY_CLOSE]
        symbol.data[Constant.KEY_GANN_REFERENCE] = ref
    next = Common.getNextGannLevel(ref)
    # if ref > next:
    #      symbol.addToWatchList(Constant.STRATEGY_GANN_ANALYSIS)


def GannAnalysisCheckForEntry(trade):
    if trade.buyTrigger < 0:
        trade.buyTrigger = Common.getNextGannLevel(trade.symbol.lastTradedPrice)
    if trade.symbol.lastTradedPrice > trade.buyTrigger:
        print("Can buy on ", trade.symbol.top.info[Constant.KEY_DATE])
        return 1
    return 0


def GannAnalysisOnEnter(trade):
    trade.takeProfit = Common.getNextGannLevel(trade.buyTrigger + 0.1)
    trade.stopLoss = Common.getPreviousGannLevel(trade.buyTrigger - 0.1)


def GannAnalysisCheckForExit(trade):
    if trade.symbol.lastTradedPrice > trade.buyTrigger:
        trade.buyTrigger = Common.getNextGannLevel(trade.buyTrigger)
        print("Sell for Trade at " +
              str(trade.tick.info[Constant.KEY_DATE]) + " at Price " + str(
            trade.symbol.lastTradedPrice) + " for takeProfit " + str(trade.takeProfit) + " on " + trade.symbol.top.info[
                  Constant.KEY_DATE])
        return 1
    if trade.symbol.lastTradedPrice < trade.stopLoss:
        print("Exit for Trade at " +
              str(trade.tick.info[Constant.KEY_DATE]) + " at Price " + str(
            trade.symbol.lastTradedPric) + " for stoploss " + str(trade.stopLoss) + " on " + trade.symbol.top.info[
                  Constant.KEY_DATE])
        return 1
    return 0


class Strategy:
    def __init__(self, name, entryLogic, onEnter, exitLogic):
        self.name = name
        self.checkForEntry = entryLogic
        self.onEnter = onEnter
        self.checkForExit = exitLogic
