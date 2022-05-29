import Constant


def update(symbol):
    # candels.append(data)
    # c = Candle()

    # Common.topIndex = Common.topIndex+1
    # global topIndex
    # topIndex = Common.topIndex
    # symbol.tickData.append(Tick(data))
    if(symbol.topIndex > 0):
        symbol.top.info[Constant.KEY_CUMMULATIVE_VOLUME] = symbol.tickData[symbol.topIndex -
                                                                           1].info[Constant.KEY_CUMMULATIVE_VOLUME]+symbol.tickData[symbol.topIndex].info[Constant.KEY_VOLUME]
    else:
        symbol.top.info[Constant.KEY_CUMMULATIVE_VOLUME] = symbol.top.info[Constant.KEY_VOLUME]
    # candels[symbol.topIndex].append(candels[])
    calculateSMA(symbol)
    calculateEMA(symbol)
    if symbol.topIndex >= Constant.RSI_WINDOW:
        calculateRSI(symbol)
    # calculateVWAP()

    checkPatterns(symbol)

    # print(symbol.tickData[symbol.topIndex].pattern)
    # print(symbol.tickData[symbol.topIndex])

    return symbol.top


def calculateSMA(symbol):
    top = symbol.top
    avg = [0, 0, 0, 0]
    for t in symbol.tickData[-Constant.MOVING_AVERAGE_SHORT_WINDOW:]:
        avg[0] = avg[0] + t.info[Constant.KEY_OPEN]
        avg[1] = avg[1] + t.info[Constant.KEY_CLOSE]
        avg[2] = avg[2] + t.info[Constant.KEY_LOW]
        avg[3] = avg[3] + t.info[Constant.KEY_HIGH]

    top.info[Constant.KEY_MOVING_AVERAGE_SHORT_OPEN] = avg[0] / \
        Constant.MOVING_AVERAGE_SHORT_WINDOW
    top.info[Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE] = avg[1] / \
        Constant.MOVING_AVERAGE_SHORT_WINDOW
    top.info[Constant.KEY_MOVING_AVERAGE_SHORT_LOW] = avg[2] / \
        Constant.MOVING_AVERAGE_SHORT_WINDOW
    top.info[Constant.KEY_MOVING_AVERAGE_SHORT_HIGH] = avg[3] / \
        Constant.MOVING_AVERAGE_SHORT_WINDOW

    avg = [0, 0, 0, 0]
    for t in symbol.tickData[-Constant.MOVING_AVERAGE_MEDIUM_WINDOW:]:
        avg[0] = avg[0] + t.info[Constant.KEY_OPEN]
        avg[1] = avg[1] + t.info[Constant.KEY_CLOSE]
        avg[2] = avg[2] + t.info[Constant.KEY_LOW]
        avg[3] = avg[3] + t.info[Constant.KEY_HIGH]

    top.info[Constant.KEY_MOVING_AVERAGE_MEDUIM_OPEN] = avg[0] / \
        Constant.MOVING_AVERAGE_MEDIUM_WINDOW
    top.info[Constant.KEY_MOVING_AVERAGE_MEDUIM_CLOSE] = avg[1] / \
        Constant.MOVING_AVERAGE_MEDIUM_WINDOW
    top.info[Constant.KEY_MOVING_AVERAGE_MEDUIM_LOW] = avg[2] / \
        Constant.MOVING_AVERAGE_MEDIUM_WINDOW
    top.info[Constant.KEY_MOVING_AVERAGE_MEDUIM_HIGH] = avg[3] / \
        Constant.MOVING_AVERAGE_MEDIUM_WINDOW

    avg = [0, 0, 0, 0]
    for t in symbol.tickData[-Constant.MOVING_AVERAGE_LONG_WINDOW:]:
        avg[0] = avg[0] + t.info[Constant.KEY_OPEN]
        avg[1] = avg[1] + t.info[Constant.KEY_CLOSE]
        avg[2] = avg[2] + t.info[Constant.KEY_LOW]
        avg[3] = avg[3] + t.info[Constant.KEY_HIGH]

    top.info[Constant.KEY_MOVING_AVERAGE_LONG_OPEN] = avg[0] / \
        Constant.MOVING_AVERAGE_LONG_WINDOW
    top.info[Constant.KEY_MOVING_AVERAGE_LONG_CLOSE] = avg[1] / \
        Constant.MOVING_AVERAGE_LONG_WINDOW
    top.info[Constant.KEY_MOVING_AVERAGE_LONG_LOW] = avg[2] / \
        Constant.MOVING_AVERAGE_LONG_WINDOW
    top.info[Constant.KEY_MOVING_AVERAGE_LONG_HIGH] = avg[3] / \
        Constant.MOVING_AVERAGE_LONG_WINDOW


