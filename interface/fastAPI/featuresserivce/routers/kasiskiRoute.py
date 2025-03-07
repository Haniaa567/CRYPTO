from fastapi import APIRouter
from controleur.kasikiControlleur import kasiski_controller
from models.kaseskiModel import KasiskiRequest

router = APIRouter()

@router.post("/kasiski-test", tags=["Kasiski"])
async def kasiski_route(request: KasiskiRequest):
    return kasiski_controller(request.ciphertext)
