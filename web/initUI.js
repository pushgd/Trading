const getSymbolURL = 'http://127.0.0.1:8080/getallsymbols'
const getStrategyURL = 'http://127.0.0.1:8080/getallstrategy'
const activateSymbolURL = 'http://127.0.0.1:8080/activateSymbol/'
const deactivateSymbolURL = 'http://127.0.0.1:8080/deactivateSymbol/'


const symbolSelect = document.querySelector("#SymbolName");
const symbolID = document.querySelector("#SymbolID");
const riskFactor = document.querySelector("#RiskRatio");
const strategy = document.querySelector("#strategy");
const container = document.querySelector("#symbolContainer");

const symbolList = []

async function initSymbols() {

    const response = await fetch(getSymbolURL);
    const json = await response.json();
    console.log(json)

    for (let i = 0; i < json.length; i++) {
        option = document.createElement('option');
        option.value = json[i];
        option.innerHTML = json[i];
        symbolSelect.appendChild(option)
    }
}

async function initStrategy() {

    const response = await fetch(getStrategyURL);
    const json = await response.json();
    console.log("initSymbols");
    console.log(json)


    for (let i = 0; i < json.length; i++) {
        option = document.createElement('option');
        option.value = json[i];
        option.innerHTML = json[i]
        strategy.appendChild(option)
    }
}


initSymbols()
initStrategy()

const callFlask = async () => {
    const response = await fetch('http://127.0.0.1:8080/getData');
    const json = await response.json(); //extract JSON from the http response
    let data = 0
    let table = document.querySelector('#dataTable')
    open = []
    close = []
    high = []
    low = []
    date = []
    console.log(json)
    data = json.data
    for (let i = 0; i < json.length; i++) {
        let r = table.insertRow(-1)
        r.insertCell(0).innerHTML = data[i].date
        r.insertCell(1).innerHTML = data[i].open
        r.insertCell(2).innerHTML = data[i].close
        r.insertCell(3).innerHTML = data[i].high
        r.insertCell(4).innerHTML = data[i].low

        open.push(data[i].open)
        close.push(data[i].close)
        high.push(data[i].high)
        low.push(data[i].low)
        date.push(data[i].date)
    }

    TESTER = document.getElementById('graph');
    let trace = {
        x: date,
        close: close,
        open: open,
        high: high,
        low: low,
        type: 'candlestick'
    }
    var layout = {
        yaxis: {
            autorange: false,
            range: [10000, 18000],
            type: 'linear'
        },
        xaxis: {
            autorange: false
        }
    }
    Plotly.newPlot(TESTER, [trace], {
        margin: { t: 0 }
    }, layout);
}
// console.log("Calling flask")
// callFlask()
// console.log("Called flask")


async function addSymbolButtonAction() {
    if (symbolList.indexOf(symbolSelect.value) > -1) {
        alert("Symbol Already added");
        return;
    }
    div = document.createElement('div')
    div.className = "symbolInfo";
    div.id = "s_" + symbolSelect.value.replace('-', '_').replace(' ', '_');
    div.innerHTML = `
      <div class="headerText" id="symbolName" style = " font-size: x-large">${symbolSelect.value}</div>
      <div style = "display : flex; justify-content: center;;">
            <div class="headerText gain" id="currentPrice">Current Price</div>
               <div class="headerText" id="riskFactor">Risk Factor: ${riskFactor.value}</div>
            </div>
        </div>
        </div>
            <div class='tradeList'>
                
            </div>
    `;
    container.appendChild(div);
    symbolList[symbolList.length] = symbolSelect.value;

    // let xhr = new XMLHttpRequest();
    // xhr.open("POST", activateSymbolURL + symbolSelect.value, false);
    // console.log(xhr.send());
    // xhr.onload(function (data) {
    //     console.log(data);
    // })


    // console.log(strategy.options[0].selected);
    // for (let i = 0; i < strategy.options.length; i++) {
    //     if (strategy.options[i].selected) {
    //         console.log(strategy.options[i].value)
    //     }
    // }
    // for (o in strategy.options) {
    //     console.log(o)
    // }
}



addSymbolButton = document.querySelector("#addSymbolButton")
addSymbolButton.addEventListener('click', addSymbolButtonAction)


