TEMPLATE = """
from typing import List, Union , Optional
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from pydantic import BaseModel , EmailStr ,  Field




class {{element.Name}}Create(BaseModel):
    title:str

    class Config:
        orm_mode = True


class {{element.Name}}({{element.Name}}Create):
    id: int 

    class Config:
        orm_mode = True"""