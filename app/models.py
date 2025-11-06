from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact = Column(String, nullable=True)

    receipts = relationship("Receipt", back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    receipts = relationship("Receipt", back_populates="product")


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    advance_received = Column(Float, nullable=False)
    total_due = Column(Float, nullable=False)

    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    customer = relationship("Customer", back_populates="receipts")
    product = relationship("Product", back_populates="receipts")
