# routers.py
from fastapi import APIRouter, Depends
from typing import List

from models.VigenereModel import (
    VigenereRequest, VigenereResponse,
    CryptanalysisKeyLengthRequest, CryptanalysisKeyLengthResponse,
    CryptanalysisWordRequest, CryptanalysisWordResponse
)
from controleur.VigenereControlleur import VigenereController, CryptanalysisController



router = APIRouter()

# Vigenere cipher routes
@router.post("/encrypt", response_model=VigenereResponse)
async def encrypt(
    request: VigenereRequest,
    controller: VigenereController = Depends()
):
    """Encrypt text using Vigenere cipher"""
    return await controller.encrypt(request)


@router.post("/decrypt", response_model=VigenereResponse)
async def decrypt(
    request: VigenereRequest,
    controller: VigenereController = Depends()
):
    """Decrypt text using Vigenere cipher"""
    return await controller.decrypt(request)


# Cryptanalysis routes
@router.post("/key-length", response_model=CryptanalysisKeyLengthResponse)
async def analyze_by_key_length(
    request: CryptanalysisKeyLengthRequest,
    controller: CryptanalysisController = Depends()
):
    """Analyze ciphertext using known key length"""
    return await controller.analyze_by_key_length(request)


@router.post("/suspected-word", response_model=CryptanalysisWordResponse)
async def analyze_by_suspected_word(
    request: CryptanalysisWordRequest,
    controller: CryptanalysisController = Depends()
):
    """Analyze ciphertext using a suspected word"""
    return await controller.analyze_by_suspected_word(request)