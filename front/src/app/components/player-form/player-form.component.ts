import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Component , inject} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HeaderComponent } from '../header/header.component';

@Component({
  selector: 'app-player-form',
  imports: [ CommonModule, FormsModule],
  templateUrl: './player-form.component.html',
  styleUrl: './player-form.component.css'
})
export class PlayerFormComponent {
  mode = inject(ActivatedRoute).snapshot.data['mode']; // Obtiene el modo de juego
  player1 = '';
  player2 = '';
  private router = inject(Router);
  iniciarJuego() {
    if (this.mode === 'vs-player') {
      this.router.navigate(['/game', this.player1, this.player2]);
    } else if (this.mode === 'vs-machine') {
      this.router.navigate(['/game', this.player1]);
    } else if (this.mode === 'machine-vs-machine') {
      this.router.navigate(['/game']);
    }
  }
}
