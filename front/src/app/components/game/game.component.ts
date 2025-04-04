import { Component, inject } from '@angular/core';
import { BoardComponent } from '../board/board.component';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MancalaService } from '../../services/mancala.service';
import { Board } from '../../models/board';

@Component({
  selector: 'app-game',
  imports: [BoardComponent, CommonModule],
  templateUrl: './game.component.html',
  styleUrl: './game.component.css'
})
export class GameComponent {

  private route = inject(ActivatedRoute);
  private router = inject(Router);

  player1: string | null = null;
  player2: string | null = null;

  board: Board | null = null;

  constructor(private gameService: MancalaService) {}

  ngOnInit() {
    this.board = this.gameService.board;
    this.player1 = this.gameService.player1;
    this.player2 = this.gameService.player2;
    
  }


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
