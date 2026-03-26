"""
Initialize Database Script
Creates fresh database with correct schema
"""

import sys
sys.path.insert(0, 'backend')

from main import create_app
from models import db, Admin, WebsiteSetting, WebsiteContent

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()
    print("✅ Database tables created successfully!")
    
    # Check if admin exists
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        # Create default admin
        admin = Admin(
            username='admin',
            full_name='Admin User',
            email='admin@anshaircool.com',
            is_active=True
        )
        admin.set_password('Admin@123')
        db.session.add(admin)
        print("✅ Default admin created: username=admin, password=Admin@123")
    else:
        print("ℹ️  Admin user already exists")
    
    # Create default website settings
    default_settings = {
        ('hero', 'title', 'text', 'Professional AC Service & Installation'),
        ('hero', 'subtitle', 'text', 'Certified Technicians | Same Day Service'),
        ('contact', 'phone', 'text', '+91 9819104977'),
        ('contact', 'email', 'text', 'anshaircool@gmail.com'),
        ('footer', 'company_name', 'text', 'Ansh Air Cool'),
    }
    
    for section, key, type, value in default_settings:
        content = WebsiteContent.query.filter_by(
            section_name=section, content_key=key
        ).first()
        if not content:
            content = WebsiteContent(
                section_name=section,
                content_key=key,
                content_value=value,
                content_type=type
            )
            db.session.add(content)
    
    db.session.commit()
    print("✅ Default website content created")
    
    # Print database path
    print(f"\n📄 Database location: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print("\n✅ Database initialization complete!")
