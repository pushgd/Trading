import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { MatTableModule } from '@angular/material/table';
import { AppComponent } from './app.component';
import { MainComponent } from './main/main.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ActivateButtonComponent } from './activate-button/activate-button.component';
import { MatDividerModule } from '@angular/material/divider'
import { MatButtonModule } from '@angular/material/button';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatSelectModule } from '@angular/material/select';
import { MatDatepickerModule } from '@angular/material/datepicker'
import { MatNativeDateModule } from '@angular/material/core'
import { ClipboardModule } from '@angular/cdk/clipboard';
import { StrategyComponentComponent } from './strategy-component/strategy-component.component';
import { StrategyParameterComponentComponent } from './strategy-parameter-component/strategy-parameter-component.component'
import { FormsModule } from '@angular/forms';
import { StrategySimulateComponentComponent } from './strategy-simulate-component/strategy-simulate-component.component';
import { StrategySimulateParametersComponentComponent } from './strategy-simulate-parameters-component/strategy-simulate-parameters-component.component';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { BackendServiceService } from './backend-service.service';
@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    ActivateButtonComponent,
    StrategyComponentComponent,
    StrategyParameterComponentComponent,
    StrategySimulateComponentComponent,
    StrategySimulateParametersComponentComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatTableModule,
    MatDividerModule,
    MatButtonModule,
    MatExpansionModule,
    MatSelectModule,
    FormsModule,
    MatDatepickerModule,
    MatNativeDateModule,
    ClipboardModule,
    MatIconModule,
    MatSnackBarModule
  ],
  providers: [BackendServiceService],
  bootstrap: [AppComponent]
})
export class AppModule {


}

