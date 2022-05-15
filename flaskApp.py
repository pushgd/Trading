from flask import Flask, jsonify
from markupsafe import escape
import Common
app = Flask(__name__)


def startFlask():
    app.run(host='0.0.0.0', port='8080')


@app.route("/getData", methods=['GET'])
def getData():
    replay = {}
    replay['data'] = {}
    replay['length'] = Common.topIndex
    i = 0
    for t in Common.tickData:
        replay['data'][i] = t.serialize()
        i = i+1
    replay = jsonify(replay)
    replay.headers.add('Access-Control-Allow-Origin', '*')
    return replay
