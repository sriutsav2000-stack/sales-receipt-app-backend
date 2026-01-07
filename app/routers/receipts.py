from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Receipt
from app.schemas import ReceiptCreate, ReceiptWithItemsCreate, ReceiptUpdate
from app.dependencies import get_current_user

router = APIRouter(prefix="/receipts", tags=["Receipts"])

@router.post("/")
def create_receipt(
    receipt: ReceiptCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    total_due = (receipt.amount * receipt.quantity) - receipt.advance_received

    new_receipt = Receipt(
        date=receipt.date,
        customer_id=receipt.customer_id,
        product_id=receipt.product_id,
        quantity=receipt.quantity,
        amount=receipt.amount,
        advance_received=receipt.advance_received,
        total_due=total_due,
        due_date=receipt.due_date,
        status=receipt.status,
        user_id=user_id
    )
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)

    return {"message": "Receipt created successfully", "id": new_receipt.id}


@router.get("/")
def get_receipts(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(Receipt).filter(Receipt.user_id == user_id).all()


@router.get("/{receipt_id}")
def get_receipt_by_id(
    receipt_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    receipt = db.query(Receipt).filter(
        Receipt.id == receipt_id,
        Receipt.user_id == user_id
    ).first()

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    return receipt


@router.put("/{receipt_id}")
def update_receipt(
    receipt_id: int,
    receipt_data: ReceiptUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    receipt = db.query(Receipt).filter(
        Receipt.id == receipt_id,
        Receipt.user_id == user_id
    ).first()

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    for field, value in receipt_data.dict(exclude_unset=True).items():
        setattr(receipt, field, value)

    receipt.total_due = (receipt.amount * receipt.quantity) - receipt.advance_received
    db.commit()
    db.refresh(receipt)

    return {"message": "Receipt updated successfully"}
