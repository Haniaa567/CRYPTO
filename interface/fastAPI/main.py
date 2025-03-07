from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pymongo.mongo_client import MongoClient
from userservice.models.users import Userhexvault 
from featuresserivce.models.fncts import PasswordFeature 
from logservice.models.historique import History
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os,sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
from  userservice.main import router as user_router
from  featuresserivce.main import router as features_router
from logservice.main import router as log_router


app = FastAPI(title="hexvault")
#test to push ........test123
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP
    allow_headers=["*"],  # Autoriser tous les en-têtes
)

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
SERVER_HOST=os.getenv("SERVER_HOST")
SERVER_PORT=os.getenv("SERVER_PORT")

@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(
        database=client[DATABASE_NAME], 
        document_models=[
            Userhexvault,
            PasswordFeature,
            History
            
              
        ]
    )
@app.get("/")
async def root():
    return {"message": "Bienvenue dans hexvault"}

@app.on_event("shutdown")
async def shutdown_event():
    client = AsyncIOMotorClient(MONGO_URI)
    client.close()

app.include_router(user_router, prefix="/user", tags=["Utilisateur"])
app.include_router(features_router, prefix="/fonctions", tags=["fonctions"])
app.include_router(log_router, prefix="/history", tags=["history"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)