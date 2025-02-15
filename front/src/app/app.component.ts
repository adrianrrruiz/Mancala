import { CommonModule } from '@angular/common';
import { Component, signal, Signal } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  imports: [CommonModule]
})
export class AppComponent {
  player1Pits: Signal<number[]> = signal(Array(6).fill(4)); // Casas jugador 1
  player2Pits: Signal<number[]> = signal(Array(6).fill(4)); // Casas jugador 2
  stores: Signal<number[]> = signal([0, 0]); // Almacenes de cada jugador

  moveStones(index: number, player: number): void {
    console.log(`Jugador ${player} movió las piedras de la casa ${index}`);
    // Implementa la lógica de movimiento aquí.
  }

  play(): void {
    console.log('Iniciando juego');
    // Implementa la lógica de juego aquí.
  }

  reset(): void {
    console.log('Reiniciando juego');
    // Implementa la lógica de reinicio aquí.
  }
}
