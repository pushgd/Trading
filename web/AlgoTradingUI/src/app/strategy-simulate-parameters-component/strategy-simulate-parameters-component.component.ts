import { Component, OnInit, Input } from '@angular/core';
import { parameter } from "../common"

@Component({
  selector: 'app-strategy-simulate-parameters-component',
  templateUrl: './strategy-simulate-parameters-component.component.html',
  styleUrls: ['./strategy-simulate-parameters-component.component.css']
})
export class StrategySimulateParametersComponentComponent implements OnInit {
  @Input() parameters: parameter[] = [];

  displayedColumns: string[] = ["table-position", "table-parameter", "table-input"]
  constructor() { }

  ngOnInit(): void {
  }
  parameterUpdate(p: parameter): void {

  }
  public getParameters(): parameter[] {
    return this.parameters;
  }

}
