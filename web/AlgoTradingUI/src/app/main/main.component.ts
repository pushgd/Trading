import { Component, OnInit, ViewChild } from '@angular/core';
import { Sort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

export interface tableElement {
  name: string;
  position: number;
}
const myDataArray: tableElement[] = [
  { position: 1, name: "ABC" },
  { position: 2, name: "DEF" },
  { position: 3, name: "GHI" },
  { position: 4, name: "JKL" }
];


@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})

export class MainComponent implements OnInit {

  displayedColumns: string[] = ["table-position", "table-name", "table-activeButton", "table-strategy", "table-simulate"]
  dataSource = new MatTableDataSource(myDataArray);
  constructor() { }



  ngOnInit(): void {
    console.log(" main Init ");
  }
  sortData(sort: Sort) {
    console.log(sort);
  }

}
