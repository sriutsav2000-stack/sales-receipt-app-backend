from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.schemas import ProductCreate
from app.dependencies import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    new_product = Product(
        name=product.name,
        price=product.price,
        user_id=user_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product created successfully", "id": new_product.id}


@router.get("/")
def get_products(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(Product).filter(Product.user_id == user_id).all()


@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.user_id == user_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.user_id == user_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
