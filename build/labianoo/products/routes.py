
from typing import List
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import products.models as models
import products.crud as crud 
from products.schemas import ProductCreate , Product
from database import SessionLocal, engine
from global_schemas import ResponseModel , ResponseModelSchema
from auth.RoleChecker import  RoleCheckerByToken
from auth.jwt_bearer import JWTBearer , decodeJWT
from fastapi.security import OAuth2PasswordBearer
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()
 
@router.get("/", response_model=List[Product] , dependencies=[ Depends( JWTBearer())])
def get_all_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme) ):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "products" , db , "read__products")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=Product ,  dependencies=[ Depends( JWTBearer())])
def create_product(product: ProductCreate, db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme) ):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "products" , db , "create__product")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    return crud.create_product(db=db, product=product)
    
#JWTBearer
@router.delete("/" ,  dependencies=[ Depends( JWTBearer())] )
def delete_all_products(db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "products" , db , "delete__products")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    crud.delete_all_product(db)
    raise  HTTPException(200, ResponseModel([] , "All products Deleted" , True , 200 , {})) from None

@router.get("/{ product_id}", response_model=Product ,  dependencies=[ Depends( JWTBearer())])
def get_one_product(product_id: int, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "products" , db , "show__product")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail=ResponseModel([] , "Product not found" , True , 404 , {}))
    return db_product

@router.put("/{id}" ,  dependencies=[ Depends( JWTBearer())])
def update_product(id:int ,db: Session = Depends(get_db) , product: ProductCreate = Body(...) ,  token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "products" , db , "update__product")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_product = crud.update_product(db, product   ,id)
    return  db_product

@router.delete("/{id}" ,  dependencies=[ Depends( JWTBearer())]  )
def delete_one_product(id:int ,db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme)):
	# Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "products" , db , "delete__product")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_product = crud.delete_product(db,id)
    return  db_product