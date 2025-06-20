from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, services
from app.database import get_db
from typing import List

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("/", response_model=schemas.Cart)
def get_user_cart(user_id: int, db: Session = Depends(get_db)):
    cart = services.get_cart(db, user_id=user_id)
    if not cart:
        cart = services.create_cart(db, user_id)
    return cart

@router.post("/items/", response_model=schemas.Cart)
def add_item_to_cart(user_id: int, item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    return services.add_to_cart(db, user_id=user_id, item=item)

@router.delete("/items/{product_id}", response_model=schemas.Cart)
def remove_item_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    return services.remove_from_cart(db, user_id=user_id, product_id=product_id)

@router.delete("/clear/", response_model=schemas.Cart)
def clear_user_cart(user_id: int, db: Session = Depends(get_db)):
    return services.clear_cart(db, user_id=user_id)