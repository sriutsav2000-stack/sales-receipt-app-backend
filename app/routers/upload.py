from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import shutil, os, uuid
from datetime import date, timedelta

from app.database import get_db
from app.models import Customer, Product, Receipt
from app.dependencies import get_current_user

router = APIRouter(prefix="/receipts", tags=["Receipt Upload"])

UPLOAD_DIR = "media/receipts"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-image")
def upload_receipt_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_customer_name = "Auto Customer"
    extracted_product_name = "Auto Product"
    extracted_product_price = 100.0
    extracted_quantity = 2
    extracted_advance = 50.0

    total_amount = extracted_product_price * extracted_quantity
    total_due = total_amount - extracted_advance

    customer = db.query(Customer).filter(
        Customer.name == extracted_customer_name,
        Customer.user_id == user_id
    ).first()

    if not customer:
        customer = Customer(
            name=extracted_customer_name,
            contact="0000000000",
            user_id=user_id
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

    product = db.query(Product).filter(
        Product.name == extracted_product_name,
        Product.user_id == user_id
    ).first()

    if not product:
        product = Product(
            name=extracted_product_name,
            price=extracted_product_price,
            user_id=user_id
        )
        db.add(product)
        db.commit()
        db.refresh(product)

    receipt = Receipt(
        date=date.today(),
        due_date=date.today() + timedelta(days=14),
        status="Open",
        quantity=extracted_quantity,
        amount=total_amount,
        advance_received=extracted_advance,
        total_due=total_due,
        customer_id=customer.id,
        product_id=product.id,
        receipt_image=file_path,
        user_id=user_id
    )

    db.add(receipt)
    db.commit()
    db.refresh(receipt)

    return {
        "message": "Receipt uploaded successfully",
        "receipt_id": receipt.id,
        "customer": customer.name,
        "product": product.name,
        "total_amount": total_amount,
        "total_due": total_due,
        "image_path": file_path
    }
