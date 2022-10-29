import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TradeContainerComponent } from './trade-container.component';

describe('TradeContainerComponent', () => {
  let component: TradeContainerComponent;
  let fixture: ComponentFixture<TradeContainerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TradeContainerComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TradeContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
