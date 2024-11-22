from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

# Schema for Create_Posts
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool=True

# Schema for Create_Posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

# Schema for Response
class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: PostResponse
    Votes: int

    # class Config:
    #     orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None    

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore