from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, services
from app.database import get_db

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=schemas.Payment)
def process_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    order = services.get_order(db, payment.order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Order already processed")
    if payment.amount != order.total_amount:
        raise HTTPException(status_code=400, detail="Payment amount doesn't match order total")
    
    return services.process_payment(db, payment=payment)

@router.get("/{payment_id}", response_model=schemas.Payment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = services.get_payment(db, payment_id=payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment