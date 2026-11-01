from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True)

class LedgerEntry(Base):
    __tablename__ = "ledger"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    entry_type = Column(String, nullable=False)   # "purchase" or "payment"
    item = Column(String)
    quantity = Column(Float, default=0)
    price = Column(Float, default=0)              # price per unit
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)