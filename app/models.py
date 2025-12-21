from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact = Column(String, nullable=True)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


    receipts = relationship("Receipt", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


    receipts = relationship("Receipt", back_populates="product")


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    advance_received = Column(Float, nullable=False)
    total_due = Column(Float, nullable=False)
    due_date = Column(Date, nullable = True)
    status = Column(String, nullable = False)
    receipt_image = Column(String, nullable=True)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)



    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    customer = relationship("Customer", back_populates="receipts")
    product = relationship("Product", back_populates="receipts")

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
