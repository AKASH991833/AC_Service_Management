"""
Production Database Initialization Script
Creates unified schema for ac_service_billing database
Includes: Tables, Indexes, Default Admin, Sample Data

Usage:
    python init_production_db.py
"""

from main import create_app
from models import db, Admin, Customer, Invoice, InvoiceItem, Technician, AMCContract, AMCUnit
from models import Service, Product, ServiceRequest, ContactMessage, Testimonial, GalleryImage
from models import WebsiteContent, WebsiteSetting, AdminActivityLog
from sqlalchemy import text
import sys
import os

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = create_app()


def create_tables():
    """Create all database tables"""
    print("\n[1/5] Creating database tables...")
    db.create_all()
    
    # Verify tables
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"      ✅ Created {len(tables)} tables:")
    for table in sorted(tables):
        print(f"         • {table}")
    return tables


def create_admin_user():
    """Create default admin user"""
    print("\n[2/5] Setting up admin user...")
    
    admin = Admin.query.filter_by(username='admin').first()
    
    if not admin:
        admin = Admin(
            username='admin',
            full_name='Admin User',
            email='admin@anshaircool.com',
            is_active=True
        )
        admin.set_password('Admin@123')
        db.session.add(admin)
        db.session.commit()
        
        print("      ✅ Default admin created!")
        print("         Username: admin")
        print("         Password: Admin@123")
        print("         ⚠️  CHANGE THIS IMMEDIATELY!")
    else:
        print("      ℹ️  Admin user already exists")
    
    return admin


def create_default_services():
    """Create default AC services"""
    print("\n[3/5] Setting up default services...")
    
    default_services = [
        {
            'service_slug': 'installation',
            'service_name': 'AC Installation',
            'description': 'Professional installation of new AC units with all necessary accessories',
            'starting_price': '₹500',
            'price_numeric': 500,
            'duration': '2-3 Hrs',
            'icon_class': 'fa-solid fa-screwdriver-wrench',
            'features': '["Free Site Survey", "Professional Installation", "Testing & Commissioning", "1 Year Service Warranty"]',
            'is_featured': True,
            'display_order': 1
        },
        {
            'service_slug': 'repair',
            'service_name': 'AC Repair & Service',
            'description': 'Expert repair for all AC brands and models with genuine parts',
            'starting_price': '₹300',
            'price_numeric': 300,
            'duration': '1-2 Hrs',
            'icon_class': 'fa-solid fa-tools',
            'features': '["Diagnosis & Testing", "Genuine Spare Parts", "Expert Technicians", "90 Days Warranty"]',
            'is_featured': True,
            'display_order': 2
        },
        {
            'service_slug': 'gas_refill',
            'service_name': 'AC Gas Refill',
            'description': 'Complete gas refill with quality checked refrigerant (R32/R410A/R22)',
            'starting_price': '₹800',
            'price_numeric': 800,
            'duration': '1-2 Hrs',
            'icon_class': 'fa-solid fa-wind',
            'features': '["Pressure Check", "Leak Testing", "Quality Refrigerant", "Performance Testing"]',
            'is_featured': True,
            'display_order': 3
        },
        {
            'service_slug': 'cleaning',
            'service_name': 'AC Deep Cleaning',
            'description': 'Comprehensive cleaning service for better cooling and health',
            'starting_price': '₹400',
            'price_numeric': 400,
            'duration': '1-2 Hrs',
            'icon_class': 'fa-solid fa-sparkles',
            'features': '["Jet Pump Cleaning", "Anti-bacterial Treatment", "Improved Air Quality", "Better Cooling"]',
            'is_featured': True,
            'display_order': 4
        },
        {
            'service_slug': 'amc',
            'service_name': 'AMC (Annual Maintenance)',
            'description': 'Yearly maintenance contract for hassle-free AC operation',
            'starting_price': '₹2,000',
            'price_numeric': 2000,
            'duration': '1 Year',
            'icon_class': 'fa-solid fa-file-contract',
            'features': '["4 Scheduled Services", "Priority Support", "10% Discount on Repairs", "Free Gas Top-up"]',
            'is_featured': True,
            'display_order': 5
        },
        {
            'service_slug': 'pcb_repair',
            'service_name': 'PCB Repair & Replacement',
            'description': 'Expert PCB repair and replacement for all AC brands',
            'starting_price': '₹500',
            'price_numeric': 500,
            'duration': '2-4 Hrs',
            'icon_class': 'fa-solid fa-microchip',
            'features': '["PCB Diagnosis", "Component Level Repair", "Testing & Programming", "90 Days Warranty"]',
            'is_featured': False,
            'display_order': 6
        }
    ]
    
    service_count = 0
    for service_data in default_services:
        existing = Service.query.filter_by(service_slug=service_data['service_slug']).first()
        
        if not existing:
            service = Service(**service_data)
            db.session.add(service)
            service_count += 1
    
    db.session.commit()
    print(f"      ✅ Created/Updated {service_count} services")
    return service_count


