
from typing import List
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import products.models as models
import products.crud as crud 
from products.schemas import ProductCreate , Product
from database import SessionLocal, engine
from global_schemas import ResponseModel , ResponseModelSchema



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



router = APIRouter()

@router.get("/", response_model=List[Product])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@router.delete("/" )
def delete_all_products(db: Session = Depends(get_db)):
	db_product = crud.delete_all_product(db)
	raise  HTTPException(200, ResponseModel([] , "All Products Deleted" , True , 200 , {})) from None

@router.get("/{ product_id}", response_model=Product)
def get_one_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail=ResponseModel([] , "Product not found" , True , 404 , {}))
    return db_product

@router.put("/{id}")
def update_product(id:int ,db: Session = Depends(get_db) , product: ProductCreate = Body(...)):
	db_product = crud.update_product(db, product   ,id)
	return  db_product

@router.delete("/{id}"  )
def delete_one_product(id:int ,db: Session = Depends(get_db)):
	db_product = crud.delete_product(db,id)
	return  db_product