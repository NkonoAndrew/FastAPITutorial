from typing import Optional
from pydantic import BaseModel, EmailStr, conint 
from datetime import datetime

# schema model for user input validation
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#gets the user id from JWT
class PostCreate(PostBase):
    pass 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

#for the response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
 
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    likes: int

    class Config:
        orm_mode = True
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str



#user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#Pydantic Model that will be used in the token endpoint for the response.
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #not an efficient way to check if the number is 1 or 0 because it allows negatives too

