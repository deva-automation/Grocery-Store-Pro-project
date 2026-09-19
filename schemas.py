from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    unit: str
    stock_quantity: int
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductOut(ProductBase):
    id: int
    class Config:
        from_attributes = True

class CategoryOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

# নতুন: অর্ডার প্লেস করার স্কিমা
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    items: List[OrderItemCreate]

# নতুন: অর্ডারের হিস্টরি দেখার স্কিমা
class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price_at_time: float
    product_name: Optional[str] = None

class OrderOut(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemOut]
    
    class Config:
        from_attributes = True
        