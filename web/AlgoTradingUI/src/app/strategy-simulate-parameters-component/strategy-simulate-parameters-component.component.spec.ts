import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StrategySimulateParametersComponentComponent } from './strategy-simulate-parameters-component.component';

describe('StrategySimulateParametersComponentComponent', () => {
  let component: StrategySimulateParametersComponentComponent;
  let fixture: ComponentFixture<StrategySimulateParametersComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StrategySimulateParametersComponentComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StrategySimulateParametersComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
