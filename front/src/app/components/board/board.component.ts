import { Component, inject, Input, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Board } from '../../models/board';
import { MancalaService } from '../../services/mancala.service';
import { Router } from '@angular/router';

import { DialogModule } from 'primeng/dialog';

@Component({
  selector: 'app-board',
  imports: [CommonModule, DialogModule],
  templateUrl: './board.component.html',
  styleUrl: './board.component.css'
})
export class BoardComponent {

  private router = inject(Router);

  winnerModal: boolean = false;
  winner: string = '';
  finalStore1: string = '';
  finalStore2: string = '';

  @Input() player1 = '';
  @Input() player2 = '';
  @Input() board!: Board;
  pTurn: number = 1;

  player1Pits = signal<number[]>(Array(6).fill(2));
  player2Pits = signal<number[]>(Array(6).fill(0));
  stores = signal<number[]>([0, 0]);

  movePit: number = 1;

  constructor(private gameService: MancalaService) { }

  ngOnInit(): void {
    console.log('Board en BoardComponent:', this.board);
    console.log('pils:', this.board.pils);

    if (this.board && this.board.pils.length === 2) {
      console.log('Jugador 1:', this.board.pils[1]);
      console.log('Jugador 2:', this.board.pils[0]);

      this.player1Pits.set([...this.board.pils[1]]); // Clonar para evitar mutaciones inesperadas
      this.player2Pits.set([...this.board.pils[0]]);
      this.stores.set([this.board.store1, this.board.store2]);
      this.pTurn = this.board.turn;
    } else {
      console.warn('Board no tiene la estructura esperada');
    }
  }

  moveStones(column: number, fila: number): void {
    const pits = fila === 1 ? this.player1Pits() : this.player2Pits();

    if (fila === this.pTurn && pits[column] > 0) {
      console.log(`Jugador ${this.pTurn} movió las piedras de la casilla ${column}`);

      this.gameService.move(this.movePit, column, this.pTurn).subscribe({
        next: (resp) => {
          if ('message' in resp) { // Mensaje de error
            alert(resp.message);
            return;
          }

          if (resp.store1 + resp.store2 == 48) { // Fin de juego
            this.finalStore1 = resp.store1.toString();
            this.finalStore2 = resp.store2.toString();
            if (resp.store1 > resp.store2) {
              this.winner = `¡${this.player1} ha ganado!😎 `;
            } else if (resp.store1 < resp.store2) {
              this.winner = `¡${this.player2} ha ganado!😎 `;
            } else {
              this.winner = '¡Empate!🙃 ';
            }
            this.winnerModal = true;
          }

          this.board = structuredClone(resp);
          this.player1Pits.set([...resp.pils[1]]);
          this.player2Pits.set([...resp.pils[0]]);
          this.stores.set([resp.store1, resp.store2]);
          this.pTurn = resp.turn;
          this.movePit = this.pTurn === 1 ? 1 : 0;
        },
        error: (err) => {
          console.error('Error al mover piedras:', err);
          alert('Hubo un error al procesar el movimiento.');
        }
      });
    }
  }

  //updateBoard
  changeTurn(): void {
    if (this.pTurn == 1) {
      this.pTurn = 2;
      this.movePit = 0;
    }
    else {
      this.pTurn = 1;
      this.movePit = 1;
    }
  }

  closeModal(): void {
    this.winnerModal = false;
    this.router.navigate(['']);
  }
}
