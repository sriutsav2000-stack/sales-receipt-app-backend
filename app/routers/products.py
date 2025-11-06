from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Product

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_product(name: str, price: float, db: Session = Depends(get_db)):
    existing = db.query(Product).filter(Product.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product already exists")
    new_product = Product(name=name, price=price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product created", "id": new_product.id}


@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
