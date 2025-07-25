import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.transaction import Transaction, BBPSTransaction, TransactionStatus, TransactionType
from app.models.user import User

def create_dmt_transaction(db: Session, transaction_data, current_user):
    if current_user.balance < transaction_data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    transaction = Transaction(
        order_id=str(uuid.uuid4()),
        user_id=current_user.id,
        amount=transaction_data.amount,
        transaction_type=TransactionType.DMT,
        status=TransactionStatus.PENDING,
        beneficiary=transaction_data.beneficiary,
        mobile_no=transaction_data.mobile_no
    )
    
    try:
        # Update user balance
        current_user.balance -= transaction_data.amount
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        # Here you would integrate with actual payment gateway
        # For demo, we'll mark it as success
        transaction.status = TransactionStatus.SUCCESS
        db.commit()
        
        return transaction
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def create_recharge(db: Session, recharge_data, current_user):
    if current_user.balance < recharge_data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    transaction = Transaction(
        order_id=str(uuid.uuid4()),
        user_id=current_user.id,
        amount=recharge_data.amount,
        transaction_type=TransactionType.RECHARGE,
        status=TransactionStatus.PENDING,
        beneficiary=recharge_data.operator,
        mobile_no=recharge_data.mobile_no
    )
    
    try:
        current_user.balance -= recharge_data.amount
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        # Here you would integrate with recharge provider
        # For demo, we'll mark it as success
        transaction.status = TransactionStatus.SUCCESS
        db.commit()
        
        return {
            **transaction.__dict__,
            'operator': recharge_data.operator,
            'circle': recharge_data.circle
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def create_bbps_transaction(db: Session, bill_payment, current_user):
    if current_user.balance < bill_payment.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    transaction = Transaction(
        order_id=str(uuid.uuid4()),
        user_id=current_user.id,
        amount=bill_payment.amount,
        transaction_type=TransactionType.BBPS,
        status=TransactionStatus.PENDING,
        beneficiary=bill_payment.operator_name,
        mobile_no=bill_payment.mobile_no
    )
    
    bbps_transaction = BBPSTransaction(
        client_ref=str(uuid.uuid4()),
        operator_type=bill_payment.operator_type,
        operator_name=bill_payment.operator_name,
        bill_number=bill_payment.bill_number
    )
    
    try:
        current_user.balance -= bill_payment.amount
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        bbps_transaction.transaction_id = transaction.id
        db.add(bbps_transaction)
        db.commit()
        db.refresh(bbps_transaction)
        
        # Here you would integrate with BBPS provider
        # For demo, we'll mark it as success
        transaction.status = TransactionStatus.SUCCESS
        db.commit()
        
        return {
            **transaction.__dict__,
            'operator_type': bbps_transaction.operator_type,
            'operator_name': bbps_transaction.operator_name,
            'bill_number': bbps_transaction.bill_number
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_user_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).offset(skip).limit(limit).all()
