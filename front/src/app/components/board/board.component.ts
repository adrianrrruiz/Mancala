import { Component, Input, signal, Signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-board',
  imports: [CommonModule],
  templateUrl: './board.component.html',
  styleUrl: './board.component.css'
})
export class BoardComponent {

  @Input() player1 = '';
  @Input() player2 = '';

  player1Pits: Signal<number[]> = signal(Array(6).fill(4)); // Casas jugador 1
  player2Pits: Signal<number[]> = signal(Array(6).fill(4)); // Casas jugador 2
  stores: Signal<number[]> = signal([0, 0]); // Almacenes de cada jugador
  
  moveStones(index: number, player: number): void {
    console.log(`Jugador ${player} movió las piedras de la casa ${index}`);
      // Implementa la lógica de movimiento aquí.
}
  
    
  
    
}
