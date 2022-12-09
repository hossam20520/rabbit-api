from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
from typing import Optional ,List
from fastapi import FastAPI, Header
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt_handler import decodeJWT
from users.schemas import User
from sqlalchemy.orm import Session
from users.models import UserModel
from fastapi.encoders import jsonable_encoder
from permissions.models import PermissionModel
from permission_roles.schemas import Permission_roleCreate , Permission_role
from permission_roles.models import Permission_roleModel
from role_users.models import Role_userModel
from role_users.schemas import Role_userCreate , Role_user
from global_schemas import ResponseModel , ResponseModelSchema
from fastapi.encoders import jsonable_encoder
from permissions.models import PermissionModel
from permission_roles.models import Permission_roleModel
from role_users.models import Role_userModel
from roles.models import RoleModel
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



class RoleCheckerByToken:
    def __init__(self, token , table , db , crud):
        self.db = db
        self.token = token
        self.table = table
        self.crud = crud

    def __call__(self , id):
       data = self.db.query(UserModel).filter(UserModel.id == id).first()
       data = jsonable_encoder(data)
       if self.crud in self.getPermissions(data['role_id']):
          pass 
       else:
           raise HTTPException(status_code=403, detail=ResponseModel([] , "Operation not permitted", False , 403  , {}))
    def getPermissions(self , roleID):
        q = (self.db.query(  Permission_roleModel, RoleModel  , PermissionModel )
        .join(PermissionModel , PermissionModel.id == Permission_roleModel.permission_id)
        .filter(RoleModel.id == roleID)
        .filter(Permission_roleModel.role_id == RoleModel.id)
        ).all()

        permissions = []
        for ite in q:
           data = jsonable_encoder(ite)
           json = data['PermissionModel']
        # print()
           permissions.append(json['title'])
        return permissions