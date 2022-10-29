import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { StrategyParameterComponentComponent } from '../strategy-parameter-component/strategy-parameter-component.component';
import { strategy, parameter, symbolInfo } from '../common'
import { BackendServiceService } from '../backend-service.service';

@Component({
  selector: 'app-strategy-component',
  templateUrl: './strategy-component.component.html',
  styleUrls: ['./strategy-component.component.css']
})
export class StrategyComponentComponent implements OnInit {

  @Input() symbolName: string = '';
  // strategyListInput: strategy[] = [];
  @ViewChild(StrategyParameterComponentComponent) strategyParameter!: StrategyParameterComponentComponent;
  selectedStrategy: number = -1;
  strategyList: strategy[] = [];
  // strategyList: strategy[] = [
  //   { index: 1, name: 'MACrossoverup', inUse: false },
  //   { index: 2, name: 'Pizza', inUse: false },
  //   { index: 3, name: 'Tacos', inUse: false }
  // ];
  constructor(private backEndService: BackendServiceService) {

  }

  ngOnInit(): void {

  }

  public initStrategyData(strategyListInput: strategy[]): void {
    console.log("initStrategyData");
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
  }

  addStrategy(): void {

    this.strategyList.filter(s => s.index == this.selectedStrategy)[0].inUse = true;
  }

  public setStrategy(strategy: string, p: parameter[]) {
    console.log("set strategy ", strategy, " for ", this.symbolName);
    console.log("Parameters ", p);
    let s = this.strategyList.filter(s => s.name == strategy)[0];
    s.inUse = true;

    for (let i = 0; i < s.parameters.length; i++) {
      let key = s.parameters[i].name as keyof typeof p
      s.parameters[i].value = p[key]
      console.log(`setting parameter ${s.parameters[i].name} to ${p[key]}`)
    }

  }



  saveClicked(s: strategy): void {
    this.backEndService.startStrategy(this.symbolName, s.name, s.parameters)
    console.log(this.strategyParameter.getParameters().forEach((e => console.log(e.name, " ", e.value))));
  }
  removeClicked(s: strategy): void {
    this.backEndService.removeStrategy(this.symbolName, s.name)
    s.inUse = false;
  }
}
