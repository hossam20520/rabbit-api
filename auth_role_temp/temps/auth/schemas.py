from typing import List, Union , Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from pydantic import BaseModel , EmailStr ,  Field








class RegisterSchema(BaseModel):
    first_name:str  = Field(...)
    last_name:str = Field(...)
    username:str = Field(...)
    email:str = Field(...)
    hashed_password:str = Field(...)
    is_active:bool = Field(...)
    
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Hossam",
                "last_name": "Hassan",
                "username": "hossam20520",
                "email": "hossamhassan889@gmail.com",
                "hashed_password": "hossam",
                "is_active": True
            }
        }