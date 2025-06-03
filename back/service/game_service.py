import copy
import pprint
from entity.game import Game
from entity.player import Player
from entity.board import Board
import copy

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
            board=board,
            extra_turn = False
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
      
      # Aplicar regla de captura
      if isinstance(last_pos, tuple) and isinstance(last_pos[0], int):
          self.capture_rule(*last_pos, turn)

      # Verificar fin del juego
      if self.check_end_game():
          return self.game.board

      # Verificar turno extra
      if last_pos == ("store", turn):
          self.game.extra_turn = True
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

    def check_end_game(self) -> bool:
      # Sumar semillas restantes para ver si algún lado está vacío
      side1_empty = all(p == 0 for p in self.game.board.pils[0]) # Arriba
      side2_empty = all(p == 0 for p in self.game.board.pils[1]) # Abajo

      if side1_empty or side2_empty:
          # Si arriba vacío → sumar todo lo de abajo al store1
          if side1_empty:
              self.game.board.store1 += sum(self.game.board.pils[1])
              self.game.board.pils[1] = [0] * 6

          # Si abajo vacío → sumar todo lo de arriba al store2
          if side2_empty:
              self.game.board.store2 += sum(self.game.board.pils[0])
              self.game.board.pils[0] = [0] * 6

          # Finaliza el juego
          self.game.playing = False
            
          return True
      return False

    def ia_play_greedy(self, player: int) -> Board:
        board = self.game.board
        if player == 1:
            # Jugador 1
            pass
        else:
            h = self.VorazMancala(board.pils, [board.store1, board.store2], fila=0, jugador=2)
            if h != -1:
                self.make_movement(0, h, 2)  # Jugador 2 juega en fila 0
        return self.game.board


    
    def ia_play_minimax(self, player: int) -> Board:
        board = self.game.board
        if player == 1:
            # Jugador 1
            pass
        else:
            # Jugador 2
            pass
              
          

    def VorazMancala(self, P, S, fila, jugador):
        """
        Parámetros:
        - P: matriz de hoyos (2D list o array)
        - S: almacenes [store1, store2]
        - fila: fila del jugador actual (1 para jugador 1, 0 para jugador 2)
        - jugador: 1 o 2
        """

        posibles_movimientos = self.obtener_hoyos_validos(P, fila)
        mejor_movimiento_actual = -1
        movimientos_con_turno_extra = []
        movimientos_con_captura = []

        if not posibles_movimientos:
            return -1

        for h in posibles_movimientos:
            P_sim, S_sim, es_turno_extra, semillas_capturadas_val = self.simular_movimiento_completo(
                P, S, fila, jugador, h, self.game
            )
            
            if es_turno_extra:
                movimientos_con_turno_extra.append((h, P[fila][h]))
            elif semillas_capturadas_val > 0:
                movimientos_con_captura.append((h, semillas_capturadas_val))

        if movimientos_con_turno_extra:
            mejor_movimiento_actual = self.elegir_mejor_de_lista(movimientos_con_turno_extra, criterio="MAX_PUNTAJE")
            return mejor_movimiento_actual[0]

        if movimientos_con_captura:
            mejor_movimiento_actual = self.elegir_mejor_de_lista(movimientos_con_captura, criterio="MAX_PUNTAJE")
            return mejor_movimiento_actual[0]

        mejor_puntaje_general = -1
        for h in posibles_movimientos:
            if P[fila][h] > mejor_puntaje_general:
                mejor_puntaje_general = P[fila][h]
                mejor_movimiento_actual = h

        return mejor_movimiento_actual




    def obtener_hoyos_validos(self, P, fila):
        return [i for i, semillas in enumerate(P[fila]) if semillas > 0]

    

    def simular_movimiento_completo(self, P, S, fila, jugador, h, juego):
        game_copy = copy.deepcopy(juego)

        game_copy.board.pils = copy.deepcopy(P)
        game_copy.board.store1, game_copy.board.store2 = S[0], S[1]
        game_copy.turn = jugador
        game_copy.playing = True

        board_resultado = game_copy.make_movement(fila, h, jugador)

        P_sim = board_resultado.pils
        S_sim = [board_resultado.store1, board_resultado.store2]

        es_turno_extra = (game_copy.turn == jugador)
        semillas_capturadas_val = S_sim[jugador - 1] - S[jugador - 1]

        return P_sim, S_sim, es_turno_extra, semillas_capturadas_val
    
    def elegir_mejor_de_lista(self, lista, criterio="MAX_PUNTAJE"):

        if not lista:
            return None

        if criterio == "MAX_PUNTAJE":
            return max(lista, key=lambda x: x[1])
        
        raise ValueError(f"Criterio no soportado: {criterio}")


