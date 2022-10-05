import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StrategySimulateComponentComponent } from './strategy-simulate-component.component';

describe('StrategySimulateComponentComponent', () => {
  let component: StrategySimulateComponentComponent;
  let fixture: ComponentFixture<StrategySimulateComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StrategySimulateComponentComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StrategySimulateComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
