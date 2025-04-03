from pydantic import BaseModel
from entity.player import Player
from entity.board import Board 

class Game(BaseModel):
    playing: bool
    turn: int
    game_type: int
    player1: Player
    player2: Player
    board: Board
      
    
  
