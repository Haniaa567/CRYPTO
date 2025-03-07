from fastapi import APIRouter
from models.cesarModel import (
    CaesarEncryptRequest, 
    CaesarDecryptRequest, 
    BruteForceRequest, 
    FrequencyAnalysisRequest,
    FrequencyAnalysisResponse
)
from controleur.cesarControlleur import (
    encrypt_text, 
    decrypt_text, 
    brute_force_crack, 
    analyze_frequency
)

router = APIRouter()

@router.post("/encrypt", response_model=dict)
async def encrypt_route(request: CaesarEncryptRequest):
    """
    Endpoint to encrypt text using Caesar cipher
    """
    return await encrypt_text(request)

@router.post("/decrypt", response_model=dict)
async def decrypt_route(request: CaesarDecryptRequest):
    """
    Endpoint to decrypt text using Caesar cipher
    """
    return await decrypt_text(request)

@router.post("/brute-force", response_model=dict)
async def brute_force_route(request: BruteForceRequest):
    """
    Endpoint to crack text using brute force approach
    """
    return await brute_force_crack(request)

@router.post("/frequency-analysis", response_model=FrequencyAnalysisResponse)
async def frequency_analysis_route(request: FrequencyAnalysisRequest):
    """
    Endpoint to analyze text using frequency analysis
    """
    return await analyze_frequency(request)