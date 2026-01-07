from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Customer
from app.schemas import CustomerCreate
from app.dependencies import get_current_user

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    new_customer = Customer(
        name=customer.name,
        contact=customer.contact,
        user_id=user_id
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return {"message": "Customer created successfully", "id": new_customer.id}


@router.get("/")
def get_customers(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return db.query(Customer).filter(Customer.user_id == user_id).all()


@router.get("/{customer_id}")
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.user_id == user_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.user_id == user_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted"}
