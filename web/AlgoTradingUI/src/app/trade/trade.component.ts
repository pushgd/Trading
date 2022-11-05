import { Component, OnInit, Input, SimpleChanges, ViewChild, Host } from '@angular/core';
import { MatStepper } from '@angular/material/stepper';
import { BackendServiceService } from '../backend-service.service';

import { tradeInfo } from '../common';

@Component({
  selector: 'app-trade',
  templateUrl: './trade.component.html',
  styleUrls: ['./trade.component.css']
})
export class TradeComponent implements OnInit {
  @Input() info: tradeInfo;
  @Input() symbol: string = '';
  @Input() allTrade: boolean = false;
  currentstep: number = 0;
  currentPrice: number = 0;
  // backendService: BackendServiceService;

  @ViewChild(MatStepper) progress!: MatStepper;
  constructor(private backEndService: BackendServiceService) {
    this.info = {
      index: 0,
      ID: "",
      exitPricce: 0,
      buyPrice: 0,
      qunatity: 0,
      pnl: 0,
      status: '',
      entryPrice: 0,
      entryTime: "",
      exitPrice: 0,
      exitTime: "",
      buyTriggerCall: 0,
      buyTriggerPut: 0,
      stopLoss: 0,
      takeProfit: 0,
      strategyName: "",
      gain: 0,
      startDate: "",
      buyDate: "",
      exitDate: "",
      timeOutDate: "",
      type: ""
    }
    // this.backendService = backEndService;

  }

  ngOnInit(): void {
    let step = 0; //step zero fro 'TRADE_STATUS.NOT_STARTED':
    switch (this.info.status) {
      case 'TRADE_STATUS.NOT_STARTED':
        step = 0;
        break;
      case 'TRADE_STATUS.LOOKING_FOR_ENTRY':
        step = 1;
        break;
      case 'TRADE_STATUS.ENTERED':
        step = 2;
        break;
      default:
        step = 3;

    }
    this.currentstep = step;
    try {
      this.currentPrice = this.backEndService.getCurrentPriceForSymbol(this.symbol).currentPrice;

    } catch (e) {
      console.log("CurrentPrice not found ");
    }
  }

  public getDate(time: string): string {
    let t = Number(time) * 1000;
    let d = new Date(time);
    // console.log(d);
    return d.toTimeString();
  }


}
