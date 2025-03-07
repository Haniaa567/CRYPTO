from fastapi import APIRouter
from typing import List
from models.fncts import PasswordFeature
from services.servicesFcts import create_feature,list_features,get_feature,update_feature,delete_feature,get_features_by_user_id 

router = APIRouter()

@router.post("/create", response_model=PasswordFeature)
async def create_feature_db(feature: PasswordFeature):
    return await create_feature(feature)

@router.get("/list", response_model=List[PasswordFeature])
async def list_features_db():
    return await list_features()

@router.get("/{feature_id}", response_model=PasswordFeature)
async def get_feature_db(feature_id: str):
    return await get_feature(feature_id)
@router.get("/gethistorique/{id_utilisateur}",response_model=List[PasswordFeature])
async def getfeaturiduser(id_utilisateur: str):
    return await get_features_by_user_id(id_utilisateur)

@router.put("/modifie/{feature_id}", response_model=PasswordFeature)
async def update_feature_db(feature_id: str, updated_data: PasswordFeature):
    return await update_feature(feature_id, updated_data)

@router.delete("/delete/{feature_id}")
async def delete_feature_db(feature_id: str):
    return await delete_feature(feature_id)




