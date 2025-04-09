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
        
        board = Board(store1=0, store2=0, pils=[[4 for _ in range(6)] for _ in range(2)], turn=1)
        
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
      if self.game is None or self.game.playing is False:
          return None

      board = self.game.board
      rocks = board.pils[row][col]
      if rocks == 0:
          return board  # Movimiento inválido, pozo vacío

      print(f"[DEBUG] Jugador {turn} movió desde ({row},{col}) con {rocks} piedras.")
      
      board.pils[row][col] = 0  # Vaciar el pit del jugador actual
      current_row, current_col = row, col
      last_pos = None

      while rocks > 0:
        # Movimiento antihorario
        if current_row == 1:  # fila jugador 1 (abajo → derecha)
            if current_col < 5:
                current_col += 1
            else:
                if turn == 1:
                    board.store1 += 1
                    rocks -= 1
                    if rocks == 0:
                        last_pos = ("store", 1)
                current_row = 0
                current_col = 6
                continue  # saltar si no se sembró
            board.pils[1][current_col] += 1
            rocks -= 1
            if rocks == 0:
                last_pos = (1, current_col)

        else:  # fila jugador 2 (arriba → izquierda)
            if current_col > 0:
                current_col -= 1
            else:
                if turn == 2:
                    board.store2 += 1
                    rocks -= 1
                    if rocks == 0:
                        last_pos = ("store", 2)
                current_row = 1
                current_col = -1
                continue  # saltar si no se sembró
            board.pils[0][current_col] += 1
            rocks -= 1
            if rocks == 0:
                last_pos = (0, current_col)

      print(f"[DEBUG] Última semilla cayó en: {last_pos}")
      print(f"[DEBUG] Estado actual del tablero: {board.pils}")
      
      # Aplicar regla de captura
      if isinstance(last_pos, tuple) and isinstance(last_pos[0], int):
          self.capture_rule(*last_pos, turn)

      # Verificar fin del juego
      winner = self.check_end_game()
      if winner:
          return winner

      # Verificar turno extra
      if last_pos == ("store", turn):
          pass  # mismo jugador repite turno
      else:
          self.game.turn = 2 if turn == 1 else 1

      board.turn = self.game.turn
      return board

    
    
    def _advance_position(self, row, col, turn):
      if row == 1:
          col += 1
          if col == 6:
              return ("store", 1) if turn == 1 else (0, 5)
          return (1, col)
      else:  # row == 0
          col -= 1
          if col == -1:
              return ("store", 2) if turn == 2 else (1, 0)
          return (0, col)


    
    def capture_rule(self, row, col, turn):
      # Verifica si cayó en su lado y la casilla tenía solo 1 semilla (es decir, estaba vacía antes de caer ahí la última)
      if turn == 1 and row == 1 and self.game.board.pils[row][col] == 1:
          opposite = self.game.board.pils[0][col]
          if opposite > 0:
              # Suma la semilla propia + las del lado contrario
              self.game.board.store1 += opposite + 1
              self.game.board.pils[0][col] = 0
              self.game.board.pils[1][col] = 0

      elif turn == 2 and row == 0 and self.game.board.pils[row][col] == 1:
          opposite = self.game.board.pils[1][col]
          if opposite > 0:
              self.game.board.store2 += opposite + 1
              self.game.board.pils[1][col] = 0
              self.game.board.pils[0][col] = 0
    

    def check_end_game(self):
      board = self.game.board

      # Sumar semillas restantes si un lado está vacío
      side1_empty = all(p == 0 for p in board.pils[1])
      side2_empty = all(p == 0 for p in board.pils[0])

      if side1_empty or side2_empty:
          # Si lado 1 vacío → sumar lado 2 al store2
          if not side2_empty:
              self.game.board.store2 += sum(board.pils[1])
              board.pils[1] = [0] * 6

          # Si lado 2 vacío → sumar lado 1 al store1
          if not side1_empty:
              self.game.board.store1 += sum(board.pils[0])
              board.pils[0] = [0] * 6

          # Finaliza el juego
          self.game.playing = False

          # Determinar ganador 
          if board.store1 > board.store2:
            return self.game.player1.name
          elif board.store2 > board.store1:
              return self.game.player2.name
          else:
              return "Empate"
      return None


              
          
