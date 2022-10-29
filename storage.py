import json
import os
def getSymbolInfo(symbol,key,default = None):
    jsonFile = open(f"storage/symbol/{symbol}.json", "r")
    data = json.load(jsonFile)
    if key in data:
        return data[key]
    else:
        return default
def isSymbolInfoExist(symbol,key):
    jsonFile = open(f"storage/symbol/{symbol}.json", "r")
    data = json.load(jsonFile)
    return key in data

def setSymbolInfo(symbol,key,value):
    fileName = f"storage/symbol/{symbol}.json"
    jsonFile = open(fileName, "r")  # Open the JSON file for reading
    data = json.load(jsonFile)
    jsonFile.close()
    data[key] = value
    jsonFile = open(fileName, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def removeSymbolInfo(symbol,key):
    fileName = f"storage/symbol/{symbol}.json"
    jsonFile = open(fileName, "r")  # Open the JSON file for reading
    data = json.load(jsonFile)
    jsonFile.close()
    data.pop(key,'None')
    jsonFile = open(fileName, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()



def setTradeInfo(symbolName,trade):
    if not os.path.isfile(f"storage/trade/{symbolName}.json"):
        with open(f"storage/trade/{symbolName}.json", 'w') as f:
            print("Storage file not Exist creating ")
            # adding tradeinfo to avoid creating blank json file
            json.dump({trade.ID: json.dumps(trade.serialize())}, f)
            return
    fileName = f"storage/trade/{symbolName}.json"
    jsonFile = open(fileName, "r")  # Open the JSON file for reading
    data = json.load(jsonFile)
    jsonFile.close()
    data[trade.ID] = json.dumps(trade.serialize())
    jsonFile = open(fileName, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()