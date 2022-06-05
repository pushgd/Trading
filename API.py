from EdelweissAPIConnect import EdelweissAPIConnect, Feed
import json
APIKey = "QDFbQZIsst9A6A"
AppSecret = "62eM4#YaL+kX5!Rt"
reqId = "64323ae35e2e3970"
accid = "45055736"
userID = "45055736"


def init():

    global client
    client = EdelweissAPIConnect(
        APIKey, AppSecret, reqId, True, conf="python-settings.ini")
    # authResponse = client.__GetAuthorization(reqId)


def initLiveData(callback):
    f = Feed(accid, userID, "python-settings.ini")
    f.subscribe(["235127_MCX"], callback, subscribe_order=False)


def dataReceived(data):
    print("New Data is here")
    try:
        d = json.loads(data)
    # print(d)
        # print("open "+d['response']['data']['a0'])
        # print("high "+d['response']['data']['a1'])
        # print("low "+d['response']['data']['a2'])
        print("close "+d['response']['data']['a9'])
        print("close "+d['response']['data']['c6'])
    except:
        print("error parsing" + data)
