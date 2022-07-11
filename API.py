from EdelweissAPIConnect import EdelweissAPIConnect, Feed
import json
import Common
import csv
APIKey = "QDFbQZIsst9A6A"
AppSecret = "62eM4#YaL+kX5!Rt"
reqId = "323631b6e4b02fd1"
accid = "45055736"
userID = "45055736"


def init():

    global client
    client = EdelweissAPIConnect(
        APIKey, AppSecret, reqId, True)
    print('Logged in')
    # authResponse = client.__GetAuthorization(reqId)


def initLiveData(callback):
    print('waiting for Data')
    s = []
    for key in Common.SymbolDict.keys():
        s.append(Common.SymbolDict[key].scripCode)
    f = Feed(accid, userID,"python-settings.ini")
    f.subscribe(s, callback)

def initLocalFile(callback):
    print("New Data is here local")
    i = 0
    with open('data.csv') as csvfile:
        fileReader = csv.DictReader(csvfile)
        # next(fileReader)
        for row in fileReader:
            print("Row ",str(i)," price ",row['price'])
            if i == 421:
                print(i)
            i = i+1
            callback(float(row['price']), float(row['volume']),row['symbol'])

