import { CommonModule } from '@angular/common';
import { Component, signal, Signal } from '@angular/core';
import { StartComponent } from './components/start/start.component';
import { RouterModule } from '@angular/router';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  imports: [CommonModule, RouterModule ]
})
export class AppComponent {
  
}
