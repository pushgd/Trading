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
console.log("Calling flask")
callFlask()
console.log("Called flask")

