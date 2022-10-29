import { Component, OnInit, ViewChild, QueryList, ViewChildren } from '@angular/core';
import { Sort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { BackendServiceService } from '../backend-service.service';
import { symbolInfo, strategy, parameter } from '../common'
import { MatTable } from '@angular/material/table';
import { StrategyComponentComponent } from '../strategy-component/strategy-component.component';
import { StrategySimulateComponentComponent } from '../strategy-simulate-component/strategy-simulate-component.component';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})

export class MainComponent implements OnInit {
  @ViewChild(MatTable) matTable?: MatTable<symbolInfo>;
  @ViewChildren(StrategyComponentComponent) strategyComponent!: QueryList<StrategyComponentComponent>;
  @ViewChildren(StrategySimulateComponentComponent) strategySimulateComponent!: QueryList<StrategySimulateComponentComponent>;

  // displayedColumns: string[] = ["table-position", "table-name", "table-strategy", "table-trades", "table-all-trades", "table-simulate"];
  displayedColumns: string[] = ["table-position", "table-name", "table-strategy", "table-trades", "table-all-trades", "table-simulate"];
  symbolInfo: symbolInfo[] = [];
  dataSource = new MatTableDataSource(this.symbolInfo);
  strategyList: strategy[] = [];
  symbolStrategyData: any[] = [];
  simulateColumnWidth = 25;
  strategyColumnWidth = 25;
  valueIncreased: boolean = false;
  constructor(private backEndService: BackendServiceService) {


    this.backEndService.getAllSymbols()
      .then(response => { this.getSymbolCallback(response) });
    this.backEndService.getAllStrategies()
      .then(response => { this.getStrategyCallback(response) });


    setInterval(() => this.backEndService.getCurrentPrice().then(response => { this.onCurrentPricecallback(response) }), 5000);
  }

  getSymbolCallback(response: any) {
    for (let i = 0; i < response.length; i++) {
      let s: symbolInfo = {
        index: i,
        name: response[i].symbolName,
        tradingSymbol: response[i].tradingSymbol,
        exchangeCode: response[i].exchangeToken,
        currentPrice: 0,
        lastPrice: 0,
      }
      this.symbolInfo?.push(s);
      let t = {
        name: response[i].symbolName,
        GannAnalysis: response[i].GannAnalysis,
        MACrossoverup: response[i].MACrossoverup
      }
      this.symbolStrategyData.push(t);
    }
    // this.dataSource = response
    this.matTable?.renderRows();

  }

  getStrategyCallback(response: any) {
    for (let i = 0; i < response.length; i++) {

      let s: strategy = {
        index: i,
        name: response[i].name,
        inUse: false,
        parameters: []
      }
      for (let j = 0; j < response[i].parameter.length; j++) {
        let p: parameter = {
          index: j,
          name: response[i].parameter[j].name,
          type: response[i].parameter[j].type,
          value: ""
        }
        s.parameters.push(p);
      }
      this.strategyList?.push(s);

    }

    this.strategyComponent.forEach((sc) => {
      sc.initStrategyData(this.strategyList);
    });
    this.strategySimulateComponent.forEach((sc) => {
      sc.initStrategyData(this.strategyList);
    });

    for (let i = 0; i < this.symbolStrategyData.length; i++) {
      this.strategyComponent.forEach((sc) => {
        if (sc.symbolName == this.symbolStrategyData[i].name) {
          if (this.symbolStrategyData[i].GannAnalysis)
            sc.setStrategy("GannAnalysis", this.symbolStrategyData[i].GannAnalysis)

          if (this.symbolStrategyData[i].MACrossoverup)
            sc.setStrategy("MACrossoverup", this.symbolStrategyData[i].MACrossoverup)

        }
      });
    }

  }

  onCurrentPricecallback(response: any) {
    for (let i = 0; i < this.symbolInfo.length; i++) {
      this.symbolInfo[i].lastPrice = this.symbolInfo[i].currentPrice
      this.symbolInfo[i].currentPrice = response[this.symbolInfo[i].tradingSymbol].currentPrice;

    }

    console.log(response);
  }

  ngOnInit(): void {

  }
  showTradeToggle(isChecked: any) {
    // if (isChecked) {
    //   this.displayedColumns.splice(this.displayedColumns.indexOf("table-all-trades"), 1);
    // } else {
    //   this.displayedColumns.push("table-all-trades");
    // }


  }


  simulateHeadClicked(): void {
    console.log("Simulate HEad clicked");
    if (this.simulateColumnWidth == 0) {
      this.simulateColumnWidth = 25;
    } else {
      this.simulateColumnWidth = 0;
    }
  }

  strategyHeadClicked(): void {
    if (this.strategyColumnWidth == 0) {
      this.strategyColumnWidth = 25;
    } else {
      this.strategyColumnWidth = 0;
    }
  }
}
