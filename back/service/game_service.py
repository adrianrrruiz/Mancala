from entity.game import Game
from entity.player import Player
from entity.board import Board

class GameService:
    _instance = None
    
    # Para que GameService se comporte como un Singleton
    def __new__(cls):
        if cls._instance is None:
          cls._instance = super(GameService, cls).__new__(cls)
          cls._instance.game = None
        return cls._instance

    def start_game(self, name_p1, name_p2, game_type) -> Board:
        p1 = Player(id=1, name=name_p1)
        p2 = Player(id=2, name=name_p2)
        
        board = Board(store1=0, store2=0, pils=[[4 for _ in range(6)] for _ in range(2)])
        
        self.game = Game(
            playing=True,
            turn=1, # Inicia jugador 1 siempre
            game_type=game_type,
            player1=p1,
            player2=p2,
            board=board
        )
        return self.game.board
    
    def get_game(self):
      return self.game
    
    def restart_game(self):
      self.game = None
      
    def make_movement(self, row, col, turn) -> Board:
      if self.game == None:
        return None
      
      rocks = self.game.board.pils[row][col]
      self.game.board.pils[row][col] = 0 
      
      while(rocks):
        if(row == 1): col+=1 # En la fila de abajo
        else: col -= 1 # En la fila de arriba
        
        if(col == 6): # Punto para el jugador 1
          self.game.board.store1 += 1
          row = 0
        elif(col == -1): # Punto para el jugador 2
          self.game.board.store2 += 1
          row = 1
        else: 
          self.game.board.pils[row][col] += 1
          
        rocks -= 1
      
      self.capture_rule(row, col, turn)
        
      return self.game.board
    
    def capture_rule(self, row, col, turn):
      if turn == 1 and row == 1 and self.game.board.pils[row][col] == 1: # Jugador 1, en la fila 2 y pill solo con una roca
        self.game.board.store1 += self.game.board.pils[row-1][col]
        self.game.board.pils[row-1][col] = 0
      elif turn == 2 and row == 0: # Jugador 2, en la fila 1 y pill solo con una roca
        self.game.board.store2 += self.game.board.pils[row+1][col]
        self.game.board.pils[row+1][col] = 0
        
              
          
