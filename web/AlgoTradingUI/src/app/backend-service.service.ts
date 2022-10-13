import { Injectable } from '@angular/core';
import { parameter } from './common';
@Injectable({
  providedIn: 'root'
})
export class BackendServiceService {

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
      return json;
    } catch (e) {
      console.log("Error getting current price")
      return [];
    }
  }


  public async startStrategy(symbol: string, strategy: string, parameters: parameter[]): Promise<any> {
    // let result;
    let p = "";
    for (let i = 0; i < parameters.length; i++) {
      p += `"${encodeURIComponent(parameters[i].name)}":"${encodeURIComponent(parameters[i].value)}"`;
    }
    const options = {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }, method: 'POST', body: `{"strategy":"${encodeURIComponent(strategy)}",${p}}`
    };
    console.log(options.body);
    let response = await fetch(`http://127.0.0.1:8080/setStrategy/${symbol}`, options);
    let json = await response.json();

    // let response = await fetch(`http://127.0.0.1:8080/simulate/${symbol}`, options);

    console.log(json);
    console.log(p);
    return json;
  }
}
