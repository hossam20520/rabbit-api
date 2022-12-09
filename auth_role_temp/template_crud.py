TEMPLATE = """
from sqlalchemy.orm import Session
from {{ element.names}}.models import {{ element.Name }}Model
from {{ element.names}}.schemas import {{ element.Name }}Create , {{ element.Name }}
from fastapi import Depends, HTTPException
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.exc import IntegrityError
from global_schemas import ResponseModel



def get_{{ element.names}}(db: Session, skip: int = 0, limit: int = 100):
    return db.query({{ element.Name }}Model).offset(skip).limit(limit).all()


def create_{{ element.name}}(db: Session, {{ element.name}}:{{ element.Name }}):
    try:
        db_{{ element.name}}  = {{ element.Name }}Model(**{{ element.name}}.dict())
        db.add(db_{{ element.name}})
        db.commit()
        db.refresh(db_{{ element.name}})
    except IntegrityError:
         db.rollback()
         raise HTTPException(422, ResponseModel([] , "{{ element.Name }} already exist" , False , 422 , {"error":"Already exists"})) from None
    return db_{{ element.name}}


def delete_all_{{ element.name}}(db: Session):
    db.query({{ element.Name }}Model).delete()
    db.commit()
    return []


def get_{{ element.name}}(db: Session, {{ element.name}}_id: int):
    return db.query({{ element.Name }}Model).filter({{ element.Name }}Model.id == {{ element.name}}_id).first()


def get_{{ element.name}}_by_email(db: Session, email: str):
    return db.query({{ element.Name }}Model).filter({{ element.Name }}Model.email == email).first()

def update_{{ element.name}}(db: Session , {{ element.name}}: dict , id: int):
   db.query({{ element.Name }}Model).filter({{ element.Name }}Model.id == id).update(dict({{ element.name}}), synchronize_session = False)
   db.commit()
   return {{ element.name}}


def delete_{{ element.name}}(db: Session , id:int):
    db_model = db.query({{ element.Name }}Model).get(id)
    if db_model:
         db.delete(db_model)
         db.commit() 
         return db_model
            
    else:
          raise HTTPException(status_code=404, detail=ResponseModel([] , "{{ element.Name }} not found" , True , 404 , {}))

"""