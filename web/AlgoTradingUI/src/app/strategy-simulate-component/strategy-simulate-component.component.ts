import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { StrategySimulateParametersComponentComponent } from '../strategy-simulate-parameters-component/strategy-simulate-parameters-component.component';
import { strategy } from '../common'
import { Clipboard } from '@angular/cdk/clipboard';

@Component({
  selector: 'app-strategy-simulate-component',
  templateUrl: './strategy-simulate-component.component.html',
  styleUrls: ['./strategy-simulate-component.component.css']
})
export class StrategySimulateComponentComponent implements OnInit {
  @Input() symbolName: string = "";
  @ViewChild(StrategySimulateParametersComponentComponent) parameter!: StrategySimulateParametersComponentComponent;
  selectedStrategy: number = -1;
  dateStart: string = '';
  dateEnd: string = '';
  simulateLogs: string = "Log will be here";
  constructor() { }
  strategyList: strategy[] = [
    { index: 1, name: "S1", inUse: false },
    { index: 2, name: "S2", inUse: false },
    { index: 3, name: "S3", inUse: false }

  ]
  ngOnInit(): void {
  }

  addStrategy(): void {
    this.strategyList.filter(s => s.index == this.selectedStrategy)[0].inUse = true;
  }

  simulateClicked(s: strategy): void {
    let parameters = this.parameter.getParameters();
    let startDate = new Date(this.dateStart);
    let endDate = new Date(this.dateEnd);
    this.simulateLogs = `starting Simulation from ${startDate.getFullYear() + "-" + startDate.getMonth() + "-" + startDate.getDate()} to ${endDate.getFullYear() + "-" + endDate.getMonth() + "-" + endDate.getDate()} \n`;
    parameters.forEach(p => this.simulateLogs = this.simulateLogs + ` ${p.name} = ${p.value} \n`)


  }

  removeClicked(s: strategy): void {
    s.inUse = false;
  }
}
