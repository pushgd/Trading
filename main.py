import datetime
import logging
import sys
import threading

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
import os




def fetchAndAnalyseDataForEquityAndIndex():
    if API.init() == 0:
        print("Error logging In")
        thread.exit()
        return
    # waitSomeTime()
    execute.init()
    print("Fetch Started")



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
def startAnalysis():
    thread.start_new_thread(fetchAndAnalyseDataForEquityAndIndex, ())
def main():
    try:
        print("_______________________________________________")
        print("Starting Flask")
        print("_______________________________________________")
        thread.start_new_thread(flaskApp.startFlask, ())

        print("_______________________________________________")
        print("Fetch Data")
        print("_______________________________________________")
        startAnalysis()


        API.initLiveData(execute.onNewData)
    except Exception as e:
        print("Can not start flask")
        print(e)
    print("All Threads started")


    while 1:
        try:
            diff = datetime.datetime.now() - execute.lastUpdateTime
            if diff.seconds >130:
                print("restarting API")
                API.initLiveData(execute.onNewData)
                execute.lastUpdateTime = datetime.datetime.now()
            time.sleep(1)
        except KeyboardInterrupt as e:
            print('Keyboad Interrupt stopping')
            os._exit(0)


print(__name__)
if __name__ == "__main__":
    main()
