import { Injectable } from '@angular/core';
import { parameter, symbolTickInfo, tradeInfo } from './common';
@Injectable({
  providedIn: 'root'
})
export class BackendServiceService {
  symbolCurrentPrice: symbolTickInfo[] = [];
  constructor() {

    console.log("Service Constructor");
  }

  public async simulate(symbol: string, strategy: string, startDate: string, endDate: string): Promise<any> {
    // let result;
    // const options = {
    //   headers: {
    //     'Accept': 'application/json',
    //     'Content-Type': 'application/json'
    //   }, method: 'POST', body: `{"startDate":"${startDate}","endDate":"${endDate}","strategy":"${strategy}"}`
    // };
    // console.log(options.body);
    // fetch(`http://127.0.0.1:8080/simulate/${symbol}`, options)
    //   .then(response => response.json())
    //   .then(response => {
    //     result = response;
    //     console.log(response);
    //   })
    //   .catch(err => console.error(err));
    // let response = await fetch(`http://127.0.0.1:8080/simulate/${symbol}`, options);
    const options = { method: 'GET' };

    let response = await fetch(`http://127.0.0.1:8080/simulate/${symbol}?startDate=${startDate}&endDate=${endDate}&strategy=${strategy}`, options);
    let json = await response.json();
    // console.log(json)
    return json;
  }

  public async getAllSymbols() {
    const options = { method: 'GET' };

    let response = await fetch(`http://127.0.0.1:8080/getallSymbols`, options);
    let json = await response.json();
    return json;
  }
  public async getAllStrategies() {
    const options = { method: 'GET' };

    let response = await fetch(`http://127.0.0.1:8080/getallStrategy`, options);
    let json = await response.json();
    return json;
  }

  public async getCurrentPrice() {
    const options = { method: 'GET' };
    try {
      let response = await fetch(`http://127.0.0.1:8080/getCurrentPrice/all`, options);
      let json = await response.json();
      this.symbolCurrentPrice = json as symbolTickInfo[];
      return this.symbolCurrentPrice;
    } catch (e) {
      console.log("Error getting current price")
      return [];
    }
  }

  public getCurrentPriceForSymbol(symbol: string): any {
    let s = symbol as keyof typeof this.symbolCurrentPrice
    return this.symbolCurrentPrice[s];
  }

  public async startStrategy(symbol: string, strategy: string, parameters: parameter[]): Promise<any> {
    // let result;
    let p = "";
    for (let i = 0; i < parameters.length; i++) {
      p += `,"${encodeURIComponent(parameters[i].name)}":"${encodeURIComponent(parameters[i].value)}"`;
    }
    const options = {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }, method: 'POST', body: `{"strategy":"${encodeURIComponent(strategy)}"${p}}`
    };
    console.log(options.body);
    let response = await fetch(`http://127.0.0.1:8080/setStrategy/${symbol}`, options);
    let json = await response.json();

    // let response = await fetch(`http://127.0.0.1:8080/simulate/${symbol}`, options);

    return json;
  }
  public async removeStrategy(symbol: string, strategy: string): Promise<any> {
    // let result;
    const options = {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }, method: 'POST', body: `{"strategy":"${encodeURIComponent(strategy)}"}`
    };
    console.log(options.body);
    let response = await fetch(`http://127.0.0.1:8080/removeStrategy/${symbol}`, options);
    let json = await response.json();

    // let response = await fetch(`http://127.0.0.1:8080/simulate/${symbol}`, options);

    return json;
  }



  public async getActiveTradesForSymbol(symbol: string) {
    const options = { method: 'GET' };

    let response = await fetch(`http://127.0.0.1:8080/getActiveTrades/${symbol}`, options);
    let json = await response.json();
    return json as tradeInfo[];
  }
  public async getAllTradesForSymbol(symbol: string) {
    const options = { method: 'GET' };

    let response = await fetch(`http://127.0.0.1:8080/getTrades/${symbol}`, options);
    let json = await response.json();
    console.log(json);
    return json as tradeInfo[];
  }
}
