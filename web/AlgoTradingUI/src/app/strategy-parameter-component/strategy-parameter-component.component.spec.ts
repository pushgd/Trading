import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StrategyParameterComponentComponent } from './strategy-parameter-component.component';

describe('StrategyParameterComponentComponent', () => {
  let component: StrategyParameterComponentComponent;
  let fixture: ComponentFixture<StrategyParameterComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StrategyParameterComponentComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StrategyParameterComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
