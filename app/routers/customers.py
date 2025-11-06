from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Customer

router = APIRouter(prefix="/customers", tags=["Customers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_customer(name: str, contact: str = None, db: Session = Depends(get_db)):
    existing = db.query(Customer).filter(Customer.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Customer already exists")
    new_customer = Customer(name=name, contact=contact)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return {"message": "Customer created", "id": new_customer.id}


@router.get("/")
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


@router.get("/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted"}
