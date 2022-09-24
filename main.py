import datetime
import logging
import Constant
import strategy
import csv
import time
import _thread as thread
# import flaskApp
import Common
import execute
import API
import DBHelper
import flaskApp


def init():
    API.init()
    strategy.init()
    DBHelper.init()
    execute.init()


def fetchAndAnalyseDataForEquityAndIndex():
    print("Fetch Started")
    init()
    if Common.simulate:
        API.initLocalFile(execute.onNewDataLocal)
    else:
        waitSomeTime()
        API.initLiveData(execute.onNewData)
    exit()


def waitSomeTime():
    t = datetime.datetime.now()
    if t.minute % 15 != 0:
        t = t + datetime.timedelta(minutes=(15 - t.minute % 15))
    t = t.replace(second=0, microsecond=0)
    startTime = t
    timeToWait = startTime - datetime.datetime.now()
    print(f"wait for {timeToWait.seconds}  seconds")
    print(f"start time set to {startTime}")

    time.sleep(timeToWait.seconds)
    print(f"continue run {datetime.datetime.now()}")



def subsribeOptions():
    print("Subscribing for Options")
    time.sleep(10*60)


print("start")


def main():
    try:
        print("_______________________________________________")
        print("Starting Flask")
        print("_______________________________________________")
        thread.start_new_thread(flaskApp.startFlask, ())

        print("_______________________________________________")
        print("Fetch Data")
        print("_______________________________________________")

        thread.start_new_thread(fetchAndAnalyseDataForEquityAndIndex, ())
        # thread.start_new_thread(fetchAndAnalyseDataForEquityAndIndex, ())
    except Exception as e:
        print("Can not start flask")
        print(e)
    print("All Threads started")
    while 1:
        time.sleep(1)


print(__name__)
if __name__ == "__main__":
    main()
