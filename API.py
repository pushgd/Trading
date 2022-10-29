import os
import threading
import webbrowser

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
from constants.duration import DurationEnum
from constants.product_code import ProductCodeENum
import zipfile

import main
import storage

APIKey = "QDFbQZIsst9A6A"
AppSecret = "62eM4#YaL+kX5!Rt"
reqId = "1"
accid = "45055736"
userID = "45055736"

client = None
f = None


def init():
    global client,reqId
    try:
        client = EdelweissAPIConnect.EdelweissAPIConnect(APIKey, AppSecret, reqId, True)
    except:
        print('error logging in get new eqID')
        Common.copyToClipboard(accid)
        webbrowser.open_new('https://www.edelweiss.in/api-connect/login?api_key=QDFbQZIsst9A6A')
        return 0

    with zipfile.ZipFile("instruments.zip", 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())
    print('Logged in')
    return 1

def setReqID(request_id):
    global reqId
    reqId = request_id
    # storage.setSymbolInfo('App', 'reqId', reqId)
    main.startAnalysis()

# authResponse = client.__GetAuthorization(reqId)


def initLiveData(callback):

    s = []
    for key in Common.SymbolDict.keys():
        s.append(Common.SymbolDict[key].exchangeToken)
    global f
    f = Feed(accid, userID, "python-settings.ini")
    f.subscribe(s, callback)
    print('waiting for Data',datetime.datetime.now())




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


def placeOrder(TradingSymbol, Exchange, OrderType, Quantity, StreamingSymbol, LimitPrice, Duration=DurationEnum.DAY, Disclosed_Quantity="0", TriggerPrice="0", productCode=ProductCodeENum.NRML):
    response = None
    try:
        response = client.PlaceTrade(TradingSymbol, Exchange,ActionEnum.BUY, Duration, OrderType, Quantity,
                             StreamingSymbol, LimitPrice, ProductCode=productCode)
    except Exception as e:
        # try again #2
        try:
            response = client.PlaceTrade(TradingSymbol, Exchange, ActionEnum.BUY, Duration, OrderType, Quantity,
                                     StreamingSymbol, LimitPrice, ProductCode=productCode)
        except Exception as e:
            # try again #3
            try:
                response = client.PlaceTrade(TradingSymbol, Exchange, ActionEnum.BUY, Duration, OrderType, Quantity,
                                         StreamingSymbol, LimitPrice, ProductCode=productCode)
            except:
                print("Error purchasing")

    return response


def sellPosition(TradingSymbol, Exchange, OrderType, Quantity, StreamingSymbol, LimitPrice, Duration="DAY", disclosed_Quantity="0", triggerPrice="0",  productCode=ProductCodeENum.NRML):

    response = None
    try:
        response = client.PlaceTrade(TradingSymbol, Exchange, ActionEnum.SELL, DurationEnum.DAY, OrderType, Quantity,
                                     StreamingSymbol, LimitPrice, ProductCode=productCode)
    except Exception as e:
        # try again #2
        try:
            response = client.PlaceTrade(TradingSymbol, Exchange, ActionEnum.SELL, DurationEnum.DAY, OrderType,
                                         Quantity,
                                         StreamingSymbol, LimitPrice, ProductCode=productCode)
        except Exception as e:
            # try again #3
            try:
                response = client.PlaceTrade(TradingSymbol, Exchange, ActionEnum.SELL, DurationEnum.DAY, OrderType,
                                             Quantity,
                                             StreamingSymbol, LimitPrice, ProductCode=productCode)
            except:
                print("Error Selling")
    return response

def getHistoricalData(Interval,AssetType,Symbol,ExchangeType,tillDate):
    return client.getIntradayChart(ExchangeType,AssetType,Symbol,Interval,tillDate,IncludeContinuousFutures = False)
