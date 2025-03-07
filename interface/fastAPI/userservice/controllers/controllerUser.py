from fastapi.security import OAuth2PasswordRequestForm
from ..models.users import Userhexvault, UserCreate,UserLogin
from fastapi import APIRouter, HTTPException, Depends



async def create_user(user: UserCreate):

    try:
      
        existing_user_email = await Userhexvault.find_one(Userhexvault.email == user.email)
        existing_user_username = await Userhexvault.find_one(Userhexvault.username == user.username)
        
        if existing_user_email:
            raise HTTPException(status_code=400, detail="Un utilisateur avec cet email existe déjà")
        
        if existing_user_username:
            raise HTTPException(status_code=400, detail="Ce nom d'utilisateur est déjà pris")
        
      
        new_user = await Userhexvault.create_user(
            nom=user.nom,
            prenom=user.prenom,
            username=user.username,
            email=user.email,
            password=user.password
        )
        
        return {"message": "Utilisateur créé avec succès", "user_id": str(new_user.id)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def login_user(data: UserLogin):
    user = await Userhexvault.find_one(Userhexvault.username == data.username)
    
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
 
    if not user.verify_password(data.password):
        raise HTTPException(status_code=400, detail="Mot de passe incorrect")
    
    return {"access_token": "token_factice", "token_type": "bearer"}