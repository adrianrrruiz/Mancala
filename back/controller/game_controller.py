from fastapi import APIRouter
from service.game_service import GameService
from entity.game_start_request import GameStartRequest


router = APIRouter(
  prefix="/game"
)
game_service = GameService()

'''
@router.get("/start")
async def start_game():
    game = game_service.start_game("Adrian", "Leonardo", 1)
    return game.dict() 
'''
@router.post("/start")
async def start_game(request: GameStartRequest):
    game = game_service.start_game(request.player1, request.player2, request.mode)
    return game.dict() # .dict() es por Pydantic

@router.get("/get-game")
async def get_game():
    game = game_service.get_game()
    return game.dict() if game else {"message": "No hay juego activo"} # .dict() es por Pydantic

  
@router.get("/restart")
async def restart_game():
    game_service.restart_game()
    return "Juego reiniciado"

@router.get("/movement")
async def make_movement(row: int, col: int, player: int):
    board = game_service.make_movement(row, col, player)

    if board == "Empate": 
        return {"message": "Empate"}
    else:
        game = game_service.get_game()
        if board == game.player1.name:
            return {"message": "Gano el jugador 1: {}".format(game.player1.name)}
        elif board == game.player2.name:
            return {"message": "Gano el jugador 2: {}".format(game.player2.name)}
    
    return board.dict() if board else {"message": "No se pudo realizar el movimiento"}
