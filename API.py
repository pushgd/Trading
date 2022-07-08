from EdelweissAPIConnect import EdelweissAPIConnect, Feed
import json
import Common
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
    print(s)
    f = Feed(s,accid, userID,callback)
    f.subscribe(["235127_MCX"], callback, subscribe_order=False)


def dataReceived(data):
    print("New Data is here")
    # try:
    #     print(d)
    #     d = json.loads(data)

    #     # print("open "+d['response']['data']['a0'])
    #     # print("high "+d['response']['data']['a1'])
    #     # print("low "+d['response']['data']['a2'])
    #     print("close "+d['response']['data']['a9'])
    #     print("close "+d['response']['data']['c6'])
    # except:
    #     print("error parsing" + data)
