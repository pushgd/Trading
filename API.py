from EdelweissAPIConnect import EdelweissAPIConnect
from EdelweissAPIConnect.feed import Feed
import json
import Common
import csv
import execute
from constants.intraday_interval import IntradayIntervalEnum
from constants.action import ActionEnum
import Constant
import datetime


APIKey = "QDFbQZIsst9A6A"
AppSecret = "62eM4#YaL+kX5!Rt"
reqId = "376366e6d20a3aef"
accid = "45055736"
userID = "45055736"

client = None
f = None


def init():
    global client
    client = EdelweissAPIConnect.EdelweissAPIConnect(APIKey, AppSecret, reqId, True)
    print('Logged in')

# authResponse = client.__GetAuthorization(reqId)


def initLiveData(callback):
    print('waiting for Data')
    s = []
    for key in Common.SymbolDict.keys():
        s.append(Common.SymbolDict[key].exchangeToken)
    global f
    f = Feed(accid, userID, "python-settings.ini")
    f.subscribe(s, callback)


def initLocalFile(callback):
    print("New Data is here local")
    i = 0
    for s in execute.symbolsList:
        print("Starting Simulating ",s.symbolName)
        d = Common.getTillDate()
        j = json.loads(s.gethHistoricalData(IntradayIntervalEnum.M5,str(d.year),str(d.month),str(d.day)))
        for candle in j['data'][50:] :
            c = {
                Constant.KEY_OPEN: candle[1],
                Constant.KEY_HIGH: candle[2],
                Constant.KEY_LOW: candle[3],
                Constant.KEY_CLOSE: candle[4],
                Constant.KEY_DATE: datetime.datetime.strptime(candle[0], "%Y-%m-%d %H:%M:%S"),
                Constant.KEY_VOLUME: candle[5]}
            callback(0, 0, s.exchangeToken,c)
        print("Completed Simulating ", s.symbolName)
    print("Done")


def placeOrder(TradingSymbol, Exchange, OrderType, Quantity, StreamingSymbol, LimitPrice, Duration="DAY", Disclosed_Quantity="0", TriggerPrice="0", productCode="NRML"):
    response = client.PlaceTrade(TradingSymbol, Exchange,ActionEnum.BUY, Duration, OrderType, Quantity,
                                 StreamingSymbol, LimitPrice, ProductCode=productCode)
    return response


def sellPosition(TradingSymbol, Exchange, OrderType, Quantity, StreamingSymbol, LimitPrice, Duration="DAY", disclosed_Quantity="0", triggerPrice="0", productCode="NRML"):
    response = client.PlaceTrade(TradingSymbol, Exchange, ActionEnum.SELL, Duration, OrderType, Quantity,
                                 StreamingSymbol, LimitPrice, ProductCode=productCode)
    return response

def getHistoricalData(Interval,AssetType,Symbol,ExchangeType,tillDate):
    return client.getIntradayChart(ExchangeType,AssetType,Symbol,Interval,tillDate,IncludeContinuousFutures = False)
