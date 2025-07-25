from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    full_name: Optional[str] = Field(None, description="User's full name")
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    is_active: bool
    balance: float
    created_at: datetime

# Token schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class TokenRefresh(BaseModel):
    refresh_token: str

# Transaction Base Schema
class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0)
    beneficiary: str
    mobile_no: str
    
    model_config = ConfigDict(from_attributes=True)

# DMT (Direct Money Transfer) Schema
class DMTCreate(TransactionBase):
    pass

class DMTResponse(TransactionBase):
    id: int
    order_id: str
    status: str
    transaction_type: str
    created_at: datetime

# Generic Transaction Schema
class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    order_id: str
    status: str
    transaction_type: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Recharge Schema
class RechargeCreate(TransactionBase):
    operator: str = Field(..., description="Mobile operator name")
    circle: str = Field(..., description="Circle or region code")

class RechargeResponse(TransactionBase):
    id: int
    order_id: str
    status: str
    transaction_type: str
    created_at: datetime
    operator: str
    circle: str

# BBPS (Bharat Bill Payment System) Schema
class BBPSCreate(TransactionBase):
    operator_type: str = Field(..., description="Type of bill payment (Electricity, Water, etc.)")
    operator_name: str = Field(..., description="Name of the operator")
    bill_number: str = Field(..., description="Bill number or consumer number")

class BBPSResponse(TransactionBase):
    id: int
    order_id: str
    status: str
    transaction_type: str
    created_at: datetime
    operator_type: str
    operator_name: str
    bill_number: str

# Generic Transaction Response
class TransactionResponse(TransactionBase):
    id: int
    order_id: str
    status: str
    transaction_type: str
    created_at: datetime
