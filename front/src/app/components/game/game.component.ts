import { Component, inject } from '@angular/core';
import { BoardComponent } from '../board/board.component';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-game',
  imports: [BoardComponent, CommonModule],
  templateUrl: './game.component.html',
  styleUrl: './game.component.css'
})
export class GameComponent {

  private route = inject(ActivatedRoute);
  private router = inject(Router);

  player1 = this.route.snapshot.paramMap.get('player1') ?? '';
  player2 = this.route.snapshot.paramMap.get('player2') ?? '';


  get mode(): 'vs-player' | 'vs-machine' | 'machine-vs-machine' {
    if (this.player1 && this.player2) return 'vs-player';
    if (this.player1 && !this.player2) return 'vs-machine';
    return 'machine-vs-machine';
  }
  reset(): void {
    console.log('Reiniciando juego');
    this.router.navigate(['']);
  }
}
