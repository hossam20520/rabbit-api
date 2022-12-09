
from typing import List, Union , Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from pydantic import BaseModel , EmailStr ,  Field




class PermissionCreate(BaseModel):
    title: str
    label: str

    class Config:
        orm_mode = True


class Permission(PermissionCreate):
    id: int 

    class Config:
        orm_mode = True