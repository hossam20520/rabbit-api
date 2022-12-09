
from typing import List
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import permission_roles.models as models
import permission_roles.crud as crud 
from permission_roles.schemas import Permission_roleCreate , Permission_role
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

@router.get("/", response_model=List[Permission_role] ,  dependencies=[ Depends( JWTBearer())])
def get_all_permission_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "read__permission_roles")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    permission_roles = crud.get_permission_roles(db, skip=skip, limit=limit)
    return permission_roles

@router.post("/", response_model=Permission_role ,  dependencies=[ Depends( JWTBearer())])
def create_permission_role(permission_role: Permission_roleCreate, db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme)):
        # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "create__permission_role")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    return crud.create_permission_role(db=db, permission_role=permission_role)

@router.delete("/"  ,  dependencies=[ Depends( JWTBearer())])
def delete_all_permission_roles(db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "delete__permission_roles")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_permission_role = crud.delete_all_permission_role(db)
    raise  HTTPException(200, ResponseModel([] , "All Permission_roles Deleted" , True , 200 , {})) from None

@router.get("/{permission_role_id}", response_model=Permission_role , dependencies=[ Depends( JWTBearer())])
def get_one_permission_role(permission_role_id: int, db: Session = Depends(get_db)  , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "show__permission_role")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_permission_role = crud.get_permission_role(db, permission_role_id=permission_role_id)
    if db_permission_role is None:
        raise HTTPException(status_code=404, detail=ResponseModel([] , "Permission_role not found" , True , 404 , {}))
    return db_permission_role

@router.put("/{id}" , dependencies=[ Depends( JWTBearer())])
def update_permission_role(id:int ,db: Session = Depends(get_db) , permission_role: Permission_roleCreate = Body(...) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "update__permission_role")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_permission_role = crud.update_permission_role(db, permission_role   ,id)
    return  db_permission_role

@router.delete("/{id}" , dependencies=[ Depends( JWTBearer())]  )
def delete_one_permission_role(id:int ,db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "delete__permission_role")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_permission_role = crud.delete_permission_role(db,id)
    return  db_permission_role