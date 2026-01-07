from pydantic import BaseModel
import datetime
from typing import List, Optional

# Keep your existing schemas exactly as they are
class ReceiptCreate(BaseModel):
    due_date: datetime.date
    date: datetime.date
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
    due_date: datetime.date
    date: datetime.date
    customer_id: int
    items: List[dict]  # This matches your frontend structure
    amount: float
    advance_received: float
    status: str

class ReceiptUpdate(BaseModel):
    date: Optional[datetime.date] = None
    due_date: Optional[datetime.date] = None
    quantity: Optional[int] = None
    amount: Optional[float] = None
    advance_received: Optional[float] = None
    status: Optional[str] = None
    customer_id: Optional[int] = None
    product_id: Optional[int] = None

class RegisterRequest(BaseModel):
    name: str
    email: Optional[str] = None
    mobile: Optional[str] = None

class LoginRequest(BaseModel):
    email: Optional[str] = None
    mobile: Optional[str] = None

class OtpVerifyRequest(BaseModel):
    user_id: int
    otp: str
