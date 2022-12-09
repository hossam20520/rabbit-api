
from typing import List
from fastapi import APIRouter, Body
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import users.models as models
import users.crud as crud 
from users.schemas import UserCreate , User
from database import SessionLocal, engine
from global_schemas import ResponseModel , ResponseModelSchema



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



router = APIRouter()

@router.get("/", response_model=List[User])
def get_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@router.delete("/" )
def delete_all_users(db: Session = Depends(get_db)):
	db_user = crud.delete_all_user(db)
	raise  HTTPException(200, ResponseModel([] , "All Users Deleted" , True , 200 , {})) from None

@router.get("/{ user_id}", response_model=User)
def get_one_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=ResponseModel([] , "User not found" , True , 404 , {}))
    return db_user

@router.put("/{id}")
def update_user(id:int ,db: Session = Depends(get_db) , user: UserCreate = Body(...)):
	db_user = crud.update_user(db, user   ,id)
	return  db_user

@router.delete("/{id}"  )
def delete_one_user(id:int ,db: Session = Depends(get_db)):
	db_user = crud.delete_user(db,id)
	return  db_user