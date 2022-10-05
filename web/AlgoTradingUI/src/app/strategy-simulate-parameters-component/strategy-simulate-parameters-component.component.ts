import { Component, OnInit } from '@angular/core';
import { parameter } from "../common"

@Component({
  selector: 'app-strategy-simulate-parameters-component',
  templateUrl: './strategy-simulate-parameters-component.component.html',
  styleUrls: ['./strategy-simulate-parameters-component.component.css']
})
export class StrategySimulateParametersComponentComponent implements OnInit {

  dataSource: parameter[] = [
    { pos: 1, name: "P1", type: "text", value: "" },
    { pos: 2, name: "P2", type: "text", value: "" },
    { pos: 3, name: "P3", type: "text", value: "" }
  ]
  displayedColumns: string[] = ["table-position", "table-parameter", "table-input"]
  constructor() { }

  ngOnInit(): void {
  }
  parameterUpdate(p: parameter): void {

  }
  public getParameters(): parameter[] {
    return this.dataSource;
  }

}
