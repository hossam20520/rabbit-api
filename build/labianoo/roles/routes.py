
from typing import List
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import roles.models as models
import roles.crud as crud 
from roles.schemas import RoleCreate , Role
from database import SessionLocal, engine
from global_schemas import ResponseModel , ResponseModelSchema
from auth.RoleChecker import  RoleCheckerByToken
from auth.jwt_bearer import JWTBearer
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_bearer import JWTBearer , decodeJWT

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.get("/", response_model=List[Role] , dependencies=[ Depends( JWTBearer())])
def get_all_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme) ): 
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "read__roles")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    roles = crud.get_roles(db, skip=skip, limit=limit)
    # print(token)
    return roles

@router.post("/", response_model=Role , dependencies=[ Depends( JWTBearer())])
def create_role(role: RoleCreate, db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "create__roles")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    return crud.create_role(db=db, role=role)

@router.delete("/" , dependencies=[ Depends( JWTBearer())])
def delete_all_roles(db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "delete__roles")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    crud.delete_all_role(db)
    raise  HTTPException(200, ResponseModel([] , "All Roles Deleted" , True , 200 , {})) from None


@router.get("/{role_id}", response_model=Role , dependencies=[ Depends( JWTBearer())])
def get_one_role(role_id: int, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
        # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "show__role")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_role = crud.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail=ResponseModel([] , "Role not found" , True , 404 , {}))
    return db_role

@router.put("/{id}" , dependencies=[ Depends( JWTBearer())])
def update_role(id:int ,db: Session = Depends(get_db) , role: RoleCreate = Body(...) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "update__role")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_role = crud.update_role(db, role   ,id)
    return  db_role

@router.delete("/{id}"  , dependencies=[ Depends( JWTBearer())] )
def delete_one_role(id:int ,db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "roles" , db , "delete__roles")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_role = crud.delete_role(db,id)
    return  db_role