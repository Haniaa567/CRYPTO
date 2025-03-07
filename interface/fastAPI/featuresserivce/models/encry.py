from pydantic import BaseModel

class DecryptRequest(BaseModel):
    """Modèle pour les requêtes de déchiffrement."""
    encrypted_message: str
    key: str
    enregistrement:bool
    iduser:str


class EncryptRequest(BaseModel):
    """Modèle pour les requêtes de chiffrement."""
    
    message: str
    key: str
    enregistrement:bool
    iduser:str

