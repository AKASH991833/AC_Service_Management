"""
Database Migration - Add New Tables
Creates tables for Testimonials, Services, and Products management
"""

from models import db

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
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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
# WEBSITE SETTINGS (Enhanced)
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
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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
# CREATE TABLES FUNCTION
# ========================================

def create_new_tables():
    """Create all new tables"""
    try:
        # Create tables
        db.create_all()
        
        print("✅ Tables created successfully!")
        print("   - testimonials")
        print("   - services")
        print("   - products")
        print("   - website_content")
        
        # Insert default services
        insert_default_services()
        
        # Insert default stats
        insert_default_stats()
        
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False


def insert_default_services():
    """Insert default AC services"""
    default_services = [
        {
            'service_name': 'AC Installation',
            'service_slug': 'installation',
            'starting_price': '₹1,499',
            'price_numeric': 1499,
            'description': 'Professional AC installation service with warranty',
            'duration': '2-3 Hrs',
            'icon_class': 'fas fa-tools',
            'features': '["Free Site Survey", "Professional Setup", "1 Year Warranty", "Testing & Demo"]',
            'is_active': True,
            'display_order': 1
        },
        {
            'service_name': 'AC Repair',
            'service_slug': 'repair',
            'starting_price': '₹499',
            'price_numeric': 499,
            'description': 'Quick AC repair for all brands and models',
            'duration': '1-2 Hrs',
            'icon_class': 'fas fa-wrench',
            'features': '["Quick Diagnosis", "Same Day Service", "90 Days Warranty", "Genuine Parts"]',
            'is_active': True,
            'display_order': 2
        },
        {
            'service_name': 'Gas Refill',
            'service_slug': 'gas',
            'starting_price': '₹2,499',
            'price_numeric': 2499,
            'description': 'AC gas refill with leak detection',
            'duration': '1-2 Hrs',
            'icon_class': 'fas fa-fill-drip',
            'features': '["Leak Detection", "Eco-Friendly Gas", "Pressure Check", "90 Days Warranty"]',
            'is_active': True,
            'display_order': 3
        },
        {
            'service_name': 'AMC Plans',
            'service_slug': 'amc',
            'starting_price': '₹2,999',
            'price_numeric': 2999,
            'description': 'Annual maintenance contract with regular servicing',
            'duration': 'Yearly',
            'icon_class': 'fas fa-clipboard-check',
            'features': '["4 Visits Per Year", "Priority Support", "10% Discount', 'Free Cleaning"]',
            'is_active': True,
            'display_order': 4
        },
        {
            'service_name': 'PCB Repair',
            'service_slug': 'pcb',
            'starting_price': '₹1,999',
            'price_numeric': 1999,
            'description': 'Advanced PCB repair and replacement',
            'duration': '2-4 Hrs',
            'icon_class': 'fas fa-microchip',
            'features': '["Chip Level Repair', 'Replacement Available', '90 Days Warranty"]',
            'is_active': True,
            'display_order': 5
        },
        {
            'service_name': 'Deep Cleaning',
            'service_slug': 'cleaning',
            'starting_price': '₹999',
            'price_numeric': 999,
            'description': 'Complete AC deep cleaning and sanitization',
            'duration': '1-2 Hrs',
            'icon_class': 'fas fa-spray-can',
            'features': '["Chemical Wash', 'Bacteria Removal', 'Better Air Quality', 'Fresh Smell"]',
            'is_active': True,
            'display_order': 6
        }
    ]
    
    for service_data in default_services:
        existing = Service.query.filter_by(service_slug=service_data['service_slug']).first()
        if not existing:
            service = Service(**service_data)
            db.session.add(service)
    
    try:
        db.session.commit()
        print("✅ Default services inserted!")
    except Exception as e:
        db.session.rollback()
        print(f"⚠️ Services may already exist: {str(e)}")


def insert_default_stats():
    """Insert default website stats"""
    default_stats = [
        {'section_name': 'stats', 'content_key': 'stat_customers', 'content_value': '1000+', 'content_type': 'text'},
        {'section_name': 'stats', 'content_key': 'stat_reviews', 'content_value': '500+', 'content_type': 'text'},
        {'section_name': 'stats', 'content_key': 'stat_experience', 'content_value': '15+', 'content_type': 'text'},
        {'section_name': 'stats', 'content_key': 'stat_cities', 'content_value': '50+', 'content_type': 'text'},
    ]
    
    for stat_data in default_stats:
        existing = WebsiteContent.query.filter_by(
            section_name=stat_data['section_name'],
            content_key=stat_data['content_key']
        ).first()
        
        if not existing:
            stat = WebsiteContent(**stat_data)
            db.session.add(stat)
    
    try:
        db.session.commit()
        print("✅ Default stats inserted!")
    except Exception as e:
        db.session.rollback()


if __name__ == '__main__':
    import sys
    import os
    
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from main import create_app
    
    app = create_app()
    
    with app.app_context():
        print("🔧 Creating new database tables...")
        create_new_tables()
        print("\n✅ Migration completed!")
