from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import enum
from app.core.database import Base

class TransactionStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"

class TransactionType(str, enum.Enum):
    DMT = "Money Transfer"
    RECHARGE = "Recharge"
    BBPS = "Bill Payment"
    VERIFICATION = "Verification"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    transaction_type = Column(String)
    status = Column(Enum(TransactionStatus))
    beneficiary = Column(String)
    mobile_no = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class BBPSTransaction(Base):
    __tablename__ = "bbps_transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    client_ref = Column(String)
    operator_type = Column(String)
    operator_name = Column(String)
    bill_number = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
