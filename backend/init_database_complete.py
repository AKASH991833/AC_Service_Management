"""
Comprehensive Database Initialization Script
Creates tables, admin user, and default content
For both SQLite (development) and MySQL (production)
"""

from main import create_app
from models import db, Admin, WebsiteSetting, WebsiteContent, ServiceRequest, ContactMessage, Service, Product
from sqlalchemy import text
import sys
import os

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = create_app()

with app.app_context():
    print("=" * 80)
    print("  DATABASE INITIALIZATION - ANSH AIR COOL")
    print("=" * 80)
    print()
    
    try:
        # Step 1: Create all tables
        print("[1/4] Creating database tables...")
        db.create_all()
        print("      ✅ All tables created successfully!")
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"      📊 Total tables created: {len(tables)}")
        
        # Step 2: Create default admin user
        print("\n[2/4] Setting up admin user...")
        admin = Admin.query.filter_by(username='admin').first()
        
        if not admin:
            # Create default admin
            admin = Admin(
                username='admin',
                full_name='Admin User',
                email='admin@anshaircool.com',
                is_active=True
            )
            # Set secure default password
            admin.set_password('Admin@123')
            db.session.add(admin)
            db.session.commit()
            print("      ✅ Default admin created!")
            print("         Username: admin")
            print("         Password: Admin@123")
            print("         ⚠️  CHANGE THIS PASSWORD IMMEDIATELY!")
        else:
            print("      ℹ️  Admin user already exists")
        
        # Step 3: Create default website content
        print("\n[3/4] Setting up default website content...")
        default_content = [
            # Hero Section
            ('hero', 'title', 'text', 'Professional AC Service & Installation at Your Doorstep'),
            ('hero', 'subtitle', 'text', 'Certified Technicians | Same Day Service | Trusted by 1000+ Customers in Mumbai'),
            ('hero', 'cta_text', 'text', 'Book Now'),
            ('hero', 'cta_phone', 'text', '+91 9819104977'),
            
            # Services Section
            ('services', 'title', 'text', 'Our Services'),
            ('services', 'subtitle', 'text', 'Complete AC Solutions'),
            
            # Contact Section
            ('contact', 'phone', 'text', '+91 9819104977'),
            ('contact', 'email', 'text', 'anshaircool@gmail.com'),
            ('contact', 'address', 'text', 'Mumbai, Maharashtra, India'),
            
            # Footer Section
            ('footer', 'company_name', 'text', 'Ansh Air Cool'),
            ('footer', 'copyright', 'text', '© 2026 Ansh Air Cool. All rights reserved.'),
            
            # Stats Section
            ('stats', 'customers', 'text', '1000+'),
            ('stats', 'experience', 'text', '10+ Years'),
            ('stats', 'technicians', 'text', '20+'),
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
        print(f"      ✅ Created {content_count} default content entries")
        
        # Step 4: Create default services
        print("\n[4/4] Setting up default services...")
        default_services = [
            ('installation', 'AC Installation', 'Professional installation of new AC units', 500),
            ('repair', 'AC Repair', 'Expert repair for all AC brands and models', 300),
            ('gas_refill', 'Gas Refill', 'Complete gas refill with quality checked refrigerant', 800),
            ('maintenance', 'Maintenance', 'Comprehensive maintenance and servicing', 400),
            ('amc', 'AMC (Annual Maintenance)', 'Yearly maintenance contract for hassle-free operation', 2000),
        ]

        service_count = 0
        for service_slug, name, description, base_price in default_services:
            existing = Service.query.filter_by(service_slug=service_slug).first()

            if not existing:
                service = Service(
                    service_slug=service_slug,
                    service_name=name,
                    description=description,
                    starting_price=f'₹{base_price}',
                    price_numeric=base_price,
                    is_active=True
                )
                db.session.add(service)
                service_count += 1
        
        db.session.commit()
        print(f"      ✅ Created {service_count} default services")
        
        # Summary
        print("\n" + "=" * 80)
        print("  ✅ DATABASE INITIALIZATION COMPLETE!")
        print("=" * 80)
        print(f"\n📊 Database Summary:")
        print(f"   • Tables: {len(tables)}")
        print(f"   • Admin Users: 1")
        print(f"   • Website Content: {content_count} entries")
        print(f"   • Services: {service_count} entries")
        
        print(f"\n📄 Database Location:")
        print(f"   {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        print(f"\n🔐 Admin Login Credentials:")
        print(f"   Username: admin")
        print(f"   Password: Admin@123")
        print(f"   ⚠️  SECURITY WARNING: Change this password immediately!")
        
        print(f"\n🚀 Next Steps:")
        print(f"   1. Start the backend server:")
        print(f"      cd backend")
        print(f"      python main.py")
        print(f"")
        print(f"   2. Open frontend in browser:")
        print(f"      Use Live Server on port 5500")
        print(f"      OR open frontend/index.html directly")
        print(f"")
        print(f"   3. Test the website:")
        print(f"      • Submit a service request")
        print(f"      • Test contact form")
        print(f"      • Login to admin dashboard")
        print(f"")
        print(f"   4. Change admin password:")
        print(f"      Login to admin panel → Profile → Change Password")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ DATABASE INITIALIZATION FAILED!")
        print(f"   Error: {str(e)}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Check if MySQL is running")
        print(f"   2. Verify database 'ansh_aircool' exists")
        print(f"   3. Check .env file has correct DATABASE_URL")
        print(f"   4. Ensure database user has proper permissions")
        print(f"\n   Current DATABASE_URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("\n" + "=" * 80)
        import traceback
        traceback.print_exc()
        sys.exit(1)