def calculateEMA(symbol):
    top = symbol.top
    smoothing = 2/(1+Constant.EXPONENTIAL_AVERAGE_WINDOW)
    if(symbol.topIndex != 0):
        lastAvg = symbol.tickData[symbol.topIndex -
                                  1].info[Constant.KEY_EXPONENTIAL_AVERAGE_OPEN]
        top.info[Constant.KEY_EXPONENTIAL_AVERAGE_OPEN] = top.info[Constant.KEY_OPEN] * \
            smoothing + lastAvg*(1-smoothing)

        lastAvg = symbol.tickData[symbol.topIndex -
                                  1].info[Constant.KEY_EXPONENTIAL_AVERAGE_CLOSE]
        top.info[Constant.KEY_EXPONENTIAL_AVERAGE_CLOSE] = top.info[Constant.KEY_CLOSE] * \
            smoothing + lastAvg*(1-smoothing)

        lastAvg = symbol.tickData[symbol.topIndex -
                                  1].info[Constant.KEY_EXPONENTIAL_AVERAGE_HIGH]
        top.info[Constant.KEY_EXPONENTIAL_AVERAGE_HIGH] = top.info[Constant.KEY_HIGH] * \
            smoothing + lastAvg*(1-smoothing)

        lastAvg = symbol.tickData[symbol.topIndex -
                                  1].info[Constant.KEY_EXPONENTIAL_AVERAGE_LOW]
        top.info[Constant.KEY_EXPONENTIAL_AVERAGE_LOW] = top.info[Constant.KEY_LOW] * \
            smoothing + lastAvg*(1-smoothing)
    else:
        top.info[Constant.KEY_EXPONENTIAL_AVERAGE_OPEN] = top.info[Constant.KEY_OPEN]
        top.info[Constant.KEY_EXPONENTIAL_AVERAGE_CLOSE] = top.info[Constant.KEY_CLOSE]
        top.info[Constant.KEY_EXPONENTIAL_AVERAGE_LOW] = top.info[Constant.KEY_LOW]
        top.info[Constant.KEY_EXPONENTIAL_AVERAGE_HIGH] = top.info[Constant.KEY_HIGH]


