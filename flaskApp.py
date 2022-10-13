
from random import randint, random
from flask import Flask, jsonify, request
from flask_cors import CORS
import Constant
import Common
import execute




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
       symbolList.append( {"symbolName": s.symbolName,"tradingSymbol" : s.tradingSymbol,"exchangeToken" : s.exchangeToken})

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
        replay[Common.SymbolDict[key].tradingSymbol]= Common.SymbolDict[key].lastTradedPrice

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
    replay = {}
    for trade in Common.SymbolDict[symbol].tradeList:
        replay[len(replay)] = trade.serialize()
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
    parameters = {'Quantity':int(request.json['Quantity'])}
    print(symbol+" "+str(strategy)+" "+str(parameters))
    Common.getSymbolBySymbolName(symbol).setStrategy(strategy,parameters)
    replay = jsonify(str(strategy)+" "+str(parameters))
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/simulate/<symbol>", methods=['GET'])
def simulate(symbol):
    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")
    strategy = request.args.get("strategy")
    print(symbol," ",startDate," ",endDate," ",strategy)
    replay = "reply"
    try:
        replay = jsonify(execute.simulate(symbol,startDate,endDate,strategy))
    except Exception as e:
        replay = jsonify(str(e))
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/deactivateSymbol/<symbol>", methods=['GET'])
def deactivateSymbol(symbol):
    execute.deactivateSymbol(symbol)
    replay = jsonify({'1':'1'})
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay
