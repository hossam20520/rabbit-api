from typing import List
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from users.models import UserModel
from users.schemas import UserCreate , User
from database import SessionLocal, engine
from fastapi_crudrouter import SQLAlchemyCRUDRouter





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



router = SQLAlchemyCRUDRouter(
    schema=User,
    create_schema=UserCreate,
    db_model=UserModel,
    # dependencies=[Depends(token_auth)],
    # update_schema=UserCreate
    db=get_db,
    # delete_all_route=False,
    prefix='user'
)

# @router.get('')
# def overloaded_get_all():
#     return 'My overloaded route that returns all the items'