from pydantic import BaseModel, Field
from typing import List, Optional

class CaesarEncryptRequest(BaseModel):
    text: str = Field(..., description="Text to encrypt")
    shift: int = Field(..., description="Shift value for encryption")

class CaesarDecryptRequest(BaseModel):
    text: str = Field(..., description="Text to decrypt")
    shift: int = Field(..., description="Shift value for decryption")

class BruteForceRequest(BaseModel):
    text: str = Field(..., description="Encrypted text to crack using brute force")

class FrequencyAnalysisRequest(BaseModel):
    text: str = Field(..., description="Encrypted text to analyze")
    language: str = Field("english", description="Language for frequency analysis (english or french)")

class DecryptionResult(BaseModel):
    shift: int
    text: str

class FrequencyAnalysisResponse(BaseModel):
    possible_shifts: List[int]
    decryptions: List[DecryptionResult]