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
from permission_roles.models import Permission_roleModel
from role_users.models import Role_userModel
from permissions.models import PermissionModel

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()
hash_helper = CryptContext(schemes=["bcrypt"])
def getPermissions(db , id):
    user_role =  db.query(Role_userModel).filter(Role_userModel.user_id == id).first()
    if user_role:
        pass 
    else: 
        return  []
    user_role_data = jsonable_encoder(user_role)
    # print(user_role_data)
    permissions =  db.query(Permission_roleModel).filter(Permission_roleModel.role_id == user_role_data['role_id']).all()
    permissions_data = jsonable_encoder(permissions)
    # print(permissions_data)
    listPerm = []
    for item in permissions_data:
        permission =  db.query(PermissionModel).filter(PermissionModel.id == item['permission_id']).first()
        perm_data = jsonable_encoder(permission)
        listPerm.append(perm_data['title'])
    return listPerm

@router.post("/")
def Login(db: Session = Depends(get_db) ,user_credentials: HTTPBasicCredentials = Body(...)):
    # NEW CODE
    user = db.query(UserModel).filter(UserModel.email == user_credentials.username).first()
    data = jsonable_encoder(user)
  
    if (user):
        password = hash_helper.verify(
            user_credentials.password,  data['hashed_password'] )
        if (password):
            permissions = getPermissions(db , data['id'])
            return signJWT(data['id'] , user , permissions)

        raise HTTPException(status_code=401 , detail=ResponseModel([] , "Incorrect email or password" , True , 401  , {}))

    raise HTTPException(status_code=401 , detail=ResponseModel([] , "Incorrect email or password" , True , 401  , {}))
