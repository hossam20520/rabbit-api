
from sqlalchemy.orm import Session
from roles.models import RoleModel
from roles.schemas import RoleCreate , Role
from fastapi import Depends, HTTPException
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.exc import IntegrityError
from global_schemas import ResponseModel



def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RoleModel).offset(skip).limit(limit).all()


def create_role(db: Session, role:Role):
    try:
        db_role  = RoleModel(**role.dict())
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
    except IntegrityError:
         db.rollback()
         raise HTTPException(422, ResponseModel([] , "Role already exist" , False , 422 , {"error":"Already exists"})) from None
    return db_role


def delete_all_role(db: Session):
    db.query(RoleModel).delete()
    db.commit()
    return []


def get_role(db: Session, role_id: int):
    return db.query(RoleModel).filter(RoleModel.id == role_id).first()


def get_role_by_email(db: Session, email: str):
    return db.query(RoleModel).filter(RoleModel.email == email).first()

def update_role(db: Session , role: dict , id: int):
   db.query(RoleModel).filter(RoleModel.id == id).update(dict(role), synchronize_session = False)
   db.commit()
   return role


def delete_role(db: Session , id:int):
    db_model = db.query(RoleModel).get(id)
    if db_model:
         db.delete(db_model)
         db.commit() 
         return db_model
            
    else:
          raise HTTPException(status_code=404, detail=ResponseModel([] , "Role not found" , True , 404 , {}))
