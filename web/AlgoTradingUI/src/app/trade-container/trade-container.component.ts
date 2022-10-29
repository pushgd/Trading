import { Component, Input, OnInit } from '@angular/core';
import { BackendServiceService } from '../backend-service.service';
import { tradeInfo } from '../common';

@Component({
  selector: 'app-trade-container',
  templateUrl: './trade-container.component.html',
  styleUrls: ['./trade-container.component.css']
})

export class TradeContainerComponent implements OnInit {
  @Input() symbol: string = "";
  @Input() tradingSymbol: string = "";
  @Input() getAllTrades: boolean = false;
  tradelist: tradeInfo[] = [];
  // backendService: BackendServiceService;
  refreshing: boolean = false;
  constructor(private backEndService: BackendServiceService) {
    // this.backendService = backEndService;
  }

  ngOnInit(): void {
    console.log("Trade container for ", this.symbol);
    if (this.getAllTrades) {
      this.backEndService.getAllTradesForSymbol(this.symbol).then(response => { this.tradelist = response });// run for first time for init
    } else {
      this.backEndService.getActiveTradesForSymbol(this.symbol).then(response => { this.tradelist = response });// run for first time for init
      setInterval(() => this.backEndService.getActiveTradesForSymbol(this.symbol).then(response => { this.tradelist = response }), 30000)// set interval for updates
    }
  }
  public onRefreshClicked() {
    this.refreshing = true;
    if (this.getAllTrades) {
      this.backEndService.getAllTradesForSymbol(this.symbol).then(response => { this.tradelist = response; this.refreshing = false });// run for first time for init
    } else {
      this.backEndService.getActiveTradesForSymbol(this.symbol).then(response => { this.tradelist = response; this.refreshing = false });
    }
  }
}
