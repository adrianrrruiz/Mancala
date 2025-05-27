from fastapi import FastAPI

from controller.game_controller import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://mancala-one.vercel.app"
    ],  
    allow_credentials=True,
    allow_methods=["*"],                      
    allow_headers=["*"],
)

app.include_router(router)

