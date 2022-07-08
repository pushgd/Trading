
from random import randint, random
from flask import Flask, jsonify
import Constant
import Common
app = Flask(__name__)
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app.logger.disabled = True
log.disabled = True

def startFlask():
    app.run(host='0.0.0.0', port='8080')


@app.route("/getData/<symbol>", methods=['GET'])
def getData(symbol):
    replay = {}
    replay['Hello'] = "Hello"

    replay = jsonify(replay)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/getallsymbols", methods=['GET'])
def getAllSymbols():
    replay = jsonify(list(Common.SymbolDict.keys()))
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay

@app.route("/getallstrategy", methods=['GET'])
def getAllStrategy():
    replay = jsonify(list(Common.strategyDict.keys()))
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay


@app.route("/getCurrentPrice/all", methods=['GET'])
def getCurrentPriceAll():
    replay = {}
    price = 1234
    for key in Common.SymbolDict.keys():
        replay[key]= price
        price = price + randint(1000,1500)

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
    replay = Common.SymbolDict[symbol].tradeList[0].__dict__.copy()
    replay.pop("symbol")
    replay.pop("strategy")
    replay = jsonify(replay)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay
