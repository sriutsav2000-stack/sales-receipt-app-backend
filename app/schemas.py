from pydantic import BaseModel
from datetime import date

class ReceiptCreate(BaseModel):
    due_date: date
    date: date
    customer_id: int
    product_id: int
    quantity: int
    amount: float
    advance_received: float
    status: str

class CustomerCreate(BaseModel):
    name: str
    contact: str

class ProductCreate(BaseModel):
    name: str
    price: float