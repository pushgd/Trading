import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { StrategyParameterComponentComponent } from '../strategy-parameter-component/strategy-parameter-component.component';
import { strategy } from '../common'

@Component({
  selector: 'app-strategy-component',
  templateUrl: './strategy-component.component.html',
  styleUrls: ['./strategy-component.component.css']
})
export class StrategyComponentComponent implements OnInit {

  @Input() symbolName = '';
  @ViewChild(StrategyParameterComponentComponent) strategyParameter!: StrategyParameterComponentComponent;
  selectedStrategy: number = -1;
  strategyList: strategy[] = [
    { index: 1, name: 'Steak', inUse: false },
    { index: 2, name: 'Pizza', inUse: false },
    { index: 3, name: 'Tacos', inUse: false }
  ];
  constructor() { }
  ngOnInit(): void {
  }
  addStrategy(): void {
    console.log("Add Strategy clicked ", this.symbolName, " ", this.selectedStrategy);
    this.strategyList.filter(s => s.index == this.selectedStrategy)[0].inUse = true;
  }
  saveClicked(s: strategy): void {
    console.log("Start button clicked ", s);
    console.log(this.strategyParameter.getParameters())
  }
  removeClicked(s: strategy): void {
    console.log("Remove button clicked ", s);
    console.log(this.strategyParameter.getParameters())
    s.inUse = false;
  }
}
