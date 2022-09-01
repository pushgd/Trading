const getCurrentPrinceSymbolURL = 'http://127.0.0.1:8080/getCurrentPrice/'
const getTradeURL = 'http://127.0.0.1:8080/getTrades/'

const lastUpdatedTime = []
for (let i = 0; i < symbolList.length; i++) {
    lastUpdatedTime[i].push(new Date().getTime());
}

function createTradeDOM(symbol, tradeInfo) {
    let div = document.createElement('div');
    let status = "Watiting For Entry";
    if (tradeInfo['status'] == 1) {
        status = "Trade Started";
    } else if (json[json.length - 1]['status'] == 2) {
        status = "Trade Enterd";
    } else if (json[json.length - 1]['status'] == 3) {
        status = "Trade Completed";
    } else if (json[json.length - 1]['status'] == 4) {
        status = "Force Exit";
    }
    div.id = "t" + tradeInfo['ID'];
    div.className = 'tradeInfo';
    div.innerHTML =
        `<div id = "ID" class="textBlock">
            <div id="title">ID:</div>
            <div id="value">${tradeInfo['ID']}</div>
        </div>
        <div id="strategy" class="textBlock">
            <div id="title">Strategy:</div>
            <div id="value">${tradeInfo['strategyName']}</div>
        </div>
        <div id="status" class="textBlock">
            <div id="title">Status:</div>
            <div id="value">${status}</div>
        </div>
        <div id="buyTriggerCall" class="textBlock">
            <div id="title">Buy Trigger(Call):</div>
            <div id="value">${tradeInfo['buyTriggerCall']}</div>
        </div>
        <div id="buyTriggerPut" class="textBlock">
            <div id="title">Buy Trigger(Put):</div>
            <div id="value">${tradeInfo['buyTriggerPut']}</div>
        </div>
        <div id="entryPrice" class="textBlock">
            <div id="title">Entry Price:</div>
            <div id="value">${tradeInfo['entryPrice']}</div>
        </div>
        <div id="stoploss" class="textBlock">
            <div id="title">Stoploss:</div>
            <div id="value">${tradeInfo['stopLoss']}</div>
        </div>
        <div id="takeProfit" class="textBlock">
            <div id="title">TakeProfit:</div>
            <div id="value">${tradeInfo['takeProfit']}</div>
        </div>
        <div id="exit" class="textBlock">
            <div id="title">Exit:</div>
            <div id="value">${tradeInfo['exitPrice']}</div>
        </div>
        <div id="gain" class="textBlock">
            <div id="title">Gain:</div>
            <div id="value">${tradeInfo['gain']}</div>
        </div>
        <div id="ForceExit" class="exitButton button">
            ForceExit
        </div>`

    let tradelist = container.querySelector("#s_" + symbol.replace('-', '_').replace(' ', '_')).querySelector('.tradeList');
    tradelist.insertBefore(div, tradelist.firstElement)
}

function updateTradeDOM(symbol, tradeInfo, currentPrice) {
    let trade = container.querySelector("#s_" + symbol.replace('-', '_').replace(' ', '_')).querySelector('.tradeList').querySelector("#t" + tradeInfo['ID']);
    let status = "Watiting For Entry";
    if (tradeInfo['status'] == 1) {
        status = "Trade Started";
    } else if (json[json.length - 1]['status'] == 2) {
        status = "Trade Enterd";
    } else if (json[json.length - 1]['status'] == 3) {
        status = "Trade Completed";
    } else if (json[json.length - 1]['status'] == 4) {
        status = "Force Exit";
    }
    trade.querySelector("#status").querySelector("#value").textContent = status;
    trade.querySelector("#buyTriggerCall").querySelector("#value").textContent = tradeInfo['buyTriggerCall'];
    trade.querySelector("#buyTriggerPut").querySelector("#value").textContent = tradeInfo['buyTriggerPut'];
    trade.querySelector("#stoploss").querySelector("#value").textContent = tradeInfo['stopLoss'];
    trade.querySelector("#takeProfit").querySelector("#value").textContent = tradeInfo['takeProfit'];
    trade.querySelector("#exit").querySelector("#value").textContent = tradeInfo['exitPrice'];
    trade.querySelector("#entryPrice").querySelector("#value").textContent = tradeInfo['entryPrice'];
    let entryPrice = parseFloat(tradeInfo['entryPrice']);
    let color = 'green';
    if (currentPrice < entryPrice) {
        color = 'red';
    }
    trade.querySelector("#gain").querySelector("#value").textContent = tradeInfo['gain'];
    trade.querySelector("#gain").style.color = color;
    trade.querySelector("#gain").style.fontWeight = "bold";

}


async function updateSymbol() {
    for (let i = 0; i < symbolList.length; i++) {

        let response = await fetch(getCurrentPrinceSymbolURL + symbolList[i]);
        let json = await response.json();
        let currentvalue = container.querySelector("#s_" + symbolList[i].replace('-', '_').replace(' ', '_')).querySelector('#currentPrice').textContent;
        currentvalue = currentvalue.slice(currentvalue.indexOf(':') + 1, currentvalue.indexOf('(')).trim();

        let currentPrice = parseFloat(json['CURRENT_PRICE']);
        container.querySelector("#s_" + symbolList[i].replace('-', '_').replace(' ', '_')).querySelector('#currentPrice').textContent = "Current Price : " + json['CURRENT_PRICE'];
        let tradelist = container.querySelector("#s_" + symbolList[i].replace('-', '_').replace(' ', '_')).querySelector('.tradeList').querySelectorAll('.tradeInfo');

        response = await fetch(getTradeURL + symbolList[i]);
        let tradeInfoJSON = await response.json();
        // console.log(json);
        let jsonLength = Object.keys(tradeInfoJSON).length;
        //no new trade
        if (tradelist.length != jsonLength) {
            for (let t = 0; t < jsonLength; t++) {
                createTradeDOM(symbolList[i], tradeInfoJSON[t])
            }

        } else {
            for (let t = 0; t < jsonLength; t++) {
                updateTradeDOM(symbolList[i], tradeInfoJSON[t], currentPrice)
            }
        }

    }
}



let symbolUpdateIntervalId = window.setInterval(updateSymbol, 500);
