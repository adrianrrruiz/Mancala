import { Component, inject } from '@angular/core';
import { HeaderComponent } from '../header/header.component';
import { Router } from '@angular/router';

@Component({
  selector: 'app-start',
  imports: [HeaderComponent],
  templateUrl: './start.component.html',
  styleUrl: './start.component.css'
})
export class StartComponent {

  private router = inject(Router); // Inyección directa sin constructor

  player_vs_player() {
    this.router.navigate(['/vs-player']);
  }
  player_vs_machine(): void {
    this.router.navigate(['/vs-machine']);
  }
  machine_vs_machine(): void {
    this.router.navigate(['/machine-vs-machine']);
  }

}
