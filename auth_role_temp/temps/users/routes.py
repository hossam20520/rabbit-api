from typing import List
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import users.models as models
import users.crud as crud 
from users.schemas import UserCreate , User
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
 
@router.get("/", response_model=List[User] , dependencies=[ Depends( JWTBearer())])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme) ):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "users" , db , "read__users")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=User ,  dependencies=[ Depends( JWTBearer())])
def create_user(user: UserCreate, db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme) ):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "users" , db , "create__user")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    return crud.create_user(db=db, user=user)
    
#JWTBearer
@router.delete("/" ,  dependencies=[ Depends( JWTBearer())] )
def delete_all_users(db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "users" , db , "delete__users")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    crud.delete_all_user(db)
    raise  HTTPException(200, ResponseModel([] , "All Users Deleted" , True , 200 , {})) from None

@router.get("/{user_id}", response_model=User ,  dependencies=[ Depends( JWTBearer())])
def get_one_user(user_id: int, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "users" , db , "show__user")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=ResponseModel([] , "User not found" , True , 404 , {}))
    return db_user

@router.put("/{id}" ,  dependencies=[ Depends( JWTBearer())])
def update_user(id:int ,db: Session = Depends(get_db) , user: UserCreate = Body(...) ,  token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "users" , db , "update__user")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_user = crud.update_user(db, user   ,id)
    return  db_user

@router.delete("/{id}" ,  dependencies=[ Depends( JWTBearer())]  )
def delete_one_user(id:int ,db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme)):
	# Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "users" , db , "delete__user")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_user = crud.delete_user(db,id)
    return  db_user