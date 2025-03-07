from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.openapi.utils import get_openapi
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi.middleware.cors import CORSMiddleware
from pymongo.mongo_client import MongoClient
# Importer le routeur depuis le chemin relatif
from routers.fnctsRoute import router as feature_router
from routers.encryptRoute import router as encrypt_router
from routers.attaqueRoute import router as attaque_router
from routers.hillRoute import router as hill_router
from routers.subRoute import router as sub_router
from routers.CesarRoute import router as cesar_router
from routers.affineRoute import router as affine_router
from models.fncts import PasswordFeature
from models.DicModel import Dictionary
import logging

load_dotenv()
# Configuration du logging
#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)
app = FastAPI(title="Features Service")

# Configurer les CORS
origins = [
    "http://localhost:3000",  # Autoriser le frontend local React
    "http://127.0.0.1:3000",  # Variante de localhost
    # Ajoute d'autres URL si nécessaire (ex: domaine de production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Liste des origines autorisées
    allow_credentials=True,  # Autoriser l'envoi de cookies/authentification
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers (Content-Type, Authorization, etc.)
)

# Exportez le routeur 
router = feature_router

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")  # ici tu met password_testing

@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(MONGO_URI, ssl=True, tlsAllowInvalidCertificates=True)
    await init_beanie(
        database=client[DATABASE_NAME], 
        document_models=[
            PasswordFeature,
            Dictionary  # j'ai créer un model prq pour communiquer avec je suis obligé 
        ]
    )

@app.on_event("shutdown")
async def shutdown_event():
    client = AsyncIOMotorClient(MONGO_URI)
    client.close()
    
# Monter le router des fonctionnalités
app.include_router(feature_router, prefix="/features", tags=["Features"])
app.include_router(encrypt_router, prefix="/encrypt", tags=["encryption"])
app.include_router(attaque_router, prefix="/attaque", tags=["encryption"])
app.include_router(hill_router, prefix="/Hill", tags=["encryption"])
app.include_router(sub_router, prefix="/sub", tags=["encryption"])
app.include_router(cesar_router, prefix="/caesar", tags=["encryption"])
app.include_router(affine_router, prefix="/affine", tags=["encryption"])
@app.get("/")
async def root():
    return {"message": "Bienvenue dans le Features Service!"}

@app.get("/debug-openapi", include_in_schema=False)
def debug_openapi():
    return get_openapi(
        title="Debug API",
        version="1.0.0",
        routes=app.routes,
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=int(SERVER_PORT))


"""""
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.openapi.utils import get_openapi
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pymongo.mongo_client import MongoClient
# Importer le routeur depuis le chemin relatif
from routers.fnctsRoute import router as feature_router
from routers.encryptRoute import router as encrypt_router
from routers.attaqueRoute import router as attaque_router
from models.fncts import PasswordFeature
from models.DicModel import Dictionary
load_dotenv()

app = FastAPI(title="Features Service")

# Exportez le routeur 
router = feature_router

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = os.getenv("SERVER_PORT")
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")#ici tu met password_testing

@app.on_event("startup")
async def startup_event():
    client = AsyncIOMotorClient(MONGO_URI,ssl=True,tlsAllowInvalidCertificates=True)
    await init_beanie(
        database=client[DATABASE_NAME], 
        document_models=[
            
            PasswordFeature,
            Dictionary #j'ai créer un model prq pour communiquer avec je suis obligé 
            
            
              
        ]
    )
@app.on_event("shutdown")
async def shutdown_event():
    client = AsyncIOMotorClient(MONGO_URI)
    client.close()
    
# Monter le router des fonctionnalités
app.include_router(feature_router, prefix="/features", tags=["Features"])
app.include_router(encrypt_router, prefix="/encrypt", tags=["encryption"])
app.include_router(attaque_router, prefix="/attaque", tags=["encryption"])
@app.get("/")
async def root():
    return {"message": "Bienvenue dans le Features Service!"}

@app.get("/debug-openapi", include_in_schema=False)
def debug_openapi():
    return get_openapi(
        title="Debug API",
        version="1.0.0",
        routes=app.routes,
    )
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=int(SERVER_PORT))
"""