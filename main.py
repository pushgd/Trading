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
    # DBHelper.init()
    execute.init()


def fetchAndAnalyseDataForEquityAndIndex():
    API.init()
    # waitSomeTime()
    print("Fetch Started")
    init()

    API.initLiveData(execute.onNewData)
def waitSomeTime():
    startTime = datetime.datetime.now()
    timeDelta = 5
    if startTime.minute % timeDelta != 0:
        startTime = startTime + datetime.timedelta(minutes=(timeDelta - startTime.minute %timeDelta))
    else:
        return
    startTime = startTime.replace(second=0, microsecond=0)
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
    except Exception as e:
        print("Can not start flask")
        print(e)
    print("All Threads started")
    while 1:
        time.sleep(1)


print(__name__)
if __name__ == "__main__":
    main()