def create_default_products():
    """Create default AC products"""
    print("\n[4/5] Setting up default products...")
    
    default_products = [
        {
            'product_type': 'buy',
            'product_name': '1.5 Ton 5-Star Inverter Split AC',
            'brand': 'LG',
            'capacity': '1.5 Ton',
            'ac_type': 'Split',
            'star_rating': 5,
            'is_inverter': True,
            'price': '₹42,999',
            'price_numeric': 42999,
            'description': 'Energy efficient inverter AC with dual cooling technology',
            'features': '["5 Star Energy Rating", "Inverter Compressor", "Dual Cooling", "Anti-Virus Protection", "10 Year Warranty"]',
            'is_available': True,
            'stock_status': 'In Stock',
            'is_featured': True,
            'display_order': 1,
            'badge_text': 'Best Seller'
        },
        {
            'product_type': 'buy',
            'product_name': '1 Ton 3-Star Inverter Window AC',
            'brand': 'Voltas',
            'capacity': '1 Ton',
            'ac_type': 'Window',
            'star_rating': 3,
            'is_inverter': True,
            'price': '₹28,999',
            'price_numeric': 28999,
            'description': 'Compact and efficient window AC for small rooms',
            'features': '["3 Star Rating", "Inverter Technology", "Turbo Cooling", "Anti-Dust Filter", "5 Year Warranty"]',
            'is_available': True,
            'stock_status': 'In Stock',
            'is_featured': False,
            'display_order': 2
        },
        {
            'product_type': 'rent',
            'product_name': '1.5 Ton Split AC Rental',
            'brand': 'Various',
            'capacity': '1.5 Ton',
            'ac_type': 'Split',
            'star_rating': 3,
            'is_inverter': False,
            'price': '₹1,500/month',
            'price_numeric': 1500,
            'description': 'Rental AC for temporary requirements (min 3 months)',
            'features': '["Free Installation", "Maintenance Included", "24/7 Support", "Flexible Tenure"]',
            'is_available': True,
            'stock_status': 'Available',
            'rental_min_months': 3,
            'rental_deposit': '₹5,000',
            'rental_includes': '["Installation", "Maintenance", "Repairs", "Gas Refill"]',
            'is_featured': True,
            'display_order': 3,
            'badge_text': 'Popular'
        }
    ]
    
    product_count = 0
    for product_data in default_products:
        existing = Product.query.filter_by(
            product_name=product_data['product_name'],
            product_type=product_data['product_type']
        ).first()
        
        if not existing:
            product = Product(**product_data)
            db.session.add(product)
            product_count += 1
    
    db.session.commit()
    print(f"      ✅ Created/Updated {product_count} products")
    return product_count


