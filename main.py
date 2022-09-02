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
    if Common.localFile:
        API.initLocalFile(execute.onNewDataLocal)
    else:
        API.initLiveData(execute.onNewData)
    exit()


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
