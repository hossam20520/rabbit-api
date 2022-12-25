
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, HTTPException ,  Request 
import products.models as models_products 
from products.routes import router as products_router 







models_products.Base.metadata.create_all(bind=engine) 







app = FastAPI()
app.include_router(products_router, tags=["Products"], prefix="/api/v1.0/products") 
