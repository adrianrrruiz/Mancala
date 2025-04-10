import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Board } from '../models/board';

@Injectable({
  providedIn: 'root'
})
export class MancalaService {
  private apiUrl = 'http://localhost:8000/game';


  constructor(private http: HttpClient) { }

  board: Board | null = null;
  player1: string | null = null;
  player2: string | null = null;


  startGame(player1: string, player2: string, mode: number): Observable<Board> {
    const body = {
      player1,
      player2,
      mode
    };
    return this.http.post<Board>(`${this.apiUrl}/start`, body);
  }

  move(row: number, col: number, player: number): Observable<Board | { message: string }> {
    return this.http.get<Board | { message: string }>(
      `${this.apiUrl}/movement?row=${row}&col=${col}&player=${player}`
    );
  }


  getBoardState(): Observable<any> {
    return this.http.get(`${this.apiUrl}/get-game`);
  }


}
