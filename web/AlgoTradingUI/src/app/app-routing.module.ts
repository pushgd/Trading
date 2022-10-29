import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StrategySimulateComponentComponent } from './strategy-simulate-component/strategy-simulate-component.component';

const routes: Routes = [
  { path: 'simulate', component: StrategySimulateComponentComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }