from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import SessionLocal
from app.models import Customer, Receipt

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/top-customers")
def get_top_customers(db: Session = Depends(get_db)):
    """
    Returns top 5 customers by total due (sum of all receipts per customer).
    A customer may have multiple receipts — all are aggregated.
    """

    results = (
        db.query(
            Customer.id.label("customer_id"),
            Customer.name.label("name"),
            func.sum(Receipt.total_due).label("total_due")
        )
        .join(Receipt, Receipt.customer_id == Customer.id)
        .group_by(Customer.id, Customer.name)
        .order_by(func.sum(Receipt.total_due).desc())
        .limit(5)
        .all()
    )

    return [
        {
            "customer_id": r.customer_id,
            "name": r.name,
            "total_due": float(r.total_due)
        }
        for r in results
    ]


@router.get("/")
def dashboard_overview(db: Session = Depends(get_db)):
    """
    Main dashboard endpoint.
    Currently returns: top 5 customers by total due.
    """

    top_customers = (
        db.query(
            Customer.id.label("customer_id"),
            Customer.name.label("name"),
            func.sum(Receipt.total_due).label("total_due")
        )
        .join(Receipt, Receipt.customer_id == Customer.id)
        .group_by(Customer.id, Customer.name)
        .order_by(func.sum(Receipt.total_due).desc())
        .limit(5)
        .all()
    )

    return {
        "top_customers": [
            {
                "customer_id": r.customer_id,
                "name": r.name,
                "total_due": float(r.total_due)
            }
            for r in top_customers
        ]
    }
