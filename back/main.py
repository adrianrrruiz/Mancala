from fastapi import FastAPI

from controller.game_controller import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configura CORS aquí:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],                      
    allow_headers=["*"],
)

app.include_router(router)

