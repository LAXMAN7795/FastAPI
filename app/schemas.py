from pydantic import BaseModel,EmailStr,Field,ConfigDict
from datetime import datetime
from typing import Optional

# create the schema
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# to use this import shemas anywhere you want to access post use shemas.Post
class UserResponse(BaseModel):
    id:int
    email: EmailStr
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)
# create the base schema( Sending data to us)
class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True
    owner : UserResponse

#inherit base class
class CreatePost(BasePost):
    pass 

# Pydantic model for response( us sending data to the user)
class PostResponse(BasePost):
    id: int
    created_at : datetime
    owner_id:int
    owner: UserResponse

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post : PostResponse
    votes :int 

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email:EmailStr
    password:str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None

class Vote(BaseModel):
    post_id:int 
    post_dir : int

