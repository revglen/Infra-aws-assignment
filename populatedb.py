import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Product, User, Cart, CartItem, Order, OrderItem, Payment
from datetime import datetime

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ecommerce"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def populate_data():
    db = SessionLocal()
    
    try:
        create_tables()    
        db = SessionLocal()
        db.query(Payment).delete()
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.query(CartItem).delete()
        db.query(Cart).delete()
        db.query(User).delete()
        db.query(Product).delete()
        db.commit()
        
        # Add products
        products = [
            Product(name="iPhone 13 Pro", description="6.1-inch Super Retina XDR display with ProMotion", price=999.99, inventory=50, category="Electronics"),
            Product(name="MacBook Pro 14\"", description="Apple M1 Pro chip, 16GB RAM, 512GB SSD", price=1999.99, inventory=30, category="Electronics"),
            Product(name="AirPods Pro", description="Active noise cancellation for immersive sound", price=249.99, inventory=100, category="Electronics"),
            Product(name="Nike Air Max 270", description="Iconic Air Max cushioning for all-day comfort", price=150.00, inventory=75, category="Footwear"),
            Product(name="Levi's 501 Original Fit Jeans", description="Classic straight leg jeans", price=59.99, inventory=200, category="Clothing"),
            Product(name="Instant Pot Duo 7-in-1", description="Pressure cooker, slow cooker, rice cooker, and more", price=99.95, inventory=40, category="Home & Kitchen"),
            Product(name="Kindle Paperwhite", description="Waterproof, 8GB, now with adjustable warm light", price=139.99, inventory=60, category="Electronics"),
            Product(name="The Lean Startup by Eric Ries", description="How today's entrepreneurs use continuous innovation", price=14.99, inventory=150, category="Books"),
            Product(name="Bose QuietComfort 45 Headphones", description="World-class noise cancellation", price=329.00, inventory=25, category="Electronics"),
            Product(name="Yeti Rambler 20 oz Tumbler", description="Double-wall vacuum insulation", price=29.99, inventory=120, category="Home & Kitchen"),
            Product(name="Adidas Ultraboost 21 Running Shoes", description="Responsive cushioning for energy return", price=180.00, inventory=45, category="Footwear"),
            Product(name="Sony PlayStation 5", description="Ultra-high speed SSD and 3D audio", price=499.99, inventory=15, category="Electronics"),
            Product(name="Dyson V11 Torque Drive Vacuum", description="Powerful cordless vacuum with LCD screen", price=599.99, inventory=20, category="Home & Kitchen"),
            Product(name="Calvin Klein Cotton T-Shirt", description="Classic crew neck t-shirt", price=24.99, inventory=180, category="Clothing"),
            Product(name="Fitbit Charge 5", description="Advanced health & fitness tracker", price=179.95, inventory=65, category="Electronics")
        ]
        db.add_all(products)
        db.commit()
        
        # Add users
        users = [
            User(email="john.doe@example.com", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", full_name="John Doe", is_active=True),
            User(email="jane.smith@example.com", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", full_name="Jane Smith", is_active=True),
            User(email="mike.johnson@example.com", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", full_name="Mike Johnson", is_active=True),
            User(email="sarah.williams@example.com", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", full_name="Sarah Williams", is_active=True),
            User(email="david.brown@example.com", hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", full_name="David Brown", is_active=True)
        ]
        db.add_all(users)
        db.commit()
        
        # Add carts
        carts = [Cart(user_id=user.id) for user in users]
        db.add_all(carts)
        db.commit()
        
        # Add cart items
        cart_items = [
            CartItem(cart_id=1, product_id=1, quantity=1),
            CartItem(cart_id=1, product_id=3, quantity=2),
            CartItem(cart_id=2, product_id=5, quantity=1),
            CartItem(cart_id=2, product_id=7, quantity=1),
            CartItem(cart_id=3, product_id=12, quantity=1),
            CartItem(cart_id=4, product_id=9, quantity=1),
            CartItem(cart_id=4, product_id=10, quantity=3),
            CartItem(cart_id=5, product_id=2, quantity=1),
            CartItem(cart_id=5, product_id=4, quantity=1)
        ]
        db.add_all(cart_items)
        db.commit()
        
        # Add orders
        orders = [
            Order(user_id=1, total_amount=1499.97, status="completed", payment_id="pay_123456789", created_at=datetime.utcnow()),
            Order(user_id=2, total_amount=154.98, status="completed", payment_id="pay_987654321", created_at=datetime.utcnow()),
            Order(user_id=3, total_amount=499.99, status="processing", payment_id="pay_111222333", created_at=datetime.utcnow()),
            Order(user_id=4, total_amount=419.97, status="shipped", payment_id="pay_444555666", created_at=datetime.utcnow())
        ]
        db.add_all(orders)
        db.commit()
        
        # Add order items
        order_items = [
            OrderItem(order_id=1, product_id=1, quantity=1, price=999.99),
            OrderItem(order_id=1, product_id=3, quantity=2, price=249.99),
            OrderItem(order_id=2, product_id=5, quantity=1, price=59.99),
            OrderItem(order_id=2, product_id=7, quantity=1, price=139.99),
            OrderItem(order_id=3, product_id=12, quantity=1, price=499.99),
            OrderItem(order_id=4, product_id=9, quantity=1, price=329.00),
            OrderItem(order_id=4, product_id=10, quantity=3, price=29.99)
        ]
        db.add_all(order_items)
        db.commit()
        
        # Add payments
        payments = [
            Payment(order_id=1, amount=1499.97, status="completed", payment_method="credit_card", transaction_id="ch_1JXyz72eZvKYlo2C0XKX1", created_at=datetime.utcnow()),
            Payment(order_id=2, amount=154.98, status="completed", payment_method="paypal", transaction_id="PAYID-MJX12345", created_at=datetime.utcnow()),
            Payment(order_id=3, amount=499.99, status="pending", payment_method="credit_card", transaction_id="ch_3JXyz72eZvKYlo2C1XKX1", created_at=datetime.utcnow()),
            Payment(order_id=4, amount=419.97, status="completed", payment_method="apple_pay", transaction_id="ap_1JXyz72eZvKYlo2C2XKX1", created_at=datetime.utcnow())
        ]
        db.add_all(payments)
        db.commit()
        
        print("Database populated successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error populating database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_data()