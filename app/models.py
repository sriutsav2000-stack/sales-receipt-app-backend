from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=True)
    mobile = Column(String, unique=True, nullable=True)
    is_verified = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class OtpLog(Base):
    __tablename__ = "otp_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    otp = Column(String)
    expiry = Column(DateTime)
    is_used = Column(Integer, default=0)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

class Receipt(Base):
    __tablename__ = "receipts"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    quantity = Column(Integer)
    amount = Column(Float)
    advance_received = Column(Float)
    total_due = Column(Float)
    due_date = Column(Date)
    status = Column(String)
    receipt_image = Column(String)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