def calculateRSI(symbol):
    top = symbol.top
    g = 0
    l = 0

    if symbol.topIndex == Constant.RSI_WINDOW:
        avg = [0, 0]
        for t in symbol.tickData[-Constant.RSI_WINDOW:]:
            if t.info[Constant.KEY_GAIN] > 0:
                avg[0] = avg[0]+t.info[Constant.KEY_GAIN]
                g = g + 1
            else:
                avg[1] = avg[1]+abs(t.info[Constant.KEY_GAIN])
                l = l+1

        top.info[Constant.KEY_AVERAGE_GAIN] = avg[0]/Constant.RSI_WINDOW
        top.info[Constant.KEY_AVERAGE_LOSS] = avg[1]/Constant.RSI_WINDOW
    else:
        top.info[Constant.KEY_AVERAGE_GAIN] = ((symbol.tickData[symbol.topIndex-1].info[Constant.KEY_AVERAGE_GAIN] *
                                                (Constant.RSI_WINDOW-1))+top.info[Constant.KEY_GAIN])/Constant.RSI_WINDOW

        top.info[Constant.KEY_AVERAGE_LOSS] = ((symbol.tickData[symbol.topIndex-1].info[Constant.KEY_AVERAGE_LOSS] *
                                                (Constant.RSI_WINDOW-1))+top.info[Constant.KEY_LOSS])/Constant.RSI_WINDOW
    if(top.info[Constant.KEY_AVERAGE_LOSS] != 0):
        top.info[Constant.KEY_RS] = top.info[Constant.KEY_AVERAGE_GAIN] / \
            top.info[Constant.KEY_AVERAGE_LOSS]
        top.info[Constant.KEY_RSI] = 100 - \
            (100 / (1+top.info[Constant.KEY_RS]))
    else:
        top.info[Constant.KEY_RSI] = 100


def calculateVWAP(symbol):
    top = symbol.top
    pv = ((top.info[Constant.KEY_LOW]+top.info[Constant.KEY_HIGH]+top.info[Constant.KEY_CLOSE])/3) * \
        top.info[Constant.KEY_VOLUME]
    if(symbol.topIndex == 0):
        top.info[Constant.KEY_CUMMULATIVE_PV] = pv
    else:
        top.info[Constant.KEY_CUMMULATIVE_PV] = pv + \
            symbol.tickData[symbol.topIndex -
                            1].info[Constant.KEY_CUMMULATIVE_PV]
    top.info[Constant.KEY_CUMMULATIVE_VWAP] = top.info[Constant.KEY_CUMMULATIVE_PV] / \
        top.info[Constant.KEY_CUMMULATIVE_VOLUME]


def checkPatterns(symbol):

    pattern = checkDoji(symbol)
    if pattern != False:
        symbol.top.info[Constant.KEY_PATTERN].append(pattern)
        return

    pattern = checkEngulfing(symbol)
    if pattern != False:
        symbol.top.info[Constant.KEY_PATTERN].append(pattern)
    if symbol.top.info[Constant.KEY_DATE] == '10-02-2022 10.00':
        print('stop')
    pattern = checkHarami(symbol)
    if pattern != False:
        symbol.top.info[Constant.KEY_PATTERN].append(pattern)

    pattern = checkDarkCloud(symbol)
    if pattern != False:
        symbol.top.info[Constant.KEY_PATTERN].append(pattern)

    pattern = checkPiercing(symbol)
    if pattern != False:
        symbol.top.info[Constant.KEY_PATTERN].append(pattern)

    pattern = checkInvertedPiercing(symbol)
    if pattern != False:
        symbol.top.info[Constant.KEY_PATTERN].append(pattern)

    pattern = checkEveningStar(symbol)
    if pattern != False:
        symbol.top.info[Constant.KEY_PATTERN].append(pattern)

    pattern = checkMorningStar(symbol)
    if pattern != False:
        symbol.top.info[Constant.KEY_PATTERN].append(pattern)


def checkDoji(symbol):
    if(symbol.tickData[symbol.topIndex].info[Constant.KEY_BODY_LENGTH]/symbol.tickData[symbol.topIndex].info[Constant.KEY_LENGTH] < Constant.DOJI_RATIO):
        return Constant.DOJI
    return False


def checkEngulfing(symbol):
    current = symbol.top
    last = symbol.tickData[symbol.topIndex-1]
    if (current.info[Constant.KEY_TYPE] == last.info[Constant.KEY_TYPE]):
        return False
    if(current.isInsideLength(last.info[Constant.KEY_HIGH]) and current.isInsideLength(last.info[Constant.KEY_LOW])):
        return Constant.ENGULFING
    return False


