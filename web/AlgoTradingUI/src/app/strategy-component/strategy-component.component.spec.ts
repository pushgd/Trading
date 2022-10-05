import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StrategyComponentComponent } from './strategy-component.component';

describe('StrategyComponentComponent', () => {
  let component: StrategyComponentComponent;
  let fixture: ComponentFixture<StrategyComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ StrategyComponentComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(StrategyComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
