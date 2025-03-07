from fastapi import HTTPException, Request,Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import requests
from jose import jwt
from jose.exceptions import JWTError
from config import config

# Fonction de vérification du token
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
class JWTBearer(HTTPBearer):
    security = HTTPBearer()

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Authorization header missing.")

    def verify_jwt(self, token: str) -> bool:
        # Valider le token avec Keycloak
        url = "http://localhost:8080/realms/HEXVAULT/protocol/openid-connect/userinfo"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        return response.status_code == 200
    
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