def checkHarami(symbol):
    current = symbol.top
    last = symbol.tickData[symbol.topIndex-1]
    if (current.info[Constant.KEY_TYPE] == last.info[Constant.KEY_TYPE]):
        return False
    if(last.isInsideBody(current.info[Constant.KEY_HIGH]) and last.isInsideBody(current.info[Constant.KEY_LOW])):
        return Constant.HARAMI
    return False


def checkDarkCloud(symbol):
    current = symbol.top
    last = symbol.tickData[symbol.topIndex-1]
    if (current.info[Constant.KEY_TYPE] == last.info[Constant.KEY_TYPE]):
        return False
    if(not last.isPattern(Constant.DOJI) and current.isBear() and current.info[Constant.KEY_OPEN] > last.info[Constant.KEY_HIGH] and last.info[Constant.KEY_MEAN] > current.info[Constant.KEY_CLOSE] and current.info[Constant.KEY_LOW] > last.info[Constant.KEY_LOW]):
        return Constant.DARK_CLOUD
    return False


def checkPiercing(symbol):
    current = symbol.top
    last = symbol.tickData[symbol.topIndex-1]
    if (current.info[Constant.KEY_TYPE] == last.info[Constant.KEY_TYPE]):
        return False
    if(not last.isPattern(Constant.DOJI) and current.isBull() and current.info[Constant.KEY_OPEN] < last.info[Constant.KEY_LOW] and last.info[Constant.KEY_MEAN] < current.info[Constant.KEY_CLOSE] and current.info[Constant.KEY_HIGH] < last.info[Constant.KEY_HIGH]):
        return Constant.PIERCING
    return False


def checkInvertedPiercing(symbol):
    current = symbol.top
    last = symbol.tickData[symbol.topIndex-1]
    if (current.info[Constant.KEY_TYPE] == last.info[Constant.KEY_TYPE]):
        return False
    if(not last.isPattern(Constant.DOJI) and current.isBull() and approxEqual(last.info[Constant.KEY_BODY_MEAN], current.info[Constant.KEY_OPEN], errorMargin=(0.1/100)) and current.info[Constant.KEY_CLOSE] > last.info[Constant.KEY_HIGH] and current.info[Constant.KEY_LOW] > last.info[Constant.KEY_LOW]):
        return Constant.INVERTED_PIERCING
    return False
# current.info[Constant.KEY_OPEN] > last.info[Constant.KEY_CLOSE] and current.info[Constant.KEY_OPEN] < last.info[Constant.KEY_BODY_MEAN]


def checkEveningStar(symbol):
    if symbol.topIndex < 2:
        return False
    c1 = symbol.top
    c2 = symbol.tickData[symbol.topIndex-1]
    c3 = symbol.tickData[symbol.topIndex-2]
    if c1.isBear() and not c1.isPattern(Constant.DOJI) and c2.isPattern(Constant.DOJI) and not c3.isPattern(Constant.DOJI) and c3.isBull() and c1.info[Constant.KEY_HIGH] < c2.info[Constant.KEY_HIGH] and c3.info[Constant.KEY_HIGH] < c2.info[Constant.KEY_HIGH]:
        return Constant.EVENING_STAR
    return False


def checkMorningStar(symbol):
    if symbol.topIndex < 2:
        return False
    c1 = symbol.top
    c2 = symbol.tickData[symbol.topIndex-1]
    c3 = symbol.tickData[symbol.topIndex-2]
    if c1.isBull() and not c1.isPattern(Constant.DOJI) and c2.isPattern(Constant.DOJI) and not c3.isPattern(Constant.DOJI) and c3.isBear() and c1.info[Constant.KEY_LOW] > c2.info[Constant.KEY_LOW] and c3.info[Constant.KEY_LOW] > c2.info[Constant.KEY_LOW]:
        return Constant.MORNING_STAR
    return False


def approxEqual(a, b, errorMargin=0.1):
    diff = abs(a-b)
    return diff <= a*errorMargin
