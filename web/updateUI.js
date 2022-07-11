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
        let currentvalue = container.querySelector("#s_" + symbolList[i]).querySelector('#currentPrice').textContent;
        currentvalue = currentvalue.slice(currentvalue.indexOf(':') + 1, currentvalue.indexOf('(')).trim();
        let updateTime = currentvalue.slice(currentvalue.indexOf('(') + 1, currentvalue.indexOf(')') - 1)
        if (currentvalue != json['CURRENT_PRICE']) {
            lastUpdatedTime[i] = (new Date().getTime());
        }

        container.querySelector("#s_" + symbolList[i]).querySelector('#currentPrice').textContent = "Current Price : " + json['CURRENT_PRICE'] + " ( " + updateTime / 1000 + " )";
        let tradelist = container.querySelector("#s_" + symbolList[i]).querySelector('.tradeList');
        updateTime = new Date().getTime() - lastUpdatedTime[i]
        response = await fetch(getTradeURL + symbolList[i]);
        json = await response.json();
        // console.log(json);

        tradelist.querySelector("#ID").querySelector("#value").textContent = json['ID'];
        tradelist.querySelector("#strategy").querySelector("#value").textContent = json['strategy'];
        let status = "Watiting For Entry";
        if (json['status'] == 1) {
            status = "Trade Not Started";
        } else if (json['status'] == 2) {
            status = "Trade Enterd";
        } else if (json['status'] == 3) {
            status = "Trade Completed";
        }
        tradelist.querySelector("#status").querySelector("#value").textContent = status;
        tradelist.querySelector("#buyTrigger").querySelector("#value").textContent = json['buyTrigger'];
        tradelist.querySelector("#stoploss").querySelector("#value").textContent = json['stopLoss'];
        tradelist.querySelector("#takeProfit").querySelector("#value").textContent = json['takeProfit'];
        // tradelist.querySelector("#Exit").querySelector("#value").textContent = json['exitTime'];
        tradelist.querySelector("#exit").querySelector("#value").textContent = json['exitPrice'];
        tradelist.querySelector("#entryPrice").querySelector("#value").textContent = json['entryPrice'];

        if (json['status'] == 3) {

            tradelist.querySelector("#gain").querySelector("#value").textContent = Math.abs(parseFloat(json['entryPrice']) - parseFloat(json['exitPrice']));
            if (parseFloat(json['exitPrice']) > parseFloat(json['entryPrice'])) {
                tradelist.querySelector("#gain").style.color = 'green';
            } else {
                tradelist.querySelector("#gain").style.color = 'red';
            }
        }
    }
}

let symbolUpdateIntervalId = window.setInterval(updateSymbol, 500);
