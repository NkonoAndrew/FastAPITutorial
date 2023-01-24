from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import database, schemas, models
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . config import settings

#login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    #jwt times tells us when it will expire 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials!", headers={"WWW-Authenticate": "Bearer"})

    #gets the current user
    token =  verify_access_token(token, credentials_exception)

    #query db for current user
    user = db.query(models.User).filter(token.id == models.User.id).first()
    return user
 

