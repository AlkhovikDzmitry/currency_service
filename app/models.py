import enum
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from .database import Base

class TxStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    rejected = "rejected"

class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, nullable=False)
    name = Column(String(100))

class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    id = Column(Integer, primary_key=True)
    currency_code = Column(String(10), nullable=False)
    rate = Column(Numeric(18, 4), nullable=False)
    date = Column(DateTime, default=func.now())

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    status = Column(Enum(TxStatus), default=TxStatus.pending)
    amount_from = Column(Numeric(18, 2), nullable=False)
    currency_from = Column(String(10), nullable=False)
    amount_to = Column(Numeric(18, 2), nullable=False)
    currency_to = Column(String(10), nullable=False)
    rate = Column(Numeric(18, 4), nullable=False)
    created_at = Column(DateTime, default=func.now())