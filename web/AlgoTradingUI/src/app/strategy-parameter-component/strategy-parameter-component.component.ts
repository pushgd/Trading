import { Component, OnInit } from '@angular/core';

interface parameter {
  pos: number;
  name: string;
  type: string;
  value: any;
}

@Component({
  selector: 'app-strategy-parameter-component',
  templateUrl: './strategy-parameter-component.component.html',
  styleUrls: ['./strategy-parameter-component.component.css']
})
export class StrategyParameterComponentComponent implements OnInit {
  dataSource: parameter[] = [
    { pos: 1, name: "P1", type: "text", value: '' },
    { pos: 2, name: "P2", type: "number", value: '' },
    { pos: 3, name: "P3", type: "date", value: '' },
  ];
  displayedColumns: string[] = ["table-position", "table-parameter", "table-input"]
  constructor() { }

  ngOnInit(): void {
  }

  parameterUpdate(element: parameter): void {
    console.log("Updated");
    console.log(element);
  }
  public getParameters(): parameter[] {
    return this.dataSource;
  }
}
