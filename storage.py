import json
def getSymbolInfo(symbol,key,default = None):
    jsonFile = open(f"storage/symbol/{symbol}.json", "r")
    data = json.load(jsonFile)
    if key in data:
        return data[key]
    else:
        return default


def setSymbolInfo(symbol,key,value):
    fileName = f"storage/symbol/{symbol}.json"
    jsonFile = open(fileName, "r")  # Open the JSON file for reading
    data = json.load(jsonFile)
    jsonFile.close()
    data[key] = value
    jsonFile = open(fileName, "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()
