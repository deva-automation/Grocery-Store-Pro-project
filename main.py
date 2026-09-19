from pathlib import Path
from typing import List
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
import schemas

# ডাটাবেস টেবিল তৈরি
Base.metadata.create_all(bind=engine)

# ==========================================
# 🌟 MASTER FEATURE: Auto-Seeder (ডামি ডেটা ইনসার্ট)
# ==========================================
def seed_dummy_data():
    db = next(get_db())
    try:
        # যদি ডাটাবেস ফাঁকা থাকে, তবেই ডামি ডেটা ঢুকবে
        if db.query(models.Product).count() == 0:
            print("Stocking up the store with dummy products...")
            cat = db.query(models.Category).first()
            if not cat:
                cat = models.Category(name="Daily Groceries")
                db.add(cat)
                db.commit()

            # ইংরেজি ও বাংলা নাম একসাথে ( | ) দিয়ে যুক্ত করা হয়েছে
            dummy_products = [
                {"name": "Miniket Rice|মিনিকেট চাল", "price": 75, "unit": "kg|কেজি", "stock_quantity": 100, "category_id": cat.id},
                {"name": "Sonali Chicken|সোনালী মুরগি", "price": 320, "unit": "kg|কেজি", "stock_quantity": 50, "category_id": cat.id},
                {"name": "Farm Eggs|ফার্মের ডিম", "price": 150, "unit": "dozen|ডজন", "stock_quantity": 30, "category_id": cat.id},
                {"name": "Soybean Oil|সয়াবিন তেল", "price": 165, "unit": "liter|লিটার", "stock_quantity": 80, "category_id": cat.id},
                {"name": "Masoor Dal|মসুর ডাল", "price": 110, "unit": "kg|কেজি", "stock_quantity": 60, "category_id": cat.id},
                {"name": "Potato|আলু", "price": 45, "unit": "kg|কেজি", "stock_quantity": 200, "category_id": cat.id},
                {"name": "Onion|পেঁয়াজ", "price": 80, "unit": "kg|কেজি", "stock_quantity": 150, "category_id": cat.id},
                {"name": "Liquid Milk|তরল দুধ", "price": 90, "unit": "liter|লিটার", "stock_quantity": 40, "category_id": cat.id},
                {"name": "Rui Fish|রুই মাছ", "price": 350, "unit": "kg|কেজি", "stock_quantity": 25, "category_id": cat.id},
                {"name": "Beef|গরুর মাংস", "price": 750, "unit": "kg|কেজি", "stock_quantity": 20, "category_id": cat.id},
                {"name": "Sugar|চিনি", "price": 130, "unit": "kg|কেজি", "stock_quantity": 100, "category_id": cat.id},
                {"name": "Salt|লবণ", "price": 40, "unit": "kg|কেজি", "stock_quantity": 50, "category_id": cat.id},
            ]
            for p in dummy_products:
                db.add(models.Product(**p))
            db.commit()
    except Exception as e:
        print(f"Seeding Error: {e}")
    finally:
        db.close()

# সার্ভার স্টার্ট হওয়ার আগেই সিডিং ফাংশন কল করা হলো
seed_dummy_data()

app = FastAPI(title="FreshMart Pro API", version="5.0.0")

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# --- Views ---
@app.get("/")
async def render_store_home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"title": "FreshMart Home"})

@app.get("/admin")
async def render_admin_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="admin.html", context={"title": "Admin Panel"})

# --- Products API ---
@app.get("/api/products/", response_model=List[schemas.ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.post("/api/products/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    cat = db.query(models.Category).first()
    product.category_id = cat.id if cat else 1
    new_product = models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

# --- Order API ---
@app.post("/api/orders/", response_model=schemas.OrderOut)
def place_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    total = 0
    order_items = []
    
    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product or product.stock_quantity < item.quantity:
            raise HTTPException(status_code=400, detail="পণ্যটি স্টকে নেই!")
        
        product.stock_quantity -= item.quantity
        price = product.price
        total += price * item.quantity
        
        order_items.append(models.OrderItem(product_id=product.id, quantity=item.quantity, price_at_time=price))

    new_order = models.Order(customer_name=order.customer_name, customer_phone=order.customer_phone, total_amount=total, items=order_items)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@app.get("/api/orders/{phone}", response_model=List[schemas.OrderOut])
def get_order_history(phone: str, db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.customer_phone == phone).order_by(models.Order.created_at.desc()).all()
    for order in orders:
        for item in order.items:
            item.product_name = item.product.name
    return orders

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    