from fastapi import APIRouter
from service.game_service import GameService

router = APIRouter(
  prefix="/game"
)
game_service = GameService()

@router.get("/start")
async def start_game():
    game = game_service.start_game("Adrian", "Leonardo", 1)
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
async def make_movement():
    board = game_service.make_movement(1, 3, 1) # Prueba: Fila 2, Columna 4 y Jugador 1
    return board.dict() if board else {"No se pudo realizar el movimiento"} 