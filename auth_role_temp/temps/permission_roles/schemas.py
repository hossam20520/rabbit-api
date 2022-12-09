
from typing import List, Union , Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from pydantic import BaseModel , EmailStr ,  Field




class Permission_roleCreate(BaseModel):
    permission_id:int
    role_id:int
    

    class Config:
        orm_mode = True


class Permission_role(Permission_roleCreate):
    id: int 

    class Config:
        orm_mode = True