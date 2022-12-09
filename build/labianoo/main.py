
from database import SessionLocal, engine
from auth.login import router as login_router
from auth.register import router as register_router
import users.models as models
from fastapi import Depends, FastAPI, HTTPException ,  Request 
import products.models as models_products 
from products.routes import router as products_router 









models.Base.metadata.create_all(bind=engine) 
models_products.Base.metadata.create_all(bind=engine) 







app = FastAPI()



app.include_router(login_router, tags=["login"], prefix="/api/v1.0/login")
app.include_router(register_router, tags=["register"], prefix="/api/v1.0/register")
app.include_router(products_router, tags=["Products"], prefix="/api/v1.0/products") 
