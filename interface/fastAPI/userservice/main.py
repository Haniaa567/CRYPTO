import sys
import os
from fastapi import FastAPI
from routers.userRoute import router as user_router
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
load_dotenv()
from models.users import Userhexvault
app = FastAPI(title="User Service")

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(MONGO_URI)
    await init_beanie(
        database=client[DATABASE_NAME], 
        document_models=[
            
           Userhexvault
            
            
              
        ]
    )

router = user_router
app.include_router(user_router, prefix="/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Bienvenue dans le User Service"}

@app.on_event("shutdown")
async def shutdown_event():
    client = AsyncIOMotorClient(MONGO_URI)
    client.close()
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
