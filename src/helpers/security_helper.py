import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from config import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = HTTPBearer()

class SecurityHelper:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expires_delta = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token has expired"
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token"
            )

    async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
        return SecurityHelper.decode_access_token(token.credentials)

    def require_role(required_role: str):
        def role_checker(current_user=Depends(SecurityHelper.get_current_user)):
            if current_user["role"] != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )
            return current_user
        return role_checker
