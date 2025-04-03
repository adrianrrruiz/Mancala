# Install: pip install "fastapi[standard]" 
# Run: fastapi dev main.py

from fastapi import FastAPI

from controller.game_controller import router

app = FastAPI()
app.include_router(router)

