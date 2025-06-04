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
  @Input() mode: 'p-p' | 'p-m' | 'm-m' = 'p-p';
  pTurn: number = 1;

  player1Pits = signal<number[]>(Array(6).fill(2));
  player2Pits = signal<number[]>(Array(6).fill(0));
  stores = signal<number[]>([0, 0]);
  selectedPit = signal<{ row: number, col: number } | null>(null);

  movePit: number = 1;

  constructor(private gameService: MancalaService) { }

  ngOnInit(): void {
    if (this.board && this.board.pils.length === 2) {
      this.player1Pits.set([...this.board.pils[1]]); // Clonar para evitar mutaciones inesperadas
      this.player2Pits.set([...this.board.pils[0]]);
      this.stores.set([this.board.store1, this.board.store2]);
      this.pTurn = this.board.turn;
      if (this.mode === 'm-m') {
        this.playMvsM();
      }
    } else {
      console.warn('Board no tiene la estructura esperada');
    }
  }

  moveStones(column: number, fila: number): void {
    const pits = fila === 1 ? this.player1Pits() : this.player2Pits();

    if (fila === this.pTurn && pits[column] > 0) {

      this.gameService.move(this.movePit, column, this.pTurn).subscribe({
        next: (resp) => {
          if ('message' in resp) { // Mensaje de error
            alert(resp.message);
            return;
          }

          if (resp.store1 + resp.store2 == 48) {
            this.endGame(resp);
          }

          this.setBoard(resp);

          if (this.mode === 'p-m' && this.pTurn === 2) {
            this.playMachine();
          }
        },
        error: (err) => {
          console.error('Error al mover piedras:', err);
          alert('Hubo un error al procesar el movimiento.');
        }
      });
    }
  }

  async playMvsM(): Promise<void> {
    while (this.board.store1 + this.board.store2 < 48) {
      await new Promise(resolve => setTimeout(resolve, 2000)); // Delay para visualización

      const currentPlayer = this.pTurn;
      const isGreedy = (currentPlayer === 1 ? this.player1 : this.player2) === 'greedy';
      const playFn = isGreedy ? this.gameService.playGreedy : this.gameService.playMinimax;

      const response = await new Promise<Board>((resolve, reject) => {
        playFn.call(this.gameService, currentPlayer).subscribe({
          next: (resp) => {
            if ('message' in resp) {
              alert(resp.message);
              reject(resp.message);
            } else {
              resolve(resp);
            }
          },
          error: (err) => {
            console.error('Error al mover IA:', err);
            alert('Error al procesar movimiento IA.');
            reject(err);
          }
        });
      });

      this.setBoard(response);

      await new Promise(resolve => setTimeout(resolve, 2000)); // Delay tras pintar

     
      // Si NO hubo turno extra, se cambia el turno automáticamente desde setBoard()
      // (porque actualizas this.pTurn allí).
      // Si hubo turno extra, simplemente no se cambia, y el bucle continúa con el mismo jugador.
    }
    this.endGame(this.board);
  }


  async playMachine(): Promise<void> {
    await new Promise(resolve => setTimeout(resolve, 2000)); // Esperar 3 segundos
    if (this.player2 === 'greedy') {
      this.gameService.playGreedy(2).subscribe({
        next: async (resp) => {
          console.log(resp)
          if ('message' in resp) { // Mensaje de error
            alert(resp.message);
            return;
          }
          if (resp.store1 + resp.store2 == 48) {
            this.endGame(resp);
          }
          this.setBoard(resp);
          await new Promise(resolve => setTimeout(resolve, 2000));

          // Si sigue siendo el turno 2, vuelve a llamar playMachine (turno extra)
          if (resp.turn === 2 && resp.store1 + resp.store2 < 48) {
            await this.playMachine();
          }
        }
      });
    } else {
      this.gameService.playMinimax(2).subscribe({
        next: async (resp) => {
          console.log(resp)
          if ('message' in resp) { // Mensaje de error
            alert(resp.message);
            return;
          }
          if (resp.store1 + resp.store2 == 48) {
            this.endGame(resp);
          }
          this.setBoard(resp);
          await new Promise(resolve => setTimeout(resolve, 2000));

          // Si sigue siendo el turno 2, vuelve a llamar playMachine (turno extra)
          if (resp.turn === 2 && resp.store1 + resp.store2 < 48) {
            await this.playMachine();
          }
        }
      });
    }
  }

  endGame(board: Board): void {
    if (board.store1 + board.store2 == 48) { // Fin de juego
      this.finalStore1 = board.store1.toString();
      this.finalStore2 = board.store2.toString();
      if (board.store1 > board.store2) {
        this.winner = `¡${this.player1} ha ganado!😎 `;
      } else if (board.store1 < board.store2) {
        this.winner = `¡${this.player2} ha ganado!😎 `;
      } else {
        this.winner = '¡Empate!🙃 ';
      }
      this.winnerModal = true;
    }
  }

  setBoard(board: Board): void {
    // Detectar qué casilla seleccionó la máquina
    if (this.mode === 'm-m' || (this.mode === 'p-m' && this.pTurn === 2)) {
      const oldPits1 = [...this.player1Pits()];
      const oldPits2 = [...this.player2Pits()];
      const newPits1 = [...board.pils[1]];
      const newPits2 = [...board.pils[0]];

      // Buscar en las casillas del jugador 1
      for (let i = 0; i < 6; i++) {
        if (oldPits1[i] > 0 && newPits1[i] === 0) {
          this.selectedPit.set({ row: 1, col: i });
          break;
        }
      }

      // Buscar en las casillas del jugador 2
      for (let i = 0; i < 6; i++) {
        if (oldPits2[i] > 0 && newPits2[i] === 0) {
          this.selectedPit.set({ row: 2, col: i });
          break;
        }
      }

      // Limpiar la selección después de 1 segundo
      setTimeout(() => {
        this.selectedPit.set(null);
      }, 1000);
    }

    this.board = structuredClone(board);
    this.player1Pits.set([...board.pils[1]]);
    this.player2Pits.set([...board.pils[0]]);
    this.stores.set([board.store1, board.store2]);
    this.pTurn = board.turn;
    this.movePit = this.pTurn === 1 ? 1 : 0;
  }

  closeModal(): void {
    this.winnerModal = false;
    this.router.navigate(['']);
  }
}
