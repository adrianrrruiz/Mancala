from pydantic import BaseModel
class GameStartRequest(BaseModel):
    player1: str
    player2: str
    mode: int
      
    
  
