
from sqlalchemy.orm import Session
from permissions.models import PermissionModel
from permissions.schemas import PermissionCreate , Permission
from fastapi import Depends, HTTPException
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.exc import IntegrityError
from global_schemas import ResponseModel



def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PermissionModel).offset(skip).limit(limit).all()


def create_permission(db: Session, permission:Permission):
    try:
        db_permission  = PermissionModel(**permission.dict())
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
    except IntegrityError:
         db.rollback()
         raise HTTPException(422, ResponseModel([] , "Permission already exist" , False , 422 , {"error":"Already exists"})) from None
    return db_permission


def delete_all_permission(db: Session):
    db.query(PermissionModel).delete()
    db.commit()
    return []


def get_permission(db: Session, permission_id: int):
    return db.query(PermissionModel).filter(PermissionModel.id == permission_id).first()


def get_permission_by_email(db: Session, email: str):
    return db.query(PermissionModel).filter(PermissionModel.email == email).first()

def update_permission(db: Session , permission: dict , id: int):
   db.query(PermissionModel).filter(PermissionModel.id == id).update(dict(permission), synchronize_session = False)
   db.commit()
   return permission


def delete_permission(db: Session , id:int):
    db_model = db.query(PermissionModel).get(id)
    if db_model:
         db.delete(db_model)
         db.commit() 
         return db_model
            
    else:
          raise HTTPException(status_code=404, detail=ResponseModel([] , "Permission not found" , True , 404 , {}))
