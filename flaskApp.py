import json
from random import randint, random
from flask import Flask, jsonify, request
from flask_cors import CORS

import API
import Constant
import Common
import execute
import storage
import simulate
app = Flask(__name__)

cors = CORS(app)
def startFlask():
    app.run(host='0.0.0.0', port='8080')


@app.route("/getData/<symbol>", methods=['GET'])
def getData(symbol):
    replay = {}
    replay['Hello'] = "Hello"

    replay = jsonify(replay)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/getallSymbols", methods=['GET'])
def getAllSymbols():
    symbolList = []
    for s in execute.symbolsList:
        info = {"symbolName": s.symbolName,"tradingSymbol" : s.tradingSymbol,"exchangeToken" : s.exchangeToken}
        if storage.isSymbolInfoExist(s.symbolName,Constant.STRATEGY_GANN_ANALYSIS):
            info[Constant.STRATEGY_GANN_ANALYSIS] = storage.getSymbolInfo(s.symbolName,Constant.STRATEGY_GANN_ANALYSIS)
        if storage.isSymbolInfoExist(s.symbolName, Constant.STRATEGY_MA_CROSSOVER_UP):
           info[Constant.STRATEGY_MA_CROSSOVER_UP] = storage.getSymbolInfo(s.symbolName, Constant.STRATEGY_MA_CROSSOVER_UP)
        symbolList.append(info)

    replay = jsonify(symbolList)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/getallStrategy", methods=['GET'])
def getAllStrategy():
    replay = [{"name":Constant.STRATEGY_GANN_ANALYSIS,
               "parameter":Constant.STRATEGY_PARAMETER_GANN_ANALYSIS},
              {"name": Constant.STRATEGY_MA_CROSSOVER_UP,
               "parameter": Constant.STRATEGY_PARAMETER_MA_CROSSOVER_UP},
              ]
    replay = jsonify(replay)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay


@app.route("/getCurrentPrice/all", methods=['GET'])
def getCurrentPriceAll():
    replay = {}
    for key in Common.SymbolDict.keys():
        replay[Common.SymbolDict[key].tradingSymbol]= {'currentPrice':Common.SymbolDict[key].lastTradedPrice,'lastUpdate':str(Common.SymbolDict[key].lastUpdatedTime)}

    replay = jsonify(replay)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/getCurrentPrice/<symbol>", methods=['GET'])
def getCurrentPrice(symbol):
    replay = {}
    replay[Constant.KEY_CURRENT_PRICE] = Common.SymbolDict[symbol].lastTradedPrice
    replay = jsonify(replay)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/getlastCandle/<symbol>", methods=['GET'])
def getLastCandle(symbol):
    replay = {}
    replay[Constant.KEY_OPEN] = 1
    replay[Constant.KEY_HIGH] = 12
    replay[Constant.KEY_CLOSE] = 123
    replay[Constant.KEY_LOW] = 1234
    replay[Constant.KEY_SYMBOL] = symbol
    
    replay = jsonify(replay)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/getCandle/<symbol>/<index>", methods=['GET'])
def getCandle(symbol,index):
    replay = {}
    replay[Constant.KEY_OPEN] = 1
    replay[Constant.KEY_HIGH] = 12
    replay[Constant.KEY_CLOSE] = 123
    replay[Constant.KEY_LOW] = 1234
    replay[Constant.KEY_SYMBOL] = symbol
    replay[Constant.KEY_DATE] = index
    replay = jsonify(replay)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay


@app.route("/getTrades/<symbol>", methods=['GET'])
def getTrade(symbol):
    # s = Common.getSymbolBySymbolName(symbol)
    # replay = []
    # for trade in s.tradeList:
    #
    #     replay.append(trade.serialize())
    replay = jsonify(storage.getAllTradeInfo(symbol))
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay


@app.route("/getActiveTrades/<symbol>", methods=['GET'])
def getActiveTrades(symbol):
    s = Common.getSymbolBySymbolName(symbol)
    replay = []
    for trade in s.tradeList:
        if not (trade.status == Constant.TRADE_STATUS.COMPLETED or trade.status == Constant.TRADE_STATUS.TIMED_OUT):
            replay.append(trade.serialize())
    replay = jsonify(replay)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/exitTrades/<symbol>/<ID>", methods=['POST'])
def exitTrade(symbol,ID):
    Common.getSymbolBySymbolName(symbol).exitTrade(ID)


@app.route("/simulate1/<symbol>", methods=['POST'])
def simulate1(symbol):
    startDate = request.json['startDate']
    endDate = request.json['endDate']
    print(symbol," ",startDate," ",endDate)
    replay = "reply"
    replay = jsonify(execute.simulate(symbol,startDate,endDate,Constant.STRATEGY_MA_CROSSOVER_UP))
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/setStrategy/<symbol>", methods=['POST'])
def setStrategy(symbol):
    strategy = request.json['strategy']

    parameters = {}
    keys = list(request.json.keys())[1:]
    for k in keys:
        parameters[k]= request.json[k]
    print(symbol+" "+str(strategy)+" "+str(parameters))
    s = Common.getSymbolBySymbolName(symbol)
    storage.setSymbolInfo(s.symbolName,strategy,parameters)
    s.setStrategy(strategy,parameters)
    replay = jsonify(str(strategy)+" "+str(parameters))
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay
@app.route("/removeStrategy/<symbol>", methods=['POST'])
def removeStrategy(symbol):
    strategy = request.json['strategy']

    s = Common.getSymbolBySymbolName(symbol)
    storage.removeSymbolInfo(s.symbolName,strategy)
    # s.setStrategy(strategy)
    replay = jsonify(str(strategy)+" removed")
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/simulate/<symbol>", methods=['GET'])
def simulateSymbol(symbol):
    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")
    strategy = request.args.get("strategy")
    print(symbol," ",startDate," ",endDate," ",strategy)
    replay = "reply"
    # try:
    replay = jsonify(simulate.simulate(symbol,startDate,endDate,strategy))
    # except Exception as e:
    #     replay = jsonify(str(e))
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/deactivateSymbol/<symbol>", methods=['GET'])
def deactivateSymbol(symbol):
    execute.deactivateSymbol(symbol)
    replay = jsonify({'1':'1'})
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/setReqID", methods=['GET'])
def setID():
    replay = "reply"
    try:
        request_id = request.args.get("request_id")
        API.setReqID(request_id)
        print("requestID set to ",API.reqId)
        replay = jsonify("Completed")
    except Exception as e:
        replay = jsonify(str(e))
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay