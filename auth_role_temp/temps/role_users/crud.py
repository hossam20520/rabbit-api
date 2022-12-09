
from sqlalchemy.orm import Session
from role_users.models import Role_userModel
from role_users.schemas import Role_userCreate , Role_user
from fastapi import Depends, HTTPException
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.exc import IntegrityError
from global_schemas import ResponseModel



def get_role_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Role_userModel).offset(skip).limit(limit).all()


def create_role_user(db: Session, role_user:Role_user):
    try:
        db_role_user  = Role_userModel(**role_user.dict())
        db.add(db_role_user)
        db.commit()
        db.refresh(db_role_user)
    except IntegrityError:
         db.rollback()
         raise HTTPException(422, ResponseModel([] , "Role_user already exist" , False , 422 , {"error":"Already exists"})) from None
    return db_role_user


def delete_all_role_user(db: Session):
    db.query(Role_userModel).delete()
    db.commit()
    return []


def get_role_user(db: Session, role_user_id: int):
    return db.query(Role_userModel).filter(Role_userModel.id == role_user_id).first()


def get_role_user_by_email(db: Session, email: str):
    return db.query(Role_userModel).filter(Role_userModel.email == email).first()

def update_role_user(db: Session , role_user: dict , id: int):
   db.query(Role_userModel).filter(Role_userModel.id == id).update(dict(role_user), synchronize_session = False)
   db.commit()
   return role_user


def delete_role_user(db: Session , id:int):
    db_model = db.query(Role_userModel).get(id)
    if db_model:
         db.delete(db_model)
         db.commit() 
         return db_model
            
    else:
          raise HTTPException(status_code=404, detail=ResponseModel([] , "Role_user not found" , True , 404 , {}))
