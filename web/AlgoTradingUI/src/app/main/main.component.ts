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

  displayedColumns: string[] = ["table-position", "table-name", "table-activeButton", "table-strategy", "table-simulate"];
  symbolInfo: symbolInfo[] = [];
  dataSource = new MatTableDataSource(this.symbolInfo);
  strategyList: strategy[] = [];
  simulateColumnWidth = 25;
  strategyColumnWidth = 25;
  constructor(private backEndService: BackendServiceService) {
    backEndService.getAllSymbols()
      .then(response => { this.getSymbolCallback(response) });

    backEndService.getAllStrategies()
      .then(response => { this.getStrategyCallback(response) });
    setInterval(() => backEndService.getCurrentPrice().then(response => { this.onCurrentPricecallback(response) }), 5000);
  }

  getSymbolCallback(response: any) {
    for (let i = 0; i < response.length; i++) {
      let s: symbolInfo = {
        index: i,
        name: response[i].symbolName,
        tradingSymbol: response[i].tradingSymbol,
        exchangeCode: response[i].exchangeToken,
        currentPrice: 0
      }
      this.symbolInfo?.push(s);
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
    })
    this.strategySimulateComponent.forEach((sc) => {
      sc.initStrategyData(this.strategyList);
    })
  }

  onCurrentPricecallback(response: any) {
    for (let i = 0; i < this.symbolInfo.length; i++) {
      this.symbolInfo[i].currentPrice = response[this.symbolInfo[i].tradingSymbol]
    }

    console.log(response);
  }

  ngOnInit(): void {

  }
  sortData(sort: Sort) {
    console.log(sort);
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
