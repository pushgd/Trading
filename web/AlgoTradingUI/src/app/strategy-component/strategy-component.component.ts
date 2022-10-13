import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { StrategyParameterComponentComponent } from '../strategy-parameter-component/strategy-parameter-component.component';
import { strategy, parameter } from '../common'
import { BackendServiceService } from '../backend-service.service';

@Component({
  selector: 'app-strategy-component',
  templateUrl: './strategy-component.component.html',
  styleUrls: ['./strategy-component.component.css']
})
export class StrategyComponentComponent implements OnInit {

  @Input() symbolName: string = '';
  @Input("strategyList") strategyListInput: strategy[] = [];
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
  saveClicked(s: strategy): void {
    this.backEndService.startStrategy(this.symbolName, s.name, s.parameters)
    console.log(this.strategyParameter.getParameters().forEach((e => console.log(e.name, " ", e.value))));
  }
  removeClicked(s: strategy): void {

    console.log(this.strategyParameter.getParameters())
    s.inUse = false;
  }
}
