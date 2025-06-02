import { Component, inject } from '@angular/core';
import { BoardComponent } from '../board/board.component';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MancalaService } from '../../services/mancala.service';
import { Board } from '../../models/board';
import { HeaderComponent } from '../header/header.component';

@Component({
  selector: 'app-game',
  imports: [BoardComponent, CommonModule, HeaderComponent],
  templateUrl: './game.component.html',
  styleUrl: './game.component.css'
})
export class GameComponent {

  private router = inject(Router);

  player1: string | null = null;
  player2: string | null = null;

  board: Board | null = null;

  constructor(private gameService: MancalaService) { }

  ngOnInit() {
    this.board = this.gameService.board;
    this.player1 = this.gameService.player1;
    this.player2 = this.gameService.player2;
  }

  get mode(): 'p-p' | 'p-m' | 'm-m' {
    if ((this.player1 == 'greedy' || this.player1 == 'minimax') && (this.player2 == 'greedy' || this.player2 == 'minimax')) return 'm-m';
    if (this.player2 == 'greedy' || this.player2 == 'minimax') return 'p-m';
    return 'p-p';
  }

  reset(): void {
    console.log('Reiniciando juego');
    this.router.navigate(['']);
  }
}
