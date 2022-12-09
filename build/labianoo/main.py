
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException ,  Request 
import users.models as models_users 
import permissions.models as models_permissions 
import products.models as models_products 
from users.routes import router as users_router 
from permissions.routes import router as permissions_router 
from products.routes import router as products_router 







models_users.Base.metadata.create_all(bind=engine) 
models_permissions.Base.metadata.create_all(bind=engine) 
models_products.Base.metadata.create_all(bind=engine) 







app = FastAPI()
app.include_router(users_router, tags=["Users"], prefix="/api/v1.0/users") 
app.include_router(permissions_router, tags=["Permissions"], prefix="/api/v1.0/permissions") 
app.include_router(products_router, tags=["Products"], prefix="/api/v1.0/products") 
