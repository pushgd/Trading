import analyze
import strategy
import csv
import time
import Constant

import _thread as thread
# import flaskApp
import Common
import execute
import API
import DBHelper
import flaskApp

def fetchAndAnalyseData():
    print("Fetch Started")
    # API.init()
    strategy.init()
    DBHelper.init()
    execute.init()
    API.initLiveData(execute.onNewData)
    with open('WIPRO15MinJan22ToMay.csv') as csvfile:
        fileReader = csv.DictReader(csvfile)
        # next(fileReader)
        for row in fileReader:
            execute.update(row)
            # analyze.update(row)
            # strategy.update()

    Common.SymbolDict['Nifty50'].exportCSV('Nifty50',
                                           Constant.KEY_DATE, Constant.KEY_OPEN, Constant.KEY_HIGH, Constant.KEY_CLOSE, Constant.KEY_LOW, Constant.KEY_VOLUME, Constant.KEY_PATTERN, Constant.KEY_MOVING_AVERAGE_SHORT_CLOSE)
    # with open('result.csv', 'w', newline='') as csvfile:
    #     csvwriter = csv.writer(csvfile)
    #     csvwriter.writerow(["Date", "Type", "open", "close",
    #                        "low", "High", "Candle Mean", "Moving Average Short", "Moving Average Medium", "Moving Average Long", "EXPONENTIAL AVERAGE", "RSI", "VWAP", "Pattern"])
    #     for t in Common.tickData:
    #         csvwriter.writerow([str(t.date), str(t.candle.type), str(t.candle.open), str(t.candle.close), str(
    #             t.candle.low), str(t.candle.high), str(t.candle.mean), str(t.indicator.movingAverageShortClose), str(t.indicator.movingAverageMediumClose), str(t.indicator.movingAverageLongClose), str(t.indicator.exponentialAverageClose), str(t.indicator.RSI), t.indicator.VWAP, t.pattern])


    # with open('rsi.csv', 'w', newline='') as csvfile:
    #     csvwriter = csv.writer(csvfile)
    #     csvwriter.writerow(["Date", "close", "Gain", "GainAverage",
    #                        "loseAverage", "Strngth Index", "RSI"])
    #     for t in Common.tickData:
    #         csvwriter.writerow([str(t.date), str(t.candle.close), str(t.candle.gain), str(t.candle.gainAverage), str(
    #             t.candle.loseAverage), str(t.indicator.relativeStrength), str(t.indicator.RSI)])
# API.init()
# strategy.init()
# DBHelper.init()
# execute.init()
# API.initLiveData(execute.onNewData)

# fetchAndAnalyseData()
# dict = {}
# i = 0
# for t in Common.tickData:
#     dict[i] = t.serialize()
#     i = i+1
# print(dict)
# exit()
# execute.init()
print("start")
try:
    print("_______________________________________________")
    print("Starting Flask")
    print("_______________________________________________")
    thread.start_new_thread(flaskApp.startFlask, ())

    print("_______________________________________________")
    print("Fetch Data")
    print("_______________________________________________")

    thread.start_new_thread(fetchAndAnalyseData, ())
except Exception as e:
    print("Can not start flask")
    print(e)


print("All Threads started")
while 1:
    time.sleep(1)
