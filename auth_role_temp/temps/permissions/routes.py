
from typing import List
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import permissions.models as models
import permissions.crud as crud 
from permissions.schemas import PermissionCreate , Permission
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

@router.get("/", response_model=List[Permission] , dependencies=[Depends(JWTBearer())])
def get_all_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)   , token: str = Depends(oauth2_scheme)):
        # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "read__permissions")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    permissions = crud.get_permissions(db, skip=skip, limit=limit)
    return permissions

@router.post("/", response_model=Permission , dependencies=[Depends(JWTBearer())])
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
     # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "create__permission")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    return crud.create_permission(db=db, permission=permission)

@router.delete("/" , dependencies=[Depends(JWTBearer())] )
def delete_all_permissions(db: Session = Depends(get_db)  , token: str = Depends(JWTBearer) ):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "delete__permissions")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_permission = crud.delete_all_permission(db)
    raise  HTTPException(200, ResponseModel([] , "All Permissions Deleted" , True , 200 , {})) from None

@router.get("/{permission_id}", response_model=Permission , dependencies=[Depends(JWTBearer())])
def get_one_permission(permission_id: int, db: Session = Depends(get_db) , token: str = Depends(JWTBearer) ):
        # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "show__permission")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_permission = crud.get_permission(db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail=ResponseModel([] , "Permission not found" , True , 404 , {}))
    return db_permission

@router.put("/{id}" , dependencies=[Depends(JWTBearer())])
def update_permission(id:int ,db: Session = Depends(get_db) , permission: PermissionCreate = Body(...) , token: str = Depends(JWTBearer) ):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "update__permission")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_permission = crud.update_permission(db, permission   ,id)
    return  db_permission

@router.delete("/{id}" , dependencies=[Depends(JWTBearer())] )
def delete_one_permission(id:int ,db: Session = Depends(get_db) , token: str = Depends(JWTBearer)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "delete__permission")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_permission = crud.delete_permission(db,id)
    return  db_permission