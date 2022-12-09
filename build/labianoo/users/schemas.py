
from typing import List, Union , Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from pydantic import BaseModel , EmailStr ,  Field




class UserCreate(BaseModel):
    title:str

    class Config:
        orm_mode = True


class User(UserCreate):
    id: int 

    class Config:
        orm_mode = True