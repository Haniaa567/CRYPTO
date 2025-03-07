from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from ..models.users import Userhexvault, UserCreate, UserLogin
from ..controllers.controllerUser import create_user,login_user

router = APIRouter()


@router.post("/register/")
async def register_user(user: UserCreate):
    return await create_user(user)


#Rajouter l'autentification
@router.post("/login")
async def login_user_db(form_data: UserLogin):
    return await login_user(form_data)

