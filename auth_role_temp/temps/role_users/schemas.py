
from typing import List, Union , Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from pydantic import BaseModel , EmailStr ,  Field




class Role_userCreate(BaseModel):
    user_id:int
    role_id:int 

    class Config:
        orm_mode = True


class Role_user(Role_userCreate):
    id: int 

    class Config:
        orm_mode = True