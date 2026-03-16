"""
Database Models
SQLAlchemy ORM models for Service Requests, Contact Messages, Admin Users and Settings
Matches billing software database schema
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
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    full_name = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
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
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(15), nullable=False)
    customer_email = db.Column(db.String(100), nullable=True)
    customer_address = db.Column(db.Text, nullable=False)
    
    # Service Details
    service_type = db.Column(db.String(50), nullable=False)
    ac_type = db.Column(db.String(20), default='Not Specified')
    
    # Preferred Schedule
    preferred_date = db.Column(db.Date, nullable=True)
    time_slot = db.Column(db.String(20), default='Not Specified')
    
    # Additional Info
    message = db.Column(db.Text, nullable=True)
    
    # Request Status
    request_status = db.Column(db.String(20), default='Pending')
    assigned_technician_id = db.Column(db.Integer, nullable=True)
    
    # Source Tracking
    source = db.Column(db.String(50), default='Website')
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    
    # Timestamps
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)

    # Service Details
    service_type = db.Column(db.String(50), nullable=False)
    ac_type = db.Column(db.String(20), default='Not Specified')

    # Additional Info
    message = db.Column(db.Text, nullable=True)

    # Message Status
    status = db.Column(db.String(20), default='unread')

    # Source Tracking
    source = db.Column(db.String(50), default='Website')
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    rating = db.Column(db.Integer, default=5)  # 1-5 stars
    
    # Customer Photo (optional)
    customer_photo = db.Column(db.String(500), nullable=True)
    
    # Display Settings
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
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
    service_name = db.Column(db.String(100), nullable=False)
    service_slug = db.Column(db.String(100), unique=True, nullable=False)  # installation, repair, gas, etc.
    
    # Pricing
    starting_price = db.Column(db.String(50), nullable=False)  # "₹1,499"
    price_numeric = db.Column(db.Integer, nullable=True)  # 1499 (for sorting)
    
    # Service Details
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.String(50), nullable=True)  # "2-3 Hrs"
    icon_class = db.Column(db.String(50), nullable=True)  # FontAwesome class
    
    # Features (JSON array)
    features = db.Column(db.Text, nullable=True)  # '["Free Site Survey", "Pro Setup", "1 Year Warranty"]'
    
    # Display Settings
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Image
    service_image = db.Column(db.String(500), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
    product_type = db.Column(db.String(20), nullable=False)  # 'buy' or 'rent'
    
    # Product Details
    product_name = db.Column(db.String(150), nullable=False)  # "1.5 Ton Split AC"
    brand = db.Column(db.String(50), nullable=True)  # "LG", "Voltas", etc.
    
    # Specifications
    capacity = db.Column(db.String(20), nullable=True)  # "1 Ton", "1.5 Ton", "2 Ton"
    ac_type = db.Column(db.String(20), nullable=True)  # "Split", "Window", "Cassette"
    star_rating = db.Column(db.Integer, default=3)  # 3 or 5 star
    is_inverter = db.Column(db.Boolean, default=False)
    
    # Pricing
    price = db.Column(db.String(50), nullable=False)  # "₹32,999" or "₹1,999/month"
    price_numeric = db.Column(db.Integer, nullable=True)  # 32999 or 1999
    
    # Product Details
    description = db.Column(db.Text, nullable=True)
    features = db.Column(db.Text, nullable=True)  # JSON array of features
    
    # Images
    product_image = db.Column(db.String(500), nullable=True)
    image_gallery = db.Column(db.Text, nullable=True)  # JSON array of image URLs
    
    # Availability
    is_available = db.Column(db.Boolean, default=True)
    stock_status = db.Column(db.String(20), default='In Stock')  # 'In Stock', 'Out of Stock', 'Available on Order'
    
    # For Rental Products
    rental_min_months = db.Column(db.Integer, nullable=True)  # Minimum 3 months
    rental_deposit = db.Column(db.String(50), nullable=True)  # "₹5,000"
    rental_includes = db.Column(db.Text, nullable=True)  # JSON: maintenance, installation, etc.
    
    # Display Settings
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    badge_text = db.Column(db.String(50), nullable=True)  # "Best Seller", "Premium", etc.
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
