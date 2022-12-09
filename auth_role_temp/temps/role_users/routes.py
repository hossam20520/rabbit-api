
from typing import List
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import role_users.models as models
import role_users.crud as crud 
from role_users.schemas import Role_userCreate , Role_user
from database import SessionLocal, engine
from global_schemas import ResponseModel , ResponseModelSchema
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_bearer import JWTBearer , decodeJWT
from auth.RoleChecker import  RoleCheckerByToken


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.get("/", response_model=List[Role_user] , dependencies=[ Depends( JWTBearer())])
def get_all_role_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "read__role_users")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    role_users = crud.get_role_users(db, skip=skip, limit=limit)
    return role_users

@router.post("/", response_model=Role_user , dependencies=[ Depends( JWTBearer())])
def create_role_user(role_user: Role_userCreate, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "create__role_users")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    return crud.create_role_user(db=db, role_user=role_user)

@router.delete("/" , dependencies=[ Depends( JWTBearer())] )
def delete_all_role_users(db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "delete__role_users")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_role_user = crud.delete_all_role_user(db)
    raise  HTTPException(200, ResponseModel([] , "All Role_users Deleted" , True , 200 , {})) from None

@router.get("/{role_user_id}", response_model=Role_user , dependencies=[ Depends( JWTBearer())])
def get_one_role_user(role_user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "show__role_user")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_role_user = crud.get_role_user(db, role_user_id=role_user_id)
    if db_role_user is None:
       raise HTTPException(status_code=404, detail=ResponseModel([] , "Role_user not found" , True , 404 , {}))

@router.put("/{id}" ,  dependencies=[ Depends( JWTBearer())])
def update_role_user(id:int ,db: Session = Depends(get_db) , role_user: Role_userCreate = Body(...) ,  token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "update__role_user")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_role_user = crud.update_role_user(db, role_user   ,id)
    return  db_role_user

@router.delete("/{id}" ,dependencies=[ Depends( JWTBearer())]  )
def delete_one_role_user(id:int ,db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "delete__role_user")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_role_user = crud.delete_role_user(db,id)
    return  db_role_user