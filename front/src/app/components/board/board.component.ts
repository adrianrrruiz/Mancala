import { Component, Input, signal, Signal, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Board } from '../../models/board';

@Component({
  selector: 'app-board',
  imports: [CommonModule],
  templateUrl: './board.component.html',
  styleUrl: './board.component.css'
})
export class BoardComponent {

  @Input() player1 = '';
  @Input() player2 = '';
  @Input() board!: Board;

  player1Pits = signal<number[]>(Array(6).fill(2));
  player2Pits = signal<number[]>(Array(6).fill(0));
  stores = signal<number[]>([0, 0]);

  ngOnInit(): void {
    console.log('Board en BoardComponent:', this.board);
    console.log('pils:', this.board.pils);
  
    if (this.board && this.board.pils.length === 2) {
      console.log('Jugador 1:', this.board.pils[1]);
      console.log('Jugador 2:', this.board.pils[0]);
  
      this.player1Pits.set([...this.board.pils[1]]); // Clonar para evitar mutaciones inesperadas
      this.player2Pits.set([...this.board.pils[0]]);
      this.stores.set([this.board.store1, this.board.store2]);
    } else {
      console.warn('Board no tiene la estructura esperada');
    }
  }

  /*
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['board'] && this.board) {
      console.log('Board actualizado en BoardComponent:', this.board);
      this.player1Pits.set([...this.board.pils[1]]);
      this.player2Pits.set([...this.board.pils[0]]);
      this.stores.set([this.board.store1, this.board.store2]);
    }
  }
  */
  

  
  moveStones(index: number, player: number): void {
    console.log(`Jugador ${player} movió las piedras de la casa ${index}`);
      // Implementa la lógica de movimiento aquí.
}
  
    
  
    
}
