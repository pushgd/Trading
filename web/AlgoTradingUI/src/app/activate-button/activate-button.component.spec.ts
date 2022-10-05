import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActivateButtonComponent } from './activate-button.component';

describe('ActivateButtonComponent', () => {
  let component: ActivateButtonComponent;
  let fixture: ComponentFixture<ActivateButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ActivateButtonComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ActivateButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
