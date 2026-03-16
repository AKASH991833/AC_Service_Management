"""
Complete Database Setup for Admin Panel
Drops and recreates tables with correct structure
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def setup_database():
    # Database credentials
    db_name = 'ac_service_billing'
    host = 'localhost'
    port = 3306
    user = 'root'
    password = 'Akash@9918'
    
    print(f"📊 Connecting to database: {db_name}")
    
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        cursor.execute(f"USE {db_name}")
        print(f"✅ Connected to database: {db_name}")
        
        # Drop foreign keys and recreate services table
        print("\n🔧 Updating services table...")
        
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        cursor.execute("DROP TABLE IF EXISTS services")
        cursor.execute("""
            CREATE TABLE services (
                id INT AUTO_INCREMENT PRIMARY KEY,
                service_name VARCHAR(100) NOT NULL,
                service_slug VARCHAR(100) UNIQUE NOT NULL,
                starting_price VARCHAR(50) NOT NULL,
                price_numeric INT,
                description TEXT,
                duration VARCHAR(50),
                icon_class VARCHAR(50),
                features TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                display_order INT DEFAULT 0,
                is_featured BOOLEAN DEFAULT FALSE,
                service_image VARCHAR(500),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("   ✅ Created services table")
        
        # Create products table
        print("\n🔧 Creating products table...")
        cursor.execute("DROP TABLE IF EXISTS products")
        cursor.execute("""
            CREATE TABLE products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_type VARCHAR(20) NOT NULL,
                product_name VARCHAR(150) NOT NULL,
                brand VARCHAR(50),
                capacity VARCHAR(20),
                ac_type VARCHAR(20),
                star_rating INT DEFAULT 3,
                is_inverter BOOLEAN DEFAULT FALSE,
                price VARCHAR(50) NOT NULL,
                price_numeric INT,
                description TEXT,
                features TEXT,
                product_image VARCHAR(500),
                image_gallery TEXT,
                is_available BOOLEAN DEFAULT TRUE,
                stock_status VARCHAR(20) DEFAULT 'In Stock',
                rental_min_months INT,
                rental_deposit VARCHAR(50),
                rental_includes TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                is_featured BOOLEAN DEFAULT FALSE,
                display_order INT DEFAULT 0,
                badge_text VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("   ✅ Created products table")
        
        # Create testimonials table
        print("\n🔧 Creating testimonials table...")
        cursor.execute("DROP TABLE IF EXISTS testimonials")
        cursor.execute("""
            CREATE TABLE testimonials (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(100) NOT NULL,
                customer_location VARCHAR(100),
                review_text TEXT NOT NULL,
                rating INT DEFAULT 5,
                customer_photo VARCHAR(500),
                is_active BOOLEAN DEFAULT TRUE,
                is_featured BOOLEAN DEFAULT FALSE,
                display_order INT DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("   ✅ Created testimonials table")
        
        # Create website_content table
        print("\n🔧 Creating website_content table...")
        cursor.execute("DROP TABLE IF EXISTS website_content")
        cursor.execute("""
            CREATE TABLE website_content (
                id INT AUTO_INCREMENT PRIMARY KEY,
                section_name VARCHAR(50) NOT NULL,
                content_key VARCHAR(100) NOT NULL,
                content_value TEXT NOT NULL,
                content_type VARCHAR(20) DEFAULT 'text',
                is_active BOOLEAN DEFAULT TRUE,
                display_order INT DEFAULT 0,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("   ✅ Created website_content table")
        
        # Create gallery_images table
        print("\n🔧 Creating gallery_images table...")
        cursor.execute("DROP TABLE IF EXISTS gallery_images")
        cursor.execute("""
            CREATE TABLE gallery_images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image_path VARCHAR(500) NOT NULL,
                image_url VARCHAR(500) NOT NULL,
                category VARCHAR(50) NOT NULL DEFAULT 'gallery',
                alt_text VARCHAR(200),
                file_size INT,
                mime_type VARCHAR(50),
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("   ✅ Created gallery_images table")
        
        # Create website_setting table if not exists
        print("\n🔧 Creating website_setting table...")
        cursor.execute("DROP TABLE IF EXISTS website_settings")
        cursor.execute("""
            CREATE TABLE website_settings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT,
                setting_type VARCHAR(20) DEFAULT 'text',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("   ✅ Created website_settings table")
        
        conn.commit()
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        print("\n" + "="*60)
        print("✅ All tables created successfully!")
        print("="*60)
        
        cursor.close()
        conn.close()
        
        # Now run init script
        print("\n📝 Initializing default data...")
        init_default_data()
        
    except mysql.connector.Error as err:
        print(f"\n❌ Database error: {err}")

def init_default_data():
    """Initialize default data for all sections"""
    import json
    
    db_name = 'ac_service_billing'
    host = 'localhost'
    port = 3306
    user = 'root'
    password = 'Akash@9918'
    
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password
    )
    cursor = conn.cursor()
    
    cursor.execute(f"USE {db_name}")
    
    # Insert default services
    print("   Adding default services...")
    services = [
        ('AC Installation', 'ac-installation', '₹1,499', 1499, 'Professional AC installation service', '2-3 Hrs', 'fas fa-tools', '["Free Site Survey", "Professional Installation", "1 Year Warranty"]', 1),
        ('AC Repair', 'ac-repair', '₹499', 499, 'Quick AC repair for all brands', '1-2 Hrs', 'fas fa-wrench', '["Diagnosis", "Genuine Parts", "90 Days Warranty"]', 2),
        ('Gas Refilling', 'gas-refilling', '₹1,999', 1999, 'AC gas refilling service', '1-2 Hrs', 'fas fa-wind', '["Pressure Check", "Leak Testing", "Performance Guarantee"]', 3),
        ('AMC Service', 'amc-service', '₹2,999', 2999, 'Annual maintenance contract', 'Year Round', 'fas fa-shield-alt', '["4 Quarterly Services", "Priority Support", "10% Discount"]', 4)
    ]
    
    cursor.executemany("""
        INSERT INTO services (service_name, service_slug, starting_price, price_numeric, description, duration, icon_class, features, display_order)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, services)
    
    # Insert default testimonials
    print("   Adding default testimonials...")
    testimonials = [
        ('Rajesh Kumar', 'Mumbai', 'Excellent service! Very professional.', 5, 1),
        ('Priya Sharma', 'Pune', 'Great experience with their service.', 5, 2),
        ('Amit Patel', 'Thane', 'Highly recommended for AC services.', 5, 3)
    ]
    
    cursor.executemany("""
        INSERT INTO testimonials (customer_name, customer_location, review_text, rating, display_order)
        VALUES (%s, %s, %s, %s, %s)
    """, testimonials)
    
    # Insert default website content
    print("   Adding default website content...")
    
    # Hero section
    hero_content = [
        ('hero', 'title', 'Professional AC Service & Installation at Your Doorstep'),
        ('hero', 'subtitle', 'Certified Technicians | Same Day Service | Trusted by 1000+ Customers'),
        ('hero', 'cta_text', 'Book Now'),
        ('hero', 'cta_phone', '+91 9819104977'),
        ('hero', 'background_image', ''),
        ('hero', 'show_video', 'false'),
        ('hero', 'video_url', '')
    ]
    
    cursor.executemany("""
        INSERT INTO website_content (section_name, content_key, content_value)
        VALUES (%s, %s, %s)
    """, hero_content)
    
    # Contact section
    contact_content = [
        ('contact', 'phone', '+91 9819104977'),
        ('contact', 'whatsapp', '+91 9819104977'),
        ('contact', 'email', 'anshaircool@gmail.com'),
        ('contact', 'address', 'Mumbai, Maharashtra'),
        ('contact', 'business_hours', 'Mon - Sat: 9 AM - 8 PM | Sunday: 10 AM - 6 PM'),
        ('contact', 'google_maps_embed', ''),
        ('contact', 'show_form', 'true')
    ]
    
    cursor.executemany("""
        INSERT INTO website_content (section_name, content_key, content_value)
        VALUES (%s, %s, %s)
    """, contact_content)
    
    # Features section
    features_content = [
        ('features', 'title', 'Why Choose Ansh Air Cool?'),
        ('features', 'subtitle', 'We provide the best AC services with experienced technicians'),
        ('features', 'features_list', json.dumps([
            {'icon': 'fas fa-certificate', 'title': 'Certified Technicians', 'description': 'All technicians certified'},
            {'icon': 'fas fa-clock', 'title': 'Same Day Service', 'description': 'Quick service'},
            {'icon': 'fas fa-shield-alt', 'title': 'Warranty Protection', 'description': 'Service warranty'},
            {'icon': 'fas fa-hand-holding-usd', 'title': 'Transparent Pricing', 'description': 'No hidden charges'}
        ]))
    ]
    
    cursor.executemany("""
        INSERT INTO website_content (section_name, content_key, content_value)
        VALUES (%s, %s, %s)
    """, features_content)
    
    # Stats section
    stats_content = [
        ('stats', 'customers_count', '1000+'),
        ('stats', 'customers_label', 'Happy Customers'),
        ('stats', 'services_count', '5000+'),
        ('stats', 'services_label', 'Services Completed'),
        ('stats', 'experience_count', '10+'),
        ('stats', 'experience_label', 'Years Experience'),
        ('stats', 'technicians_count', '50+'),
        ('stats', 'technicians_label', 'Expert Technicians')
    ]
    
    cursor.executemany("""
        INSERT INTO website_content (section_name, content_key, content_value)
        VALUES (%s, %s, %s)
    """, stats_content)
    
    # Footer section
    footer_content = [
        ('footer', 'company_name', 'Ansh Air Cool'),
        ('footer', 'tagline', 'Professional AC Services'),
        ('footer', 'copyright_text', '© 2026 Ansh Air Cool. All rights reserved.'),
        ('footer', 'social_facebook', ''),
        ('footer', 'social_instagram', ''),
        ('footer', 'social_twitter', ''),
        ('footer', 'social_youtube', '')
    ]
    
    cursor.executemany("""
        INSERT INTO website_content (section_name, content_key, content_value)
        VALUES (%s, %s, %s)
    """, footer_content)
    
    # JustDial section
    justdial_content = [
        ('justdial', 'show_badge', 'true'),
        ('justdial', 'badge_image', ''),
        ('justdial', 'rating', '4.8'),
        ('justdial', 'review_count', '500+'),
        ('justdial', 'verified_text', 'Verified by JustDial')
    ]
    
    cursor.executemany("""
        INSERT INTO website_content (section_name, content_key, content_value)
        VALUES (%s, %s, %s)
    """, justdial_content)
    
    # Site settings
    site_settings = [
        ('site_title', 'Ansh Air Cool - Premium AC Services'),
        ('site_description', 'Professional AC Installation, Repair & Maintenance Services'),
        ('site_keywords', 'AC service, AC repair, AC installation, HVAC'),
        ('favicon_url', ''),
        ('logo_url', ''),
        ('analytics_code', ''),
        ('whatsapp_number', '+91 9819104977'),
        ('enable_whatsapp', 'true')
    ]
    
    cursor.executemany("""
        INSERT INTO website_settings (setting_key, setting_value)
        VALUES (%s, %s)
    """, site_settings)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("   ✅ Default data added successfully!")
    print("\n" + "="*60)
    print("✅ Database setup completed!")
    print("="*60)
    print("\n📋 Login Credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n⚠️  Change the default password after login!")

if __name__ == '__main__':
    print("🚀 Setting up Database for Admin Panel...")
    print("="*60)
    setup_database()
