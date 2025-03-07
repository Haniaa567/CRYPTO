from fastapi import APIRouter, HTTPException
from typing import List
from models.fncts import PasswordFeature



async def delete_feature(feature_id: str):

    feature = await PasswordFeature.get(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Fonctionnalité non trouvée")

    await feature.delete()
    return {"message": "Fonctionnalité supprimée avec succès"}


async def update_feature(feature_id: str, updated_data: PasswordFeature):
    feature = await PasswordFeature.get(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Fonctionnalité non trouvée")
    
    # Préparer les données de mise à jour
    update_data = updated_data.dict(exclude_unset=True)  # Exclure les champs non fournis
    await feature.update({"$set": update_data})
    return feature


async def get_feature(feature_id: str):
  
    feature = await PasswordFeature.get(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Fonctionnalité non trouvée")
    return feature

async def list_features():

    features = await PasswordFeature.find_all().to_list()
    return features

async def create_feature(feature: PasswordFeature):

    try:
        await feature.insert()
        return feature
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
async def get_features_by_user_id(id_utilisateur: str):
    try:
        # Filtrer les fonctionnalités par `id_utilisateur`
        
        features = await PasswordFeature.find({"id_utilisateur": id_utilisateur}).to_list()
        
        
        if not features:
            raise HTTPException(
                status_code=404,
                detail=f"Aucune fonctionnalité trouvée pour l'utilisateur avec ID {id_utilisateur}"
            )
        return features
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur lors de la recherche des fonctionnalités : {str(e)}"
        )
