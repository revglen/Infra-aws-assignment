from sqlalchemy.orm import Session
from app import models, schemas

def get_cart(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).first()

def create_cart(db: Session, user_id: int):
    db_cart = models.Cart(user_id=user_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def add_to_cart(db: Session, user_id: int, item: schemas.CartItemCreate):
    cart = get_cart(db, user_id)
    if not cart:
        cart = create_cart(db, user_id)
    
    # Check if product already in cart
    existing_item = next((i for i in cart.items if i.product_id == item.product_id), None)
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        new_item = models.CartItem(**item.dict(), cart_id=cart.id)
        db.add(new_item)
    
    db.commit()
    return cart

def remove_from_cart(db: Session, user_id: int, product_id: int):
    cart = get_cart(db, user_id)
    if cart:
        item_to_remove = next((i for i in cart.items if i.product_id == product_id), None)
        if item_to_remove:
            db.delete(item_to_remove)
            db.commit()
    return cart

def clear_cart(db: Session, user_id: int):
    cart = get_cart(db, user_id)
    if cart:
        for item in cart.items:
            db.delete(item)
        db.commit()
    return cart