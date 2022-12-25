
from sqlalchemy.orm import Session
from products.models import ProductModel
from products.schemas import ProductCreate , Product
from fastapi import Depends, HTTPException
from sqlalchemy.ext.declarative import DeclarativeMeta as Model
from sqlalchemy.exc import IntegrityError
from global_schemas import ResponseModel



def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ProductModel).offset(skip).limit(limit).all()


def create_product(db: Session, product:Product):
    try:
        db_product  = ProductModel(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    except IntegrityError:
         db.rollback()
         raise HTTPException(422, ResponseModel([] , "Product already exist" , False , 422 , {"error":"Already exists"})) from None
    return db_product


def delete_all_product(db: Session):
    db.query(ProductModel).delete()
    db.commit()
    return []


def get_product(db: Session, product_id: int):
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def get_product_by_email(db: Session, email: str):
    return db.query(ProductModel).filter(ProductModel.email == email).first()

def update_product(db: Session , product: dict , id: int):
   db.query(ProductModel).filter(ProductModel.id == id).update(dict(product), synchronize_session = False)
   db.commit()
   return product


def delete_product(db: Session , id:int):
    db_model = db.query(ProductModel).get(id)
    if db_model:
         db.delete(db_model)
         db.commit() 
         return db_model
            
    else:
          raise HTTPException(status_code=404, detail=ResponseModel([] , "Product not found" , True , 404 , {}))
