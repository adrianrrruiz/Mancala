from entity.game import Game
from entity.player import Player
from entity.board import Board
import math
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
            board=board
        )
        return self.game.board
    
    def get_game(self):
      return self.game
    
    def restart_game(self):
      self.game = None
    
    def make_movement(self, row, col, turn, game=None) -> Board:
        if game is None:
            game = self.game
        if not game or not game.playing:
            return None

        board = game.board
        rocks = board.pils[row][col]
        if rocks == 0:
            return board

        board.pils[row][col] = 0
        current_row, current_col = row, col
        last_pos = None

        while rocks > 0:
            if current_row == 1:  # jugador 1
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
                    continue
                previous = board.pils[1][current_col]
                board.pils[1][current_col] += 1
                rocks -= 1
                if rocks == 0:
                    last_pos = (1, current_col, previous)

            else:  # jugador 2
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
                    continue
                previous = board.pils[0][current_col]
                board.pils[0][current_col] += 1
                rocks -= 1
                if rocks == 0:
                    last_pos = (0, current_col, previous)

        # Aplicar captura solo si última semilla cayó en pozo
        if isinstance(last_pos, tuple) and len(last_pos) == 3:
            self.capture_rule(last_pos[0], last_pos[1], turn, last_pos[2])

        # Verificar fin de juego
        if self.check_end_game():
            return game.board

        # Turno extra
        if last_pos == ("store", turn):
            pass
        else:
            game.turn = 2 if turn == 1 else 1

        board.turn = game.turn
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

    def capture_rule(self, row, col, turn, previous_count, game=None):
        if game is None:
            game = self.game

        # Verifica que cayó en su propio lado y la casilla estaba vacía
        if turn == 1 and row == 1 and game.board.pils[row][col] == 1 and previous_count == 0:
            opposite = game.board.pils[0][col]
            if opposite > 0:
                game.board.store1 += opposite + 1
                game.board.pils[0][col] = 0
                game.board.pils[1][col] = 0

        elif turn == 2 and row == 0 and game.board.pils[row][col] == 1 and previous_count == 0:
            opposite = game.board.pils[1][col]
            if opposite > 0:
                game.board.store2 += opposite + 1
                game.board.pils[1][col] = 0
                game.board.pils[0][col] = 0


    def check_end_game(self, game = None) -> bool:
      if game is None:
          game = self.game
      # Sumar semillas restantes para ver si algún lado está vacío
      side1_empty = all(p == 0 for p in game.board.pils[0]) # Arriba
      side2_empty = all(p == 0 for p in game.board.pils[1]) # Abajo

      if side1_empty or side2_empty:
          # Si arriba vacío → sumar todo lo de abajo al store1
          if side1_empty:
              game.board.store1 += sum(game.board.pils[1])
              game.board.pils[1] = [0] * 6

          # Si abajo vacío → sumar todo lo de arriba al store2
          if side2_empty:
              game.board.store2 += sum(game.board.pils[0])
              game.board.pils[0] = [0] * 6

          # Finaliza el juego
          game.playing = False
            
          return True
      return False

    def ia_play_greedy(self, player: int) -> Board:
        board = self.game.board
        if player == 1:
            h = self.VorazMancala(board.pils, [board.store1, board.store2], fila=1, jugador=1)
            if h != -1:
                self.make_movement(1, h, 1)  # Jugador 1 juega en fila 1
        else:
            h = self.VorazMancala(board.pils, [board.store1, board.store2], fila=0, jugador=2)
            if h != -1:
                self.make_movement(0, h, 2)  # Jugador 2 juega en fila 0
        return self.game.board
    



    
    def ia_play_minimax(self, player: int) -> Board:
        board = self.game.board
        P = board.pils
        S = [board.store1, board.store2]
        profundidad = 5  

        if player == 1:
            fila = 1
            j_actual = 1
        else:
            fila = 0
            j_actual = 2

        # Llamada a Minimax
        mejor_hoyo = self.decision_minimax(P, S, j_actual, profundidad, self.game)

        if mejor_hoyo != -1:
            self.make_movement(fila, mejor_hoyo, j_actual)

        return self.game.board

              
    # ----------------------------------- Funciones del algoritmo Greedy -------------------------------------------------------------------------------
      

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


    def elegir_mejor_de_lista(self, lista, criterio="MAX_PUNTAJE"):

        if not lista:
            return None

        if criterio == "MAX_PUNTAJE":
            return max(lista, key=lambda x: x[1])
        
        raise ValueError(f"Criterio no soportado: {criterio}")    

    def obtener_hoyos_validos(self, P, fila):
        return [i for i, semillas in enumerate(P[fila]) if semillas > 0]

    

    def simular_movimiento_completo(self, P, S, fila, jugador, h, juego):
        game_copy = copy.deepcopy(juego)

        game_copy.board.pils = copy.deepcopy(P)
        game_copy.board.store1, game_copy.board.store2 = S[0], S[1]
        game_copy.turn = jugador
        game_copy.playing = True

        board_resultado = self.make_movement(fila, h, jugador, game_copy)

        P_sim = board_resultado.pils
        S_sim = [board_resultado.store1, board_resultado.store2]

        es_turno_extra = (game_copy.turn == jugador)
        semillas_capturadas_val = S_sim[jugador - 1] - S[jugador - 1]

        return P_sim, S_sim, es_turno_extra, semillas_capturadas_val
    

    
