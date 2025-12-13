from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
import uuid
from datetime import date, timedelta

from app.database import get_db
from app.models import Customer
from app.models import Product
from app.models import Receipt

router = APIRouter(
    prefix="/receipts",
    tags=["Receipt Upload"]
)

UPLOAD_DIR = "media/receipts"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload-image")
def upload_receipt_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # ---------- 1. Save image ----------
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ---------- 2. Dummy extracted data ----------
    extracted_customer_name = "Auto Customer"
    extracted_product_name = "Auto Product"
    extracted_product_price = 100.0
    extracted_quantity = 2
    extracted_advance = 50.0

    total_amount = extracted_product_price * extracted_quantity
    total_due = total_amount - extracted_advance

    # ---------- 3. Create / Get Customer ----------
    customer = db.query(Customer).filter(
        Customer.name == extracted_customer_name
    ).first()

    if not customer:
        customer = Customer(
            name=extracted_customer_name,
            contact="0000000000"
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

    # ---------- 4. Create / Get Product ----------
    product = db.query(Product).filter(
        Product.name == extracted_product_name
    ).first()

    if not product:
        product = Product(
            name=extracted_product_name,
            price=extracted_product_price
        )
        db.add(product)
        db.commit()
        db.refresh(product)

    # ---------- 5. Create Receipt ----------
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
        receipt_image=file_path  # optional column
    )

    db.add(receipt)
    db.commit()
    db.refresh(receipt)

    # ---------- 6. Response ----------
    return {
        "message": "Receipt uploaded successfully (dummy data)",
        "receipt_id": receipt.id,
        "customer": customer.name,
        "product": product.name,
        "total_amount": total_amount,
        "total_due": total_due,
        "image_path": file_path
    }
