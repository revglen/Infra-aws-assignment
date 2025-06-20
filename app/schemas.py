from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    inventory: int
    category: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    cart_id: int
    
    class Config:
        orm_mode = True

class Cart(BaseModel):
    id: int
    user_id: int
    items: List[CartItem] = []
    
    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    user_id: int
    total_amount: float
    status: str = "pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    payment_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItem] = []
    
    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_method: str

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    status: str
    transaction_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None