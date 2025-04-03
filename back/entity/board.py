from pydantic import BaseModel

class Board(BaseModel):
    store1 : int
    store2 : int
    pils : list[list[int]]
      
    
  
