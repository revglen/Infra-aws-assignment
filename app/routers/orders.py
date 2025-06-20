from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, services
from app.database import get_db
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.Order)
def create_order(user_id: int, db: Session = Depends(get_db)):
    order = services.create_order(db, user_id=user_id)
    if not order:
        raise HTTPException(status_code=400, detail="Cannot create order with empty cart")
    return order

@router.get("/", response_model=List[schemas.Order])
def get_user_orders(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return services.get_orders(db, user_id=user_id, skip=skip, limit=limit)

@router.get("/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = services.get_order(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order