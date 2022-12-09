
from sqlalchemy.orm import Session
from permission_roles.models import Permission_roleModel
from permission_roles.schemas import Permission_roleCreate , Permission_role
from fastapi import Depends, HTTPException
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.exc import IntegrityError
from global_schemas import ResponseModel



def get_permission_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Permission_roleModel).offset(skip).limit(limit).all()


def create_permission_role(db: Session, permission_role:Permission_role):
    try:
        db_permission_role  = Permission_roleModel(**permission_role.dict())
        db.add(db_permission_role)
        db.commit()
        db.refresh(db_permission_role)
    except IntegrityError:
         db.rollback()
         raise HTTPException(422, ResponseModel([] , "Permission_role already exist" , False , 422 , {"error":"Already exists"})) from None
    return db_permission_role


def delete_all_permission_role(db: Session):
    db.query(Permission_roleModel).delete()
    db.commit()
    return []


def get_permission_role(db: Session, permission_role_id: int):
    return db.query(Permission_roleModel).filter(Permission_roleModel.id == permission_role_id).first()


def get_permission_role_by_email(db: Session, email: str):
    return db.query(Permission_roleModel).filter(Permission_roleModel.email == email).first()

def update_permission_role(db: Session , permission_role: dict , id: int):
   db.query(Permission_roleModel).filter(Permission_roleModel.id == id).update(dict(permission_role), synchronize_session = False)
   db.commit()
   return permission_role


def delete_permission_role(db: Session , id:int):
    db_model = db.query(Permission_roleModel).get(id)
    if db_model:
         db.delete(db_model)
         db.commit() 
         return db_model
            
    else:
          raise HTTPException(status_code=404, detail=ResponseModel([] , "Permission_role not found" , True , 404 , {}))
