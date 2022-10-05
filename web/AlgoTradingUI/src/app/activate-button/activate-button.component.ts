import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-activate-button',
  templateUrl: './activate-button.component.html',
  styleUrls: ['./activate-button.component.css']
})
export class ActivateButtonComponent implements OnInit {

  @Input() symbolName = '';
  active: boolean = false;
  text: string = "Disabled";
  constructor() { }

  ngOnInit(): void {
    console.log(" ActiveButton Init ");
  }

  onClick(): void {
    console.log("Clicked " + this.symbolName);
    this.active = !this.active;
    this.text = this.active ? "Active" : "Disabled";
  }
}
