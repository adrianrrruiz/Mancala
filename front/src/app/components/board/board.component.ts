import { Component, Input, signal, Signal, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Board } from '../../models/board';
import { MancalaService } from '../../services/mancala.service';

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
  pTurn : number = 1;

  player1Pits = signal<number[]>(Array(6).fill(2));
  player2Pits = signal<number[]>(Array(6).fill(0));
  stores = signal<number[]>([0, 0]);

  movePit : number = 1;

  constructor(private gameService: MancalaService) {}

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
  
  
  moveStones(column: number, fila: number): void {
      // Implementa la lógica de movimiento aquí.
      const pits = fila === 1 ? this.player1Pits() : this.player2Pits();

      if(fila === this.pTurn &&  pits[column] > 0){
        
        console.log(`Jugador ${this.pTurn} movió las piedras de la casilla ${column}`);
        this.gameService.move(this.movePit, column, this.pTurn).subscribe({
          next: (updBoard) => {
            this.board = structuredClone(updBoard);
            this.player1Pits.set([...updBoard.pils[1]]);
            this.player2Pits.set([...updBoard.pils[0]]);
            this.stores.set([updBoard.store1, updBoard.store2]);
          }
        })
        this.changeTurn();
      }
  }

  //updateBoard

  changeTurn(): void{
    if(this.pTurn == 1){
      this.pTurn = 2;
      this.movePit = 0;
    }
    else{
      this.pTurn = 1;
      this.movePit = 1;
    }
  }
    
  
    
}
