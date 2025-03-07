from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import requests
from config import config  # Assurez-vous que config contient les variables Keycloak

security = HTTPBearer()

def get_keycloak_public_key():
    url = f"{config.KEYCLOAK_SERVER_URL}/realms/{config.KEYCLOAK_REALM}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        public_key = response.json()['public_key']
        return f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
    except Exception as e:
        print(f"Error fetching public key: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch public key")

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    try:
        token = credentials.credentials
        public_key = get_keycloak_public_key()
        
        # Décoder et vérifier le token
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="account",
            issuer=f"{config.KEYCLOAK_SERVER_URL}/realms/{config.KEYCLOAK_REALM}"
        )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error validating token: {str(e)}"
        )
