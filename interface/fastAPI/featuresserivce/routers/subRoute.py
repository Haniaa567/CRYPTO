from fastapi import APIRouter, Depends
from controleur.SubControlleur import generate_key,encrypt_message,decrypt_message,MessageRequest
from pydantic import BaseModel

router = APIRouter()
class KEYGENERATE(BaseModel):
    mode: str
    password: str

@router.post("/encrypt", response_model=dict)
async def encrypt_message_route(request: MessageRequest):

    return await encrypt_message(request)

@router.post("/decrypt", response_model=dict)
async def decrypt_message_route(request: MessageRequest):

    return await decrypt_message(request)

@router.get("/key", response_model=dict)
async def generate_key_route():
    return await generate_key()  
