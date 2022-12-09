from typing import List, Union , Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from pydantic import BaseModel , EmailStr ,  Field




class UserCreate(BaseModel):
    first_name:str 
    last_name:str 
    username:str 
    email:str
    hashed_password:str 
    is_active:bool

    class Config:
        orm_mode = True


class User(UserCreate):
    id: int 

    class Config:
        orm_mode = True