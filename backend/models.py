"""
Database Models - Production Ready
SQLAlchemy ORM models with soft delete, proper constraints, and indexes
Single Database Schema: ac_service_billing
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import json

db = SQLAlchemy()


class Admin(db.Model):
    """Model for admin users"""
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    full_name = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

    def __repr__(self):
        return f'<Admin {self.username}>'


class WebsiteSetting(db.Model):
    """Model for website settings"""
    __tablename__ = 'website_settings'

    id = db.Column(db.Integer, primary_key=True)
    setting_key = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(db.Text, nullable=True)
    setting_type = db.Column(db.String(20), default='text')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'setting_key': self.setting_key,
            'setting_value': self.setting_value,
            'setting_type': self.setting_type,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<WebsiteSetting {self.setting_key}>'


class ServiceRequest(db.Model):
    """Model for service request submissions"""
    __tablename__ = 'service_requests'

    id = db.Column(db.Integer, primary_key=True)

    # Customer Details
    customer_name = db.Column(db.String(100), nullable=False, index=True)
    customer_phone = db.Column(db.String(15), nullable=False, index=True)
    customer_email = db.Column(db.String(100), nullable=True, index=True)
    customer_address = db.Column(db.Text, nullable=False)

    # Service Details
    service_type = db.Column(db.String(50), nullable=False, index=True)
    ac_type = db.Column(db.String(20), default='Not Specified')

    # Preferred Schedule
    preferred_date = db.Column(db.Date, nullable=True)
    time_slot = db.Column(db.String(20), default='Not Specified')

    # Additional Info
    message = db.Column(db.Text, nullable=True)

    # Request Status
    request_status = db.Column(db.String(20), default='Pending', index=True)
    assigned_technician_id = db.Column(db.Integer, nullable=True)

    # Source Tracking
    source = db.Column(db.String(50), default='Website')
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)

    # Soft Delete Support
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Timestamps
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.customer_name,
            'phone': self.customer_phone,
            'email': self.customer_email,
            'address': self.customer_address,
            'service_type': self.service_type,
            'ac_type': self.ac_type,
            'preferred_date': self.preferred_date.isoformat() if self.preferred_date else None,
            'time_slot': self.time_slot,
            'message': self.message,
            'status': self.request_status,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<ServiceRequest {self.id} - {self.customer_name}>'


class ContactMessage(db.Model):
    """Model for contact form submissions"""
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)

    # Customer Details
    name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(15), nullable=False, index=True)
    email = db.Column(db.String(100), nullable=True, index=True)
    address = db.Column(db.Text, nullable=True)

    # Service Details
    service_type = db.Column(db.String(50), nullable=False, index=True)
    ac_type = db.Column(db.String(20), default='Not Specified')

    # Additional Info
    message = db.Column(db.Text, nullable=True)

    # Message Status
    status = db.Column(db.String(20), default='unread', index=True)

    # Source Tracking
    source = db.Column(db.String(50), default='Website')
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)

    # Soft Delete Support
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'service_type': self.service_type,
            'ac_type': self.ac_type,
            'message': self.message,
            'status': self.status,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<ContactMessage {self.id} - {self.name}>'


class GalleryImage(db.Model):
    """Model for gallery images"""
    __tablename__ = 'gallery_images'

    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False, default='gallery')
    alt_text = db.Column(db.String(200), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)
    mime_type = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'image_path': self.image_path,
            'image_url': self.image_url,
            'category': self.category,
            'alt_text': self.alt_text,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<GalleryImage {self.id} - {self.category}>'


# ========================================
# TESTIMONIALS TABLE
# ========================================

class Testimonial(db.Model):
    """Model for customer testimonials"""
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key=True)

    # Customer Details
    customer_name = db.Column(db.String(100), nullable=False)
    customer_location = db.Column(db.String(100), nullable=True)

    # Testimonial Content
    review_text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5, index=True)  # 1-5 stars

    # Customer Photo (optional)
    customer_photo = db.Column(db.String(500), nullable=True)

    # Display Settings
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    display_order = db.Column(db.Integer, default=0)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_location': self.customer_location,
            'review_text': self.review_text,
            'rating': self.rating,
            'customer_photo': self.customer_photo,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Testimonial {self.id} - {self.customer_name}>'


# ========================================
# SERVICES TABLE
# ========================================

class Service(db.Model):
    """Model for AC services"""
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)

    # Service Details
    service_name = db.Column(db.String(100), nullable=False, index=True)
    service_slug = db.Column(db.String(100), unique=True, nullable=False, index=True)

    # Pricing
    starting_price = db.Column(db.String(50), nullable=False)
    price_numeric = db.Column(db.Integer, nullable=True, index=True)

    # Service Details
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    icon_class = db.Column(db.String(50), nullable=True)

    # Features (JSON array)
    features = db.Column(db.Text, nullable=True)

    # Display Settings
    is_active = db.Column(db.Boolean, default=True, index=True)
    display_order = db.Column(db.Integer, default=0, index=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)

    # Image
    service_image = db.Column(db.String(500), nullable=True)

    # Soft Delete Support
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def to_dict(self):
        """Convert to dictionary"""
        import json
        return {
            'id': self.id,
            'service_name': self.service_name,
            'service_slug': self.service_slug,
            'starting_price': self.starting_price,
            'price_numeric': self.price_numeric,
            'description': self.description,
            'duration': self.duration,
            'icon_class': self.icon_class,
            'features': json.loads(self.features) if self.features else [],
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'display_order': self.display_order,
            'service_image': self.service_image,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Service {self.service_name}>'


# ========================================
# PRODUCTS TABLE (AC Sale & Rent Only)
# ========================================

class Product(db.Model):
    """Model for AC products (Sale & Rent)"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)

    # Product Type
    product_type = db.Column(db.String(20), nullable=False, index=True)

    # Product Details
    product_name = db.Column(db.String(150), nullable=False, index=True)
    brand = db.Column(db.String(50), nullable=True, index=True)

    # Specifications
    capacity = db.Column(db.String(20), nullable=True)
    ac_type = db.Column(db.String(20), nullable=True)
    star_rating = db.Column(db.Integer, default=3)
    is_inverter = db.Column(db.Boolean, default=False)

    # Pricing
    price = db.Column(db.String(50), nullable=False)
    price_numeric = db.Column(db.Integer, nullable=True, index=True)

    # Product Details
    description = db.Column(db.Text, nullable=True)
    features = db.Column(db.Text, nullable=True)

    # Images
    product_image = db.Column(db.String(500), nullable=True)
    image_gallery = db.Column(db.Text, nullable=True)

    # Availability
    is_available = db.Column(db.Boolean, default=True, index=True)
    stock_status = db.Column(db.String(20), default='In Stock')

    # For Rental Products
    rental_min_months = db.Column(db.Integer, nullable=True)
    rental_deposit = db.Column(db.String(50), nullable=True)
    rental_includes = db.Column(db.Text, nullable=True)

    # Display Settings
    is_active = db.Column(db.Boolean, default=True, index=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    display_order = db.Column(db.Integer, default=0)
    badge_text = db.Column(db.String(50), nullable=True)

    # Soft Delete Support
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def to_dict(self):
        """Convert to dictionary"""
        import json
        return {
            'id': self.id,
            'product_type': self.product_type,
            'product_name': self.product_name,
            'brand': self.brand,
            'capacity': self.capacity,
            'ac_type': self.ac_type,
            'star_rating': self.star_rating,
            'is_inverter': self.is_inverter,
            'price': self.price,
            'price_numeric': self.price_numeric,
            'description': self.description,
            'features': json.loads(self.features) if self.features else [],
            'product_image': self.product_image,
            'image_gallery': json.loads(self.image_gallery) if self.image_gallery else [],
            'is_available': self.is_available,
            'stock_status': self.stock_status,
            'rental_min_months': self.rental_min_months,
            'rental_deposit': self.rental_deposit,
            'rental_includes': json.loads(self.rental_includes) if self.rental_includes else [],
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'display_order': self.display_order,
            'badge_text': self.badge_text,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Product {self.product_type} - {self.product_name}>'


# ========================================
# WEBSITE CONTENT TABLE
# ========================================

class WebsiteContent(db.Model):
    """Model for editable website content"""
    __tablename__ = 'website_content'

    id = db.Column(db.Integer, primary_key=True)
    
    # Content Section
    section_name = db.Column(db.String(50), nullable=False)  # 'hero', 'stats', 'features', 'footer'
    content_key = db.Column(db.String(100), nullable=False)  # 'hero_title', 'stat_customers', etc.
    content_value = db.Column(db.Text, nullable=False)
    content_type = db.Column(db.String(20), default='text')  # 'text', 'number', 'image', 'json'
    
    # Display Settings
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    
    # Timestamps
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'section_name': self.section_name,
            'content_key': self.content_key,
            'content_value': self.content_value,
            'content_type': self.content_type,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<WebsiteContent {self.section_name}.{self.content_key}>'


# ========================================
# CUSTOMER TABLE (For Customer Management)
# ========================================

class Customer(db.Model):
    """Model for customer database (CRM)"""
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)

    # Customer Details
    name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(15), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), nullable=True, index=True)
    customer_type = db.Column(db.String(50), default='Regular', index=True)

    # Address
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)

    # Additional Info
    notes = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, index=True)

    # Soft Delete Support
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'customer_type': self.customer_type,
            'address': self.address,
            'city': self.city,
            'pincode': self.pincode,
            'notes': self.notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Customer {self.name} - {self.phone}>'


