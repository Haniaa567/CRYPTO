from fastapi import APIRouter
from models.AffineModel import AffineRequest,FrequencyAnalysisRequest,BruteForceRequest
from controleur.affineControlleur import encrypt_controller,decrypt_controller,frequency_analysis_controller,brute_force_controller

router = APIRouter()

    
@router.post("/encrypt")
async def encrypt(request: AffineRequest):
    return encrypt_controller(request.text, request.A, request.B)

@router.post("/decrypt")
async def decrypt(request: AffineRequest):
    return decrypt_controller(request.text, request.A, request.B)

@router.post("/brute_force")
async def brute_force(request: BruteForceRequest):
    return brute_force_controller(request.cipher)

@router.post("/frequency_analysis")
async def frequency_analysis(request: FrequencyAnalysisRequest):
    return frequency_analysis_controller(request.cipher, request.language)