def create_website_content():
    """Create default website content"""
    print("\n[5/5] Setting up website content...")
    
    default_content = [
        # Hero Section
        ('hero', 'title', 'text', 'Professional AC Service & Installation at Your Doorstep'),
        ('hero', 'subtitle', 'text', 'Certified Technicians | Same Day Service | Trusted by 1000+ Customers in Mumbai'),
        ('hero', 'cta_text', 'text', 'Book Now'),
        ('hero', 'cta_phone', 'text', '+91 9819104977'),
        
        # Stats Section
        ('stats', 'customers', 'text', '1000+'),
        ('stats', 'experience', 'text', '10+ Years'),
        ('stats', 'technicians', 'text', '20+'),
        ('stats', 'satisfaction', 'text', '98%'),
        
        # Contact Section
        ('contact', 'phone', 'text', '+91 9819104977'),
        ('contact', 'email', 'text', 'anshaircool@gmail.com'),
        ('contact', 'address', 'text', 'Mumbai, Maharashtra, India'),
        ('contact', 'whatsapp', 'text', '+91 9918331262'),
        
        # Footer Section
        ('footer', 'company_name', 'text', 'Ansh Air Cool'),
        ('footer', 'copyright', 'text', '© 2026 Ansh Air Cool. All rights reserved.'),
        
        # Business Hours
        ('hours', 'monday', 'text', '9:00 AM - 8:00 PM'),
        ('hours', 'sunday', 'text', 'Closed'),
    ]
    
    content_count = 0
    for section, key, content_type, value in default_content:
        existing = WebsiteContent.query.filter_by(
            section_name=section, content_key=key
        ).first()
        
        if not existing:
            content = WebsiteContent(
                section_name=section,
                content_key=key,
                content_value=value,
                content_type=content_type
            )
            db.session.add(content)
            content_count += 1
    
    db.session.commit()
    print(f"      ✅ Created {content_count} content entries")
    return content_count


def create_indexes():
    """Create additional performance indexes"""
    print("\n[BONUS] Creating performance indexes...")
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_customers_phone ON customers(phone)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_customer ON invoices(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_date ON invoices(invoice_date)",
        "CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status)",
        "CREATE INDEX IF NOT EXISTS idx_service_requests_phone ON service_requests(customer_phone)",
        "CREATE INDEX IF NOT EXISTS idx_service_requests_status ON service_requests(request_status)",
        "CREATE INDEX IF NOT EXISTS idx_amc_contracts_customer ON amc_contracts(customer_id)",
        "CREATE INDEX IF NOT EXISTS idx_amc_contracts_status ON amc_contracts(status)",
    ]
    
    created = 0
    with db.engine.connect() as conn:
        for index_sql in indexes:
            try:
                conn.execute(text(index_sql))
                created += 1
            except Exception as e:
                print(f"      ⚠️  Index warning: {e}")
    
    conn.commit()
    print(f"      ✅ Created {created} indexes")
    return created


def main():
    """Main initialization function"""
    print("=" * 80)
    print("  ANSH AIR COOL - PRODUCTION DATABASE INITIALIZATION")
    print("  Database: ac_service_billing")
    print("=" * 80)
    
    try:
        with app.app_context():
            # Create tables
            tables = create_tables()
            
            # Create admin
            admin = create_admin_user()
            
            # Create services
            services = create_default_services()
            
            # Create products
            products = create_default_products()
            
            # Create website content
            content = create_website_content()
            
            # Create indexes
            indexes = create_indexes()
            
            # Summary
            print("\n" + "=" * 80)
            print("  ✅ DATABASE INITIALIZATION COMPLETE!")
            print("=" * 80)
            
            print(f"\n📊 Database Summary:")
            print(f"   • Tables: {len(tables)}")
            print(f"   • Admin Users: 1")
            print(f"   • Services: {services}")
            print(f"   • Products: {products}")
            print(f"   • Website Content: {content} entries")
            print(f"   • Performance Indexes: {indexes}")
            
            print(f"\n🔐 Admin Credentials:")
            print(f"   Username: admin")
            print(f"   Password: Admin@123")
            print(f"   ⚠️  CHANGE THIS IMMEDIATELY AFTER FIRST LOGIN!")
            
            print(f"\n🚀 Next Steps:")
            print(f"   1. Start backend: cd backend && python main.py")
            print(f"   2. Open frontend: Use Live Server on port 5500")
            print(f"   3. Launch desktop software: cd Desktop_software && python main.py")
            print(f"   4. Change admin password from dashboard")
            
            print("\n" + "=" * 80)
            
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ INITIALIZATION FAILED!")
        print(f"   Error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if MySQL is running")
        print("   2. Verify database 'ac_service_billing' exists")
        print("   3. Check .env file has correct DATABASE_URL")
        print("   4. Ensure database user has proper permissions")
        
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
