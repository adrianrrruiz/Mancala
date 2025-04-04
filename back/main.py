# Install: pip install "fastapi[standard]" 
# Run: fastapi dev main.py

from fastapi import FastAPI

from controller.game_controller import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configura CORS aquí:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # 👈 Cambia esto si usas otro frontend
    allow_credentials=True,
    allow_methods=["*"],                      # 👈 Acepta todos los métodos (incluye OPTIONS)
    allow_headers=["*"],
)

app.include_router(router)

