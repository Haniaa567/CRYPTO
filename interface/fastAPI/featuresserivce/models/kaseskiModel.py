from pydantic import BaseModel

class KasiskiRequest(BaseModel):
    ciphertext: str

class KasiskiResponse(BaseModel):
    repeated_sequences: dict
    distances: list[int]
    common_factors: list[int]
