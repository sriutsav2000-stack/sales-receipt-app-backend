from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import SessionLocal
from app.models import Receipt
from app.schemas import ReceiptCreate, ReceiptWithItemsCreate, ReceiptUpdate

router = APIRouter(prefix="/receipts", tags=["Receipts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# KEEP YOUR EXISTING ENDPOINT FOR SINGLE PRODUCTS
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

# ADD THIS NEW ENDPOINT FOR MULTIPLE ITEMS
@router.post("/with-items")
def create_receipt_with_items(receipt: ReceiptWithItemsCreate, db: Session = Depends(get_db)):
    receipt_ids = []
    
    for item in receipt.items:
        # Calculate amount for this individual item
        item_amount = item['price'] * item['quantity']
        # Calculate advance received proportionally
        item_advance = (receipt.advance_received / len(receipt.items)) if receipt.items else 0
        total_due = item_amount - item_advance
        
        new_receipt = Receipt(
            date=receipt.date,
            customer_id=receipt.customer_id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            amount=item_amount,
            advance_received=item_advance,
            total_due=total_due,
            due_date=receipt.due_date,
            status=receipt.status
        )
        db.add(new_receipt)
        db.commit()
        db.refresh(new_receipt)
        receipt_ids.append(new_receipt.id)
    
    return {"message": "Receipts created successfully", "ids": receipt_ids}

# KEEP YOUR EXISTING GET ENDPOINT .mlklkknk
@router.get("/")
def get_receipts(db: Session = Depends(get_db)):
    return db.query(Receipt).all()

# GET A PARTICULAR RECEIPT BY ID
@router.get("/{receipt_id}")
def get_receipt_by_id(receipt_id: int, db: Session = Depends(get_db)):
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()

    if not receipt:
        raise HTTPException(
            status_code=404,
            detail=f"Receipt with id {receipt_id} not found"
        )

    return receipt

@router.put("/{receipt_id}")
def update_receipt(
    receipt_id: int,
    receipt_data: ReceiptUpdate,
    db: Session = Depends(get_db)
):
    receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()

    if not receipt:
        raise HTTPException(
            status_code=404,
            detail=f"Receipt with id {receipt_id} not found"
        )

    # Update only provided fields
    for field, value in receipt_data.dict(exclude_unset=True).items():
        setattr(receipt, field, value)

    # Recalculate total_due if financial fields changed
    if (
        receipt_data.amount is not None
        or receipt_data.quantity is not None
        or receipt_data.advance_received is not None
    ):
        receipt.total_due = (
            (receipt.amount * receipt.quantity)
            - receipt.advance_received
        )

    db.commit()
    db.refresh(receipt)

    return {
        "message": "Receipt updated successfully",
        "receipt": receipt
    }
