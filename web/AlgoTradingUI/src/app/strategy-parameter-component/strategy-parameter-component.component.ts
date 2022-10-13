import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { MatTable } from '@angular/material/table';
import { parameter } from '../common'

@Component({
  selector: 'app-strategy-parameter-component',
  templateUrl: './strategy-parameter-component.component.html',
  styleUrls: ['./strategy-parameter-component.component.css']
})
export class StrategyParameterComponentComponent implements OnInit {

  @ViewChild(MatTable) matTable?: MatTable<parameter>;
  @Input() parameters: parameter[] = [];
  displayedColumns: string[] = ["table-position", "table-parameter", "table-input"]
  constructor() {
  }

  ngOnInit(): void {
  }

  parameterUpdate(element: parameter): void {
    console.log("Updated");
    console.log(element);
  }
  public getParameters(): parameter[] {
    return this.parameters;
  }

}
