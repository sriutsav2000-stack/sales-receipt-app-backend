from pydantic import BaseModel
from datetime import date
from typing import List, Optional

# Keep your existing schemas exactly as they are
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

# ADD THIS NEW SCHEMA FOR MULTIPLE ITEMS
class ReceiptWithItemsCreate(BaseModel):
    due_date: date
    date: date
    customer_id: int
    items: List[dict]  # This matches your frontend structure
    amount: float
    advance_received: float
    status: str