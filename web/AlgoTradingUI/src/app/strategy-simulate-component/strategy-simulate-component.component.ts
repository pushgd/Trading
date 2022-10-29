import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { StrategySimulateParametersComponentComponent } from '../strategy-simulate-parameters-component/strategy-simulate-parameters-component.component';
import { strategy, parameter, symbolInfo } from '../common'
import { Clipboard } from '@angular/cdk/clipboard';
import { BackendServiceService } from '../backend-service.service';
import { MatSnackBar } from '@angular/material/snack-bar';


@Component({
  selector: 'app-strategy-simulate-component',
  templateUrl: './strategy-simulate-component.component.html',
  styleUrls: ['./strategy-simulate-component.component.css'],
})
export class StrategySimulateComponentComponent implements OnInit {
  @Input() symbolName: string = "";

  @ViewChild(StrategySimulateParametersComponentComponent) parameter!: StrategySimulateParametersComponentComponent;
  selectedStrategy: number = -1;
  strategyList: strategy[] = [];
  dateStart: string = '';
  dateEnd: string = '';
  simulateLogs: string = "Log will be here";
  constructor(private backEndService: BackendServiceService, private clipboard: Clipboard, private snackBar: MatSnackBar) { }
  // strategyList: strategy[] = [
  //   { index: 1, name: "MACrossoverup", inUse: false },
  //   { index: 2, name: "S2", inUse: false },
  //   { index: 3, name: "S3", inUse: false }

  // ]
  ngOnInit(): void {
  }

  addStrategy(): void {
    this.strategyList.filter(s => s.index == this.selectedStrategy)[0].inUse = true;
  }

  simulateClicked(s: strategy): void {

    let parameters = this.parameter.getParameters();
    let startDate = new Date(this.dateStart);
    let endDate = new Date(this.dateEnd);
    this.simulateLogs = `starting Simulation for ${this.symbolName} from ${startDate.getFullYear() + "-" + startDate.getMonth() + "-" + startDate.getDate()} to ${endDate.getFullYear() + "-" + endDate.getMonth() + "-" + endDate.getDate()} \n`;
    parameters.forEach(p => this.simulateLogs = this.simulateLogs + ` ${p.name} = ${p.value} \n`)
    this.backEndService.simulate(this.symbolName, s.name, startDate.getFullYear() + "-" + startDate.getMonth() + "-" + startDate.getDate(), endDate.getFullYear() + "-" + endDate.getMonth() + "-" + endDate.getDate())
      .then(response => this.simulateCallback(response));
  }

  public initStrategyData(strategyListInput: strategy[]): void {
    for (let i = 0; i < strategyListInput.length; i++) {
      let s: strategy = {
        index: strategyListInput[i].index,
        name: strategyListInput[i].name,
        inUse: false,
        parameters: []
      }
      for (let j = 0; j < strategyListInput[i].parameters.length; j++) {
        let p: parameter = {
          index: j,
          name: strategyListInput[i].parameters[j].name,
          type: strategyListInput[i].parameters[j].type,
          value: ""
        }
        s.parameters.push(p);
      }
      this.strategyList?.push(s);
    }
    // console.log(this.strategyList)
  }


  removeClicked(s: strategy): void {
    s.inUse = false;
  }

  simulateCallback(response: any): void {

    for (let i = 0; i < response.length; i++) {

      let t = response[i];
      console.log(response[i]);
      this.simulateLogs += "\n";
      this.simulateLogs += `-----------------------${t.status} \n`;
      this.simulateLogs += `Trade Identified => ${t.startDate} BuyTriggerCall =>${t.buyTriggerCall} BuyTriggerPut =>${t.buyTriggerPut} \n`;
      if (t.status != 'TRADE_STATUS.TIMED_OUT') {
        this.simulateLogs += `Buy => ${t.buyDate} EntryPrice => ${t.entryPrice} StopLoss => ${t.stopLoss} TakeProfit => ${t.takeProfit} \n`;
        this.simulateLogs += `Sell ${t.gain > 0 ? "Profit" : "Lose"} => ${t.exitDate} ExitPrice => ${t.exitPrice} Gain => ${t.gain}\n`;
      } else {
        this.simulateLogs += `Trade timeOut => ${t.exitDate}\n`;
      }
      this.simulateLogs += "-----------------------\n";
    }
    this.copyToClipBoard();
  }

  copyToClipBoard(): void {
    this.clipboard.copy(this.simulateLogs);
    this.snackBar.open("Copied to Clipboard", "Dismiss", { duration: 1000 });

  }

}
