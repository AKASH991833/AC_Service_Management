"""
Data models for the application
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    full_name: str
    email: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class ShopDetails:
    id: int
    shop_name: str
    address: str
    phone: Optional[str]
    email: Optional[str]
    gst_number: Optional[str]
    logo_path: Optional[str]
    owner_name: str
    owner_phone: str
    created_at: datetime

@dataclass
class Customer:
    id: int
    name: str
    mobile: str
    email: Optional[str]
    address: Optional[str]
    landmark: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class ACBrand:
    id: int
    brand_name: str
    is_active: bool
    created_at: datetime

@dataclass
class Service:
    id: int
    service_name: str
    description: Optional[str]
    default_rate: Decimal
    is_active: bool
    created_at: datetime

@dataclass
class Part:
    id: int
    part_name: str
    description: Optional[str]
    default_rate: Decimal
    stock_quantity: int
    is_active: bool
    created_at: datetime

@dataclass
class Technician:
    id: int
    name: str
    mobile: str
    email: Optional[str]
    address: Optional[str]
    commission_rate: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime

@dataclass
class InvoiceItem:
    id: int
    invoice_id: int
    item_type: str  # 'service' or 'part'
    service_id: Optional[int]
    part_id: Optional[int]
    quantity: int
    rate: Decimal
    amount: Decimal

@dataclass
class Invoice:
    id: int
    invoice_number: str
    customer_id: int
    ac_brand_id: Optional[int]
    ac_type: str
    star_rating: Optional[str]
    ton_capacity: Optional[str]
    inverter_type: str
    technician_id: Optional[int]
    subtotal: Decimal
    gst_percentage: Decimal
    gst_amount: Decimal
    total_amount: Decimal
    advance_payment: Decimal
    balance_amount: Decimal
    payment_mode: str
    payment_status: str
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # Related objects
    customer: Optional[Customer] = None
    ac_brand: Optional[ACBrand] = None
    technician: Optional[Technician] = None
    items: List[InvoiceItem] = None

@dataclass
class Payment:
    id: int
    invoice_id: int
    amount: Decimal
    payment_mode: str
    payment_date: datetime
    notes: Optional[str]

@dataclass
class TechnicianWork:
    id: int
    technician_id: int
    invoice_id: int
    work_date: datetime
    service_type: str
    amount_collected: Decimal
    pending_amount: Decimal
    notes: Optional[str]