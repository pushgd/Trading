const getCurrentPrinceSymbolURL = 'http://127.0.0.1:8080/getCurrentPrice/'
const getTradeURL = 'http://127.0.0.1:8080/getTrades/'

const lastUpdatedTime = []
for (let i = 0; i < symbolList.length; i++) {
    lastUpdatedTime[i].push(new Date().getTime());
}
async function updateSymbol() {
    for (let i = 0; i < symbolList.length; i++) {

        let response = await fetch(getCurrentPrinceSymbolURL + symbolList[i]);
        let json = await response.json();
        let currentvalue = container.querySelector("#s_" + symbolList[i].replace('-', '_').replace(' ', '_')).querySelector('#currentPrice').textContent;
        currentvalue = currentvalue.slice(currentvalue.indexOf(':') + 1, currentvalue.indexOf('(')).trim();
        let updateTime = currentvalue.slice(currentvalue.indexOf('(') + 1, currentvalue.indexOf(')') - 1)
        if (currentvalue != json['CURRENT_PRICE']) {
            lastUpdatedTime[i] = (new Date().getTime());
        }
        let currentPrice = parseFloat(json['CURRENT_PRICE']);
        container.querySelector("#s_" + symbolList[i].replace('-', '_').replace(' ', '_')).querySelector('#currentPrice').textContent = "Current Price : " + json['CURRENT_PRICE'] + " ( " + updateTime / 1000 + " )";
        let tradelist = container.querySelector("#s_" + symbolList[i].replace('-', '_').replace(' ', '_')).querySelector('.tradeList');
        updateTime = new Date().getTime() - lastUpdatedTime[i]
        response = await fetch(getTradeURL + symbolList[i]);
        json = await response.json();
        // console.log(json);

        tradelist.querySelector("#ID").querySelector("#value").textContent = json[json.length - 1]['ID'];
        tradelist.querySelector("#strategy").querySelector("#value").textContent = json[json.length - 1]['strategy'];
        let status = "Watiting For Entry";
        if (json[json.length - 1]['status'] == 1) {
            status = "Trade Not Started";
        } else if (json[json.length - 1]['status'] == 2) {
            status = "Trade Enterd";
        } else if (json[json.length - 1]['status'] == 3) {
            status = "Trade Completed";
        } else if (json[json.length - 1]['status'] == 4) {
            status = "Force Exit";
        }
        tradelist.querySelector("#status").querySelector("#value").textContent = status;
        tradelist.querySelector("#buyTrigger").querySelector("#value").textContent = json[json.length - 1]['buyTrigger'];
        tradelist.querySelector("#stoploss").querySelector("#value").textContent = json[json.length - 1]['stopLoss'];
        tradelist.querySelector("#takeProfit").querySelector("#value").textContent = json[json.length - 1]['takeProfit'];
        // tradelist.querySelector("#Exit").querySelector("#value").textContent = json['exitTime'];
        tradelist.querySelector("#exit").querySelector("#value").textContent = json[json.length - 1]['exitPrice'];
        tradelist.querySelector("#entryPrice").querySelector("#value").textContent = json[json.length - 1]['entryPrice'];

        if (json[json.length - 1]['status'] == 2) {
            tradelist.querySelector("#gain").querySelector("#value").textContent = currentPrice - parseFloat(json[json.length - 1]['entryPrice']);
            if (currentPrice < parseFloat(json[json.length - 1]['entryPrice'])) {
                tradelist.querySelector("#gain").style.color = 'red';
            } else {
                tradelist.querySelector("#gain").style.color = 'green';
            }
        }
        if (json[json.length - 1]['status'] == 3) {

            tradelist.querySelector("#gain").querySelector("#value").textContent = Math.abs(parseFloat(json[json.length - 1]['entryPrice']) - parseFloat(json[json.length - 1]['exitPrice']));
            if (parseFloat(json[json.length - 1]['exitPrice']) > parseFloat(json[json.length - 1]['entryPrice'])) {
                tradelist.querySelector("#gain").style.color = 'green';
            } else {
                tradelist.querySelector("#gain").style.color = 'red';
            }
        }
    }
}

let symbolUpdateIntervalId = window.setInterval(updateSymbol, 500);