# ========================================
# ADMIN ACTIVITY LOG TABLE
# ========================================

class AdminActivityLog(db.Model):
    """Model for tracking admin activities and actions"""
    __tablename__ = 'admin_activity_logs'

    id = db.Column(db.Integer, primary_key=True)

    # Admin Details
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=True)
    admin_username = db.Column(db.String(50), index=True)

    # Action Details
    action_type = db.Column(db.String(50), nullable=False, index=True)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    action_category = db.Column(db.String(50), index=True)  # content, product, service, testimonial, etc.
    target_type = db.Column(db.String(50))  # What was modified (e.g., 'Product', 'Service')
    target_id = db.Column(db.Integer)  # ID of modified item

    # Details
    description = db.Column(db.Text, nullable=False)
    changes = db.Column(db.Text)  # JSON of what changed
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))

    # Status
    status = db.Column(db.String(20), default='success')  # success, failed, error
    error_message = db.Column(db.Text, nullable=True)

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        """Convert to dictionary"""
        import json
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'admin_username': self.admin_username,
            'action_type': self.action_type,
            'action_category': self.action_category,
            'target_type': self.target_type,
            'target_id': self.target_id,
            'description': self.description,
            'changes': json.loads(self.changes) if self.changes else None,
            'ip_address': self.ip_address,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<AdminActivityLog {self.action_type} by {self.admin_username}>'


