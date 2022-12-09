
from typing import List, Union , Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from pydantic import BaseModel , EmailStr ,  Field




class RoleCreate(BaseModel):
    name: str
    label: str


    class Config:
        orm_mode = True


class Role(RoleCreate):
    id: int 

    class Config:
        orm_mode = True