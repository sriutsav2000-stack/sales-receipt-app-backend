from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.db import SessionLocal
from app.models import Receipt

router = APIRouter(prefix="/receipts", tags=["Receipts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_receipt(
    date: date,
    customer_id: int,
    product_id: int,
    quantity: int,
    amount: float,
    advance_received: float,
    db: Session = Depends(get_db)
):
    total_due = (amount * quantity) - advance_received
    new_receipt = Receipt(
        date=date,
        customer_id=customer_id,
        product_id=product_id,
        quantity=quantity,
        amount=amount,
        advance_received=advance_received,
        total_due=total_due
    )
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)
    return {"message": "Receipt created successfully", "id": new_receipt.id}

@router.get("/")
def get_receipts(db: Session = Depends(get_db)):
    return db.query(Receipt).all()