# ============================================================================
# INVOICE MANAGEMENT MODELS (For Desktop Software Integration)
# ============================================================================

class Invoice(db.Model):
    """
    Model for invoices - Shared between backend and desktop software
    Status: draft -> final -> paid (LOCKED) or cancelled (LOCKED)
    
    INVOICE LOCKING RULES:
    - 'draft': Can be edited and deleted
    - 'final': Can be edited (not yet paid), cannot delete
    - 'paid': LOCKED - Read-only, cannot edit or delete
    - 'cancelled': LOCKED - Read-only, cannot edit
    """
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)

    # Invoice Number - UNIQUE
    invoice_number = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Customer Link - Foreign Key with RESTRICT (can't delete customer with invoices)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='RESTRICT'), nullable=False, index=True)

    # Invoice Dates
    invoice_date = db.Column(db.Date, nullable=False, index=True)
    due_date = db.Column(db.Date, nullable=True)

    # AC Details
    ac_brand = db.Column(db.String(100), nullable=True)
    ac_type = db.Column(db.String(20), nullable=True)
    ac_model = db.Column(db.String(100), nullable=True)

    # Financial Details
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), default=0)
    tax_percentage = db.Column(db.Numeric(5, 2), default=18)
    tax_amount = db.Column(db.Numeric(10, 2), default=0)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)

    # Payment Details
    paid_amount = db.Column(db.Numeric(10, 2), default=0, index=True)
    balance_amount = db.Column(db.Numeric(10, 2), nullable=False, index=True)

    # Invoice Status: draft, final, paid, cancelled
    # ENUM type enforced at database level
    status = db.Column(db.Enum('draft', 'final', 'paid', 'cancelled', name='invoice_status'), 
                      default='draft', index=True, nullable=False)

    # Payment Mode
    payment_mode = db.Column(db.String(20), nullable=True)

    # Notes
    notes = db.Column(db.Text, nullable=True)

    # Created By (User ID from desktop software)
    created_by = db.Column(db.Integer, nullable=True)

    # Soft Delete Support
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # Relationships
    customer = db.relationship('Customer', backref=db.backref('invoices', lazy='select'), lazy='joined')
    items = db.relationship('InvoiceItem', backref='invoice', lazy='select', cascade='all, delete-orphan')

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else None,
            'invoice_date': self.invoice_date.isoformat() if self.invoice_date else None,
            'ac_brand': self.ac_brand,
            'ac_type': self.ac_type,
            'subtotal': float(self.subtotal) if self.subtotal else 0,
            'discount': float(self.discount) if self.discount else 0,
            'tax_percentage': float(self.tax_percentage) if self.tax_percentage else 18,
            'tax_amount': float(self.tax_amount) if self.tax_amount else 0,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'paid_amount': float(self.paid_amount) if self.paid_amount else 0,
            'balance_amount': float(self.balance_amount) if self.balance_amount else 0,
            'status': self.status,
            'payment_mode': self.payment_mode,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'items': [item.to_dict() for item in self.items]
        }

    def __repr__(self):
        return f'<Invoice {self.invoice_number} - {self.status}>'

    @property
    def is_locked(self):
        """Check if invoice is locked (paid or cancelled)"""
        return self.status in ['paid', 'cancelled']


