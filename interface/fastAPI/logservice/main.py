from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Importer le routeur depuis le chemin relatif
from .routers.historiqueRoute import router as log_router

load_dotenv()

app = FastAPI(title="Log Service")

# Exportez le routeur
router = log_router

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")

# Monter le router des logs
app.include_router(log_router, prefix="/logs", tags=["Logs"])

@app.get("/")
async def root():
    return {"message": "Bienvenue dans le Log Service!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=int(SERVER_PORT))