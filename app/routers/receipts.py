from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.db import SessionLocal
from app.models import Receipt
from app.schemas import ReceiptCreate

router = APIRouter(prefix="/receipts", tags=["Receipts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_receipt(receipt: ReceiptCreate, db: Session = Depends(get_db)):
    total_due = (receipt.amount * receipt.quantity) - receipt.advance_received
    new_receipt = Receipt(
        date=receipt.date,
        customer_id=receipt.customer_id,
        product_id=receipt.product_id,
        quantity=receipt.quantity,
        amount=receipt.amount,
        advance_received=receipt.advance_received,
        total_due=total_due,
        due_date= receipt.due_date,
        status= receipt.status
    )
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)
    return {"message": "Receipt created successfully", "id": new_receipt.id}

@router.get("/")
def get_receipts(db: Session = Depends(get_db)):
    return db.query(Receipt).all()