class InvoiceItem(db.Model):
    """Model for invoice line items"""
    __tablename__ = 'invoice_items'

    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False, index=True)

    # Item Type: service or part
    item_type = db.Column(db.String(20), nullable=False, index=True)

    # Item Details
    service_id = db.Column(db.Integer, nullable=True)
    part_id = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(500), nullable=False)

    # Pricing
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'item_type': self.item_type,
            'service_id': self.service_id,
            'part_id': self.part_id,
            'description': self.description,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'total_price': float(self.total_price) if self.total_price else 0
        }

    def __repr__(self):
        return f'<InvoiceItem {self.description}>'


class Technician(db.Model):
    """Model for technicians"""
    __tablename__ = 'technicians'

    id = db.Column(db.Integer, primary_key=True)

    # Personal Details
    name = db.Column(db.String(100), nullable=False, index=True)
    phone = db.Column(db.String(15), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)

    # Professional Details
    specialization = db.Column(db.String(100), nullable=True)
    commission_rate = db.Column(db.Numeric(5, 2), default=10)
    is_active = db.Column(db.Boolean, default=True, index=True)
    joined_date = db.Column(db.Date, nullable=True)

    # Soft Delete Support
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'specialization': self.specialization,
            'is_active': self.is_active,
            'joined_date': self.joined_date.isoformat() if self.joined_date else None
        }

    def __repr__(self):
        return f'<Technician {self.name}>'


class AMCContract(db.Model):
    """Model for Annual Maintenance Contracts"""
    __tablename__ = 'amc_contracts'

    id = db.Column(db.Integer, primary_key=True)

    # Contract Number - UNIQUE
    contract_number = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Customer Link
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False, index=True)

    # Contract Period
    start_date = db.Column(db.Date, nullable=False, index=True)
    end_date = db.Column(db.Date, nullable=False, index=True)

    # Financial Details
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    paid_amount = db.Column(db.Numeric(10, 2), default=0)
    payment_frequency = db.Column(db.String(20), default='yearly')

    # Contract Status
    status = db.Column(db.String(20), default='active', index=True)

    # Notes
    notes = db.Column(db.Text, nullable=True)

    # Soft Delete Support
    is_deleted = db.Column(db.Boolean, default=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # Relationships
    customer = db.relationship('Customer', backref='amc_contracts')
    units = db.relationship('AMCUnit', backref='contract', cascade='all, delete-orphan')

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'contract_number': self.contract_number,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'status': self.status,
            'units': [unit.to_dict() for unit in self.units]
        }

    def __repr__(self):
        return f'<AMCContract {self.contract_number}>'


class AMCUnit(db.Model):
    """Model for AC units under AMC contract"""
    __tablename__ = 'amc_units'

    id = db.Column(db.Integer, primary_key=True)

    # Foreign Key
    contract_id = db.Column(db.Integer, db.ForeignKey('amc_contracts.id'), nullable=False, index=True)

    # AC Details
    ac_brand = db.Column(db.String(100), nullable=False)
    ac_type = db.Column(db.String(20), nullable=True)
    ac_model = db.Column(db.String(100), nullable=True)
    serial_number = db.Column(db.String(100), nullable=True)
    capacity_tonnage = db.Column(db.String(10), nullable=True)
    installation_year = db.Column(db.Integer, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'contract_id': self.contract_id,
            'ac_brand': self.ac_brand,
            'ac_type': self.ac_type,
            'ac_model': self.ac_model,
            'serial_number': self.serial_number,
            'capacity_tonnage': self.capacity_tonnage
        }

    def __repr__(self):
        return f'<AMCUnit {self.ac_brand} {self.ac_type}>'
