import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HeaderComponent } from '../header/header.component';
import { Board } from '../../models/board';
import { MancalaService } from '../../services/mancala.service';


@Component({
  selector: 'app-player-form',
  imports: [CommonModule, FormsModule, HeaderComponent],
  templateUrl: './player-form.component.html',
  styleUrl: './player-form.component.css'
})
export class PlayerFormComponent {
  mode = inject(ActivatedRoute).snapshot.data['mode']; // Obtiene el modo de juego
  player1 = '';
  player2 = '';
  private router = inject(Router);

  modeNumber = 0;

  constructor(private gameService: MancalaService) { }

  iniciarJuego() {
    if (this.mode === 'vs-player') {
      this.modeNumber = 1;
    } else if (this.mode === 'vs-machine') {
      this.modeNumber = 2;
    } else if (this.mode === 'machine-vs-machine') {
      this.modeNumber = 3;
    }

    this.gameService.startGame(this.player1, this.player2, this.modeNumber).subscribe({
      next: (data) => {
        this.gameService.board = data;
        this.gameService.player1 = this.player1;
        this.gameService.player2 = this.player2;
        this.router.navigate(['/game']);
      },
      error: (err) => {
        console.error('Error al iniciar juego', err);
      }
    });
  }
}
