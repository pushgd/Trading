const getCurrentPrinceSymbolURL = 'http://127.0.0.1:8080/getCurrentPrice/'
const getTradeURL = 'http://127.0.0.1:8080/getTrades/'

async function updateSymbol() {
    for (let i = 0; i < symbolList.length; i++) {
        let response = await fetch(getCurrentPrinceSymbolURL + symbolList[i]);
        let json = await response.json();
        container.querySelector("#s_" + symbolList[i]).querySelector('#currentPrice').textContent = "Current Price : " + json['CURRENT_PRICE'];
        let tradelist = container.querySelector("#s_" + symbolList[i]).querySelector('.tradeList');

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

    }
}

let symbolUpdateIntervalId = window.setInterval(updateSymbol, 500);
