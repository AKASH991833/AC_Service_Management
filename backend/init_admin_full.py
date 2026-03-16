"""
Initialize Admin Database with Default Data
Creates admin user and default website content
"""

from flask import Flask
from models import db, Admin, WebsiteContent, WebsiteSetting, Service, Testimonial
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/ansh_aircool')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def init_database():
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("📊 Creating database tables...")
        db.create_all()
        print("✅ Database tables created!")
        
        # Check if admin exists
        admin = Admin.query.filter_by(username='admin').first()
        
        if not admin:
            print("👤 Creating default admin user...")
            admin = Admin(
                username='admin',
                email='admin@anshaircool.com',
                full_name='Admin',
                is_active=True
            )
            admin.set_password('admin123')  # Default password
            db.session.add(admin)
            print("✅ Admin user created! (username: admin, password: admin123)")
        else:
            print("✅ Admin user already exists")
        
        # Initialize default website content
        print("📝 Initializing default website content...")
        
        # Hero Section Defaults
        hero_defaults = {
            'title': 'Professional AC Service & Installation at Your Doorstep',
            'subtitle': 'Certified Technicians | Same Day Service | Trusted by 1000+ Customers',
            'cta_text': 'Book Now',
            'cta_phone': '+91 9819104977',
            'background_image': '',
            'show_video': 'false',
            'video_url': ''
        }
        
        for key, value in hero_defaults.items():
            content = WebsiteContent.query.filter_by(section_name='hero', content_key=key).first()
            if not content:
                content = WebsiteContent(
                    section_name='hero',
                    content_key=key,
                    content_value=value,
                    content_type='text'
                )
                db.session.add(content)
        
        # Contact Section Defaults
        contact_defaults = {
            'phone': '+91 9819104977',
            'email': 'anshaircool@gmail.com',
            'whatsapp': '+91 9819104977',
            'address': 'Mumbai, Maharashtra',
            'business_hours': 'Mon - Sat: 9 AM - 8 PM | Sunday: 10 AM - 6 PM',
            'google_maps_embed': '',
            'show_form': 'true'
        }
        
        for key, value in contact_defaults.items():
            content = WebsiteContent.query.filter_by(section_name='contact', content_key=key).first()
            if not content:
                content = WebsiteContent(
                    section_name='contact',
                    content_key=key,
                    content_value=value,
                    content_type='text'
                )
                db.session.add(content)
        
        # Features Section Defaults
        import json
        features_defaults = {
            'title': 'Why Choose Ansh Air Cool?',
            'subtitle': 'We provide the best AC services with experienced technicians',
            'features_list': json.dumps([
                {'icon': 'fas fa-certificate', 'title': 'Certified Technicians', 'description': 'All our technicians are certified and trained'},
                {'icon': 'fas fa-clock', 'title': 'Same Day Service', 'description': 'We provide quick and efficient same-day service'},
                {'icon': 'fas fa-shield-alt', 'title': 'Warranty Protection', 'description': 'All services come with warranty protection'},
                {'icon': 'fas fa-hand-holding-usd', 'title': 'Transparent Pricing', 'description': 'No hidden charges, upfront pricing'}
            ])
        }
        
        for key, value in features_defaults.items():
            content = WebsiteContent.query.filter_by(section_name='features', content_key=key).first()
            if not content:
                content = WebsiteContent(
                    section_name='features',
                    content_key=key,
                    content_value=value,
                    content_type='json' if key == 'features_list' else 'text'
                )
                db.session.add(content)
        
        # Stats Section Defaults
        stats_defaults = {
            'customers_count': '1000+',
            'customers_label': 'Happy Customers',
            'services_count': '5000+',
            'services_label': 'Services Completed',
            'experience_count': '10+',
            'experience_label': 'Years Experience',
            'technicians_count': '50+',
            'technicians_label': 'Expert Technicians'
        }
        
        for key, value in stats_defaults.items():
            content = WebsiteContent.query.filter_by(section_name='stats', content_key=key).first()
            if not content:
                content = WebsiteContent(
                    section_name='stats',
                    content_key=key,
                    content_value=value,
                    content_type='text'
                )
                db.session.add(content)
        
        # Footer Section Defaults
        footer_defaults = {
            'company_name': 'Ansh Air Cool',
            'tagline': 'Professional AC Services',
            'copyright_text': '© 2026 Ansh Air Cool. All rights reserved.',
            'social_facebook': '',
            'social_instagram': '',
            'social_twitter': '',
            'social_youtube': '',
            'quick_links': json.dumps([
                {'label': 'Home', 'url': '#home'},
                {'label': 'Services', 'url': '#services'},
                {'label': 'Products', 'url': '#products'},
                {'label': 'Contact', 'url': '#contact'}
            ])
        }
        
        for key, value in footer_defaults.items():
            content = WebsiteContent.query.filter_by(section_name='footer', content_key=key).first()
            if not content:
                content = WebsiteContent(
                    section_name='footer',
                    content_key=key,
                    content_value=value,
                    content_type='json' if key == 'quick_links' else 'text'
                )
                db.session.add(content)
        
        # JustDial Section Defaults
        justdial_defaults = {
            'show_badge': 'true',
            'badge_image': '',
            'rating': '4.8',
            'review_count': '500+',
            'verified_text': 'Verified by JustDial'
        }
        
        for key, value in justdial_defaults.items():
            content = WebsiteContent.query.filter_by(section_name='justdial', content_key=key).first()
            if not content:
                content = WebsiteContent(
                    section_name='justdial',
                    content_key=key,
                    content_value=value,
                    content_type='text'
                )
                db.session.add(content)
        
        # Site Settings Defaults
        site_defaults = {
            'site_title': 'Ansh Air Cool - Premium AC Services',
            'site_description': 'Professional AC Installation, Repair & Maintenance Services',
            'site_keywords': 'AC service, AC repair, AC installation, HVAC, air conditioning',
            'favicon_url': '',
            'logo_url': '',
            'analytics_code': '',
            'facebook_pixel': '',
            'whatsapp_number': '+91 9819104977',
            'enable_whatsapp': 'true'
        }
        
        for key, value in site_defaults.items():
            setting = WebsiteSetting.query.filter_by(setting_key=key).first()
            if not setting:
                setting = WebsiteSetting(
                    setting_key=key,
                    setting_value=value,
                    setting_type='text'
                )
                db.session.add(setting)
        
        # Initialize default services if none exist
        service_count = Service.query.count()
        if service_count == 0:
            print("🔧 Creating default services...")
            default_services = [
                {
                    'service_name': 'AC Installation',
                    'service_slug': 'ac-installation',
                    'starting_price': '₹1,499',
                    'price_numeric': 1499,
                    'description': 'Professional AC installation service with certified technicians',
                    'duration': '2-3 Hrs',
                    'icon_class': 'fas fa-tools',
                    'features': json.dumps(['Free Site Survey', 'Professional Installation', '1 Year Service Warranty']),
                    'is_active': True,
                    'is_featured': True,
                    'display_order': 1
                },
                {
                    'service_name': 'AC Repair',
                    'service_slug': 'ac-repair',
                    'starting_price': '₹499',
                    'price_numeric': 499,
                    'description': 'Quick and reliable AC repair service for all brands',
                    'duration': '1-2 Hrs',
                    'icon_class': 'fas fa-wrench',
                    'features': json.dumps(['Diagnosis', 'Genuine Parts', '90 Days Warranty']),
                    'is_active': True,
                    'is_featured': True,
                    'display_order': 2
                },
                {
                    'service_name': 'Gas Refilling',
                    'service_slug': 'gas-refilling',
                    'starting_price': '₹1,999',
                    'price_numeric': 1999,
                    'description': 'AC gas refilling service for optimal cooling',
                    'duration': '1-2 Hrs',
                    'icon_class': 'fas fa-wind',
                    'features': json.dumps(['Pressure Check', 'Leak Testing', 'Performance Guarantee']),
                    'is_active': True,
                    'is_featured': False,
                    'display_order': 3
                },
                {
                    'service_name': 'AMC Service',
                    'service_slug': 'amc-service',
                    'starting_price': '₹2,999',
                    'price_numeric': 2999,
                    'description': 'Annual Maintenance Contract for hassle-free AC operation',
                    'duration': 'Year Round',
                    'icon_class': 'fas fa-shield-alt',
                    'features': json.dumps(['4 Quarterly Services', 'Priority Support', '10% Discount on Repairs']),
                    'is_active': True,
                    'is_featured': True,
                    'display_order': 4
                }
            ]
            
            for svc in default_services:
                service = Service(**svc)
                db.session.add(service)
            
            print(f"✅ Created {len(default_services)} default services")
        
        # Initialize default testimonials if none exist
        testimonial_count = Testimonial.query.count()
        if testimonial_count == 0:
            print("⭐ Creating default testimonials...")
            default_testimonials = [
                {
                    'customer_name': 'Rajesh Kumar',
                    'customer_location': 'Mumbai',
                    'review_text': 'Excellent service! The technician was very professional and completed the installation quickly.',
                    'rating': 5,
                    'is_active': True,
                    'is_featured': True,
                    'display_order': 1
                },
                {
                    'customer_name': 'Priya Sharma',
                    'customer_location': 'Pune',
                    'review_text': 'Very satisfied with the AC repair service. Reasonable pricing and quality work.',
                    'rating': 5,
                    'is_active': True,
                    'is_featured': True,
                    'display_order': 2
                },
                {
                    'customer_name': 'Amit Patel',
                    'customer_location': 'Thane',
                    'review_text': 'Great experience with their AMC service. My AC works perfectly throughout the year.',
                    'rating': 5,
                    'is_active': True,
                    'is_featured': False,
                    'display_order': 3
                }
            ]
            
            for tst in default_testimonials:
                testimonial = Testimonial(**tst)
                db.session.add(testimonial)
            
            print(f"✅ Created {len(default_testimonials)} default testimonials")
        
        # Commit all changes
        db.session.commit()
        print("\n✅ Database initialization completed successfully!")
        print("\n📋 Default Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n⚠️  Please change the default password after first login!")

if __name__ == '__main__':
    init_database()
