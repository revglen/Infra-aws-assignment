from sqlalchemy.orm import Session
from app import models, schemas
from .orders import get_order, update_order_status
import uuid
from datetime import datetime

def process_payment(db: Session, payment: schemas.PaymentCreate):
    order = get_order(db, payment.order_id)
    if not order:
        return None
    
    # Simulate payment processing
    transaction_id = str(uuid.uuid4())
    payment_status = "completed"  # In real app, this would come from payment gateway
    
    # Create payment record
    db_payment = models.Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        status=payment_status,
        payment_method=payment.payment_method,
        transaction_id=transaction_id
    )
    db.add(db_payment)
    
    # Update order status
    update_order_status(db, order.id, "paid")
    order.payment_id = transaction_id
    
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()