# ----------------------------------- Funciones del algoritmo  Minimax -------------------------------------------------------------------------------


    def esta_vacia(self, lista):
        return len(lista) == 0

    def oponente(self, jugador):
        return 2 if jugador == 1 else 1

    def es_fin_de_juego(self, P, jugador):
        fila = 1 if jugador == 1 else 0
        return all(p == 0 for p in P[fila])

    def funcion_evaluacion_estado(self, P, S, jugador_eval):
        return S[jugador_eval - 1] - S[self.oponente(jugador_eval) - 1]

    def decision_minimax(self, P, S, j_actual, profundidad_max, juego):
        fila = 1 if j_actual == 1 else 0
        posibles_movimientos = self.obtener_hoyos_validos(P, fila)
        
        if self.esta_vacia(posibles_movimientos):
            return -1

        mejor_hoyo_encontrado = -1
        max_valor_evaluado = -math.inf
        alfa = -math.inf
        beta = math.inf

        for h in posibles_movimientos:
            P_siguiente, S_siguiente, es_turno_extra, _ = self.simular_movimiento_completo(P, S, fila, j_actual, h, juego)

            if es_turno_extra:
                valor_movimiento_actual = self.valor_max(P_siguiente, S_siguiente, j_actual, profundidad_max - 1, alfa, beta, j_actual, juego)
            else:
                j_oponente = self.oponente(j_actual)
                valor_movimiento_actual = self.valor_min(P_siguiente, S_siguiente, j_oponente, profundidad_max - 1, alfa, beta, j_actual, juego)

            if valor_movimiento_actual > max_valor_evaluado:
                max_valor_evaluado = valor_movimiento_actual
                mejor_hoyo_encontrado = h

            alfa = max(alfa, max_valor_evaluado)

        return mejor_hoyo_encontrado


    def valor_max(self, P_estado, S_estado, j_turno_max, profundidad, alfa, beta, j_perspectiva_eval, juego):
        if profundidad == 0 or self.es_fin_de_juego(P_estado, j_turno_max):
            return self.funcion_evaluacion_estado(P_estado, S_estado, j_perspectiva_eval)

        fila = 1 if j_turno_max == 1 else 0
        posibles_movimientos = self.obtener_hoyos_validos(P_estado, fila)

        if self.esta_vacia(posibles_movimientos):
            return self.funcion_evaluacion_estado(P_estado, S_estado, j_perspectiva_eval)

        valor_max = -math.inf

        for h in posibles_movimientos:
            P_siguiente, S_siguiente, es_turno_extra, _ = self.simular_movimiento_completo(P_estado, S_estado, fila, j_turno_max, h, juego)

            if es_turno_extra:
                eval_actual = self.valor_max(P_siguiente, S_siguiente, j_turno_max, profundidad - 1, alfa, beta, j_perspectiva_eval, juego)
            else:
                j_oponente = self.oponente(j_turno_max)
                eval_actual = self.valor_min(P_siguiente, S_siguiente, j_oponente, profundidad - 1, alfa, beta, j_perspectiva_eval, juego)

            valor_max = max(valor_max, eval_actual)
            alfa = max(alfa, valor_max)

            if beta <= alfa:
                break  # Poda Beta

        return valor_max


    def valor_min(self, P_estado, S_estado, j_turno_min, profundidad, alfa, beta, j_perspectiva_eval, juego):
        if profundidad == 0 or self.es_fin_de_juego(P_estado, j_turno_min):
            return self.funcion_evaluacion_estado(P_estado, S_estado, j_perspectiva_eval)

        fila = 1 if j_turno_min == 1 else 0
        posibles_movimientos = self.obtener_hoyos_validos(P_estado, fila)

        if self.esta_vacia(posibles_movimientos):
            return self.funcion_evaluacion_estado(P_estado, S_estado, j_perspectiva_eval)

        valor_min = math.inf

        for h in posibles_movimientos:
            P_siguiente, S_siguiente, es_turno_extra, _ = self.simular_movimiento_completo(P_estado, S_estado, fila, j_turno_min, h, juego)

            if es_turno_extra:
                eval_actual = self.valor_min(P_siguiente, S_siguiente, j_turno_min, profundidad - 1, alfa, beta, j_perspectiva_eval, juego)
            else:
                j_oponente = self.oponente(j_turno_min)
                eval_actual = self.valor_max(P_siguiente, S_siguiente, j_oponente, profundidad - 1, alfa, beta, j_perspectiva_eval, juego)

            valor_min = min(valor_min, eval_actual)
            beta = min(beta, valor_min)

            if beta <= alfa:
                break  # Poda Alfa

        return valor_min
