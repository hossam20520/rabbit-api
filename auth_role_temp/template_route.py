TEMPLATE = """
from typing import List
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import {{element.names}}.models as models
import {{element.names}}.crud as crud 
from {{element.names}}.schemas import {{element.Name}}Create , {{element.Name}}
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
 
@router.get("/", response_model=List[{{element.Name}}] , dependencies=[ Depends( JWTBearer())])
def get_all_{{element.names}}(skip: int = 0, limit: int = 100, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme) ):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "{{element.names}}" , db , "read__{{element.names}}")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    {{element.names}} = crud.get_{{element.names}}(db, skip=skip, limit=limit)
    return {{element.names}}

@router.post("/", response_model={{element.Name}} ,  dependencies=[ Depends( JWTBearer())])
def create_{{element.name}}({{element.name}}: {{element.Name}}Create, db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme) ):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "{{element.names}}" , db , "create__{{element.name}}")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    return crud.create_{{element.name}}(db=db, {{element.name}}={{element.name}})
    
#JWTBearer
@router.delete("/" ,  dependencies=[ Depends( JWTBearer())] )
def delete_all_{{element.names}}(db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "{{element.names}}" , db , "delete__{{element.names}}")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    crud.delete_all_{{element.name}}(db)
    raise  HTTPException(200, ResponseModel([] , "All {{element.names}} Deleted" , True , 200 , {})) from None

@router.get("/{ {{element.name}}_id}", response_model={{element.Name}} ,  dependencies=[ Depends( JWTBearer())])
def get_one_{{element.name}}({{element.name}}_id: int, db: Session = Depends(get_db) , token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "{{element.names}}" , db , "show__{{element.name}}")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_{{element.name}} = crud.get_{{element.name}}(db, {{element.name}}_id={{element.name}}_id)
    if db_{{element.name}} is None:
        raise HTTPException(status_code=404, detail=ResponseModel([] , "{{element.Name}} not found" , True , 404 , {}))
    return db_{{element.name}}

@router.put("/{id}" ,  dependencies=[ Depends( JWTBearer())])
def update_{{element.name}}(id:int ,db: Session = Depends(get_db) , {{element.name}}: {{element.Name}}Create = Body(...) ,  token: str = Depends(oauth2_scheme)):
    # Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "{{element.names}}" , db , "update__{{element.name}}")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_{{element.name}} = crud.update_{{element.name}}(db, {{element.name}}   ,id)
    return  db_{{element.name}}

@router.delete("/{id}" ,  dependencies=[ Depends( JWTBearer())]  )
def delete_one_{{element.name}}(id:int ,db: Session = Depends(get_db) ,  token: str = Depends(oauth2_scheme)):
	# Start RoleCheckerByToken
    userToken = decodeJWT(token)
    allow_access = RoleCheckerByToken(token, "{{element.names}}" , db , "delete__{{element.name}}")
    allow_access.__call__(userToken['user_id']['id'])
    # End RoleCheckerByToken
    db_{{element.name}} = crud.delete_{{element.name}}(db,id)
    return  db_{{element.name}}
"""