from sqlalchemy.orm import Session
from app import models, schemas
from .products import get_product
from .cart import get_cart, clear_cart
from datetime import datetime

def create_order(db: Session, user_id: int):
    cart = get_cart(db, user_id)
    if not cart or not cart.items:
        return None
    
    # Calculate total amount
    total_amount = 0
    order_items = []
    
    for item in cart.items:
        product = get_product(db, item.product_id)
        if product and product.inventory >= item.quantity:
            total_amount += product.price * item.quantity
            order_items.append(
                schemas.OrderItemCreate(
                    product_id=product.id,
                    quantity=item.quantity,
                    price=product.price
                )
            )
            # Reduce inventory
            product.inventory -= item.quantity
    
    if not order_items:
        return None
    
    # Create order
    db_order = models.Order(
        user_id=user_id,
        total_amount=total_amount,
        status="pending"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Add order items
    for item in order_items:
        db_item = models.OrderItem(**item.dict(), order_id=db_order.id)
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    
    # Clear cart
    clear_cart(db, user_id)
    
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Order).filter(models.Order.user_id == user_id).offset(skip).limit(limit).all()

def update_order_status(db: Session, order_id: int, status: str):
    db_order = get_order(db, order_id)
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order