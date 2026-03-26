"""
Database Migration Script
Adds indexes for performance and creates missing Customer table

Run this script once to optimize your database:
    python migrate_indexes.py

IMPORTANT: This script imports models directly to avoid circular imports
"""

import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables first
load_dotenv()

# Import Flask and SQLAlchemy directly (avoid main.py to prevent circular imports)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# Create minimal Flask app for database operations
app = Flask(__name__)

# Configure database from environment
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/ansh_aircool')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import models after db is initialized
from models import Admin, WebsiteSetting, ServiceRequest, ContactMessage, GalleryImage, Testimonial, Service, Product, WebsiteContent, Customer, AdminActivityLog

with app.app_context():
    print("=" * 70)
    print("DATABASE MIGRATION - Indexes & Customer Table")
    print("=" * 70)
    
    try:
        # Create Customer table if it doesn't exist
        print("\n[1/3] Checking Customer table...")
        db.create_all()
        print("      ✓ Database tables created/verified")
        
        # Add indexes to service_requests table
        print("\n[2/3] Adding indexes to service_requests...")
        indexes_to_add = [
            ("idx_service_request_phone", "service_requests", "customer_phone"),
            ("idx_service_request_email", "service_requests", "customer_email"),
            ("idx_service_request_type", "service_requests", "service_type"),
            ("idx_service_request_status", "service_requests", "request_status"),
            ("idx_service_request_active", "service_requests", "is_active"),
            ("idx_service_request_created", "service_requests", "created_at"),
        ]
        
        for idx_name, table, column in indexes_to_add:
            try:
                db.session.execute(text(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})"))
                print(f"      ✓ Index {idx_name} added")
            except Exception as e:
                print(f"      ⚠ Index {idx_name} may already exist: {str(e)[:50]}")
        
        db.session.commit()
        
        # Add indexes to contact_messages table
        print("\n[3/3] Adding indexes to contact_messages...")
        indexes_to_add = [
            ("idx_contact_phone", "contact_messages", "phone"),
            ("idx_contact_email", "contact_messages", "email"),
            ("idx_contact_service_type", "contact_messages", "service_type"),
            ("idx_contact_status", "contact_messages", "status"),
            ("idx_contact_created", "contact_messages", "created_at"),
        ]
        
        for idx_name, table, column in indexes_to_add:
            try:
                db.session.execute(text(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})"))
                print(f"      ✓ Index {idx_name} added")
            except Exception as e:
                print(f"      ⚠ Index {idx_name} may already exist: {str(e)[:50]}")
        
        db.session.commit()
        
        # Add indexes to testimonials table
        print("\n[4/4] Adding indexes to testimonials...")
        indexes_to_add = [
            ("idx_testimonial_rating", "testimonials", "rating"),
            ("idx_testimonial_active", "testimonials", "is_active"),
            ("idx_testimonial_featured", "testimonials", "is_featured"),
            ("idx_testimonial_created", "testimonials", "created_at"),
        ]
        
        for idx_name, table, column in indexes_to_add:
            try:
                db.session.execute(text(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})"))
                print(f"      ✓ Index {idx_name} added")
            except Exception as e:
                print(f"      ⚠ Index {idx_name} may already exist: {str(e)[:50]}")
        
        db.session.commit()
        
        # Add indexes to services table
        print("\n[5/5] Adding indexes to services...")
        indexes_to_add = [
            ("idx_service_slug", "services", "service_slug"),
            ("idx_service_price", "services", "price_numeric"),
            ("idx_service_active", "services", "is_active"),
            ("idx_service_featured", "services", "is_featured"),
            ("idx_service_created", "services", "created_at"),
        ]
        
        for idx_name, table, column in indexes_to_add:
            try:
                db.session.execute(text(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})"))
                print(f"      ✓ Index {idx_name} added")
            except Exception as e:
                print(f"      ⚠ Index {idx_name} may already exist: {str(e)[:50]}")
        
        db.session.commit()
        
        # Add indexes to products table
        print("\n[6/6] Adding indexes to products...")
        indexes_to_add = [
            ("idx_product_type", "products", "product_type"),
            ("idx_product_active", "products", "is_active"),
            ("idx_product_featured", "products", "is_featured"),
            ("idx_product_price", "products", "price_numeric"),
        ]
        
        for idx_name, table, column in indexes_to_add:
            try:
                db.session.execute(text(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table}({column})"))
                print(f"      ✓ Index {idx_name} added")
            except Exception as e:
                print(f"      ⚠ Index {idx_name} may already exist: {str(e)[:50]}")
        
        db.session.commit()
        
        # Add indexes to customers table
        print("\n[7/7] Adding indexes to customers...")
        try:
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_customer_phone ON customers(phone)"))
            print("      ✓ Index idx_customer_phone added")
        except Exception as e:
            print(f"      ⚠ Index may already exist: {str(e)[:50]}")
        
        db.session.commit()
        
        print("\n" + "=" * 70)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nDatabase is now optimized with indexes for faster queries.")
        print("\nNext steps:")
        print("  1. Restart the Flask backend")
        print("  2. Test the website and admin panel")
        print("  3. Monitor query performance")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ MIGRATION FAILED: {str(e)}")
        print("\nTroubleshooting:")
        print("  1. Check MySQL is running")
        print("  2. Verify database credentials in .env")
        print("  3. Ensure database exists")
        import traceback
        traceback.print_exc()
