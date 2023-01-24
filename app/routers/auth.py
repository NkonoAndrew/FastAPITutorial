from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm  import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database, schemas, models, utils, oauth2


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_info: OAuth2PasswordRequestForm = Depends(), db:  Session = Depends(database.get_db)):

    #user info is returned as a dict: username, password
    user = db.query(models.User).filter(models.User.email == user_info.username).first()
    print(user)

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Wrong credentials!")
    
    #takes in row password and compares it from the one in the database 
    if not utils.verify_password(user_info.password, user.password):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Wrong credentials!")

    #create a token, user id is the only user data we put in the payload 
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    #return token
    return {"access_token" : access_token, "token_type" : "bearer"}


   