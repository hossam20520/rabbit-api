from fastapi.security import HTTPBasicCredentials, HTTPBasic
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from users.models import UserModel
from users.schemas import UserCreate , User
security = HTTPBasic()
from auth.jwt_handler import signJWT
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException , status
from database import SessionLocal, engine
from global_schemas import ResponseModel , ResponseModelSchema
from fastapi.encoders import jsonable_encoder
from auth.schemas import RegisterSchema
from sqlalchemy.exc import IntegrityError

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



router = APIRouter()


hash_helper = CryptContext(schemes=["bcrypt"])

@router.post("/")
def Register(db: Session = Depends(get_db) ,register: RegisterSchema = Body(...)):
    # NEW CODE
    register.hashed_password  =  hash_helper.encrypt(register.hashed_password) 
    
    user = db.query(UserModel).filter(UserModel.email == register.email).first()
    username = db.query(UserModel).filter(UserModel.username == register.username).first()
    data = jsonable_encoder(user)
    if (user):
         raise HTTPException(status_code=200, detail=ResponseModel([] , "Email already exists" , True , 200 , {}))
        #  return "Email already exists"
    if (username):
        raise HTTPException(status_code=200, detail=ResponseModel([] , "Username already exists" , True , 200 , {}))

    
    db_user  = UserModel(**register.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    data = jsonable_encoder(db_user)
    # Here you can controll in fields 
    data.pop('hashed_password', None)
    return data
