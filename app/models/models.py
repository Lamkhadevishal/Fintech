from sqlalchemy import Column,Boolean,String,Integer,String,Text,Float,DateTime,Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# creating table for company name
class CompanyName(base):
    __tablename__="company_name"

    company_full_name = Column(String,nullable=False)
    company_name = Column(String,nullable=False)
    company_website = Column(String)
    sender_id = Column(Integer,ForeignKey("user.id"),nullable=False) 
    sms_user = Column(Integer)
    sms_password = Column(String)
    company_logo = Column(LargeBinary)
    company_news =Column(Text)
    company_bill_notice = Column(Text)
    company_notice = Column(Text)
    company_contact_no = Column(Integer)
    company_email = Column(String,unique=True,Index=True)

# creating table for fund_action
class FundActionEnum(str,enum.Enum):
    transfer = "transfer"
    return_ = "return"
class FundAction(base):
    __tabelname__ = "fund_action"

    fund_action = Column(Enum(FundActionEnum),nullabel=False)
    fund_amount = Column(Float)
    remark = Column(String,nullabel=True)

# creating table for fund_request
class StatusEnum(str,enum.Enum):
    active = "active" 
    inactive = "inactive"
    delete = "delete"
class FundRequest(Base):
    __tabelname__="fund_request"
    requested_by = Column(Integer,ForeignKey("user.id"),nullable=False)
    deposite_bank_details = Column(Integer,ForeignKey("user.id"),nullable=False)
    reference_detail = Column()  #datatype and constraint not decided yet
    amount = Column(Float)
    remark = Column(String,nullable=True)

