from typing import Optional
from beanie import Document
from pydantic import BaseModel, EmailStr, Field, validator
from passlib.context import CryptContext

# Configuration pour le hachage de mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Userhexvault(Document):
    nom: str = Field(...)
    prenom: str = Field(...)
    username: str = Field(..., unique=True)
    email: EmailStr = Field(..., unique=True)
    password: str = Field(...)

    class Settings:
        name = "users"
        unique_fields = ["username", "email"]

    class Config:
        json_schema_extra = {
            "example": {
                "nom": "Dupont",
                "prenom": "Jean",
                "username": "jeandupont",
                "email": "jean.dupont@example.com",
                "password": "motdepasse123"
            }
        }

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Haché le mot de passe avant enregistrement
        """
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        """
        Vérifie le mot de passe fourni
        """
        return pwd_context.verify(plain_password, self.password)

    @classmethod
    async def create_user(cls, nom: str, prenom: str, username: str, email: str, password: str):
        """
        Méthode de création d'utilisateur sécurisée
        """
        # Haché le mot de passe avant l'enregistrement
        hashed_password = cls.hash_password(password)
        
        user = cls(
            nom=nom,
            prenom=prenom,
            username=username,
            email=email,
            password=hashed_password
        )
        await user.save()
        return user

class UserCreate(BaseModel):
    """
    Schéma de validation pour la création d'utilisateur
    """
    nom: str
    prenom: str
    username: str
    email: EmailStr
    password: str

    @validator('username')
    def username_alphanumeric(cls, v):
        """
        Validation du username (uniquement alphanumériques)
        """
        assert v.isalnum(), 'Le username doit être alphanumériques'
        return v
class UserLogin(BaseModel):
    username: str
    password: str
