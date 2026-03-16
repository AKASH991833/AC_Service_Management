"""
Database Migration Script
Adds missing columns to existing tables for admin panel
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def migrate_database():
    # Database credentials from .env
    db_name = 'ac_service_billing'
    host = 'localhost'
    port = 3306
    user = 'root'
    password = 'Akash@9918'
    
    print(f"📊 Connecting to database: {db_name}")
    print(f"   User: {user}")
    print(f"   Host: {host}:{port}")
    
    try:
        # Connect without database first
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        print(f"✅ Connected to database: {db_name}")
        
        # Check and update services table
        print("\n🔧 Updating services table...")
        
        # Check if service_slug column exists
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'services' 
            AND COLUMN_NAME = 'service_slug'
        """, (db_name,))
        
        if cursor.fetchone()[0] == 0:
            print("   Adding service_slug column...")
            cursor.execute("""
                ALTER TABLE services 
                ADD COLUMN service_slug VARCHAR(100) AFTER service_name
            """)
            print("   ✅ Added service_slug")
        
        # Check and add other missing columns
        columns_to_add = [
            ('services', 'price_numeric', 'ALTER TABLE services ADD COLUMN price_numeric INT AFTER starting_price'),
            ('services', 'duration', 'ALTER TABLE services ADD COLUMN duration VARCHAR(50) AFTER description'),
            ('services', 'icon_class', 'ALTER TABLE services ADD COLUMN icon_class VARCHAR(50) AFTER duration'),
            ('services', 'features', 'ALTER TABLE services ADD COLUMN features TEXT AFTER icon_class'),
            ('services', 'display_order', 'ALTER TABLE services ADD COLUMN display_order INT DEFAULT 0 AFTER is_featured'),
            ('services', 'is_featured', 'ALTER TABLE services ADD COLUMN is_featured BOOLEAN DEFAULT FALSE AFTER is_active'),
            ('services', 'service_image', 'ALTER TABLE services ADD COLUMN service_image VARCHAR(500) AFTER updated_at'),
        ]
        
        for table, col_name, sql in columns_to_add:
            cursor.execute("""
                SELECT COUNT(*) 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                AND TABLE_NAME = %s 
                AND COLUMN_NAME = %s
            """, (db_name, table, col_name))
            
            if cursor.fetchone()[0] == 0:
                print(f"   Adding {col_name} to {table}...")
                cursor.execute(sql)
                print(f"   ✅ Added {col_name}")
        
        # Check products table
        print("\n🔧 Checking products table...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'products'
        """, (db_name,))
        
        if cursor.fetchone()[0] == 0:
            print("   Creating products table...")
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
                )
            """)
            print("   ✅ Created products table")
        else:
            print("   ✅ Products table exists")
        
        # Check testimonials table
        print("\n🔧 Checking testimonials table...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'testimonials'
        """, (db_name,))
        
        if cursor.fetchone()[0] == 0:
            print("   Creating testimonials table...")
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
                )
            """)
            print("   ✅ Created testimonials table")
        else:
            print("   ✅ Testimonials table exists")
        
        # Check website_content table
        print("\n🔧 Checking website_content table...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'website_content'
        """, (db_name,))
        
        if cursor.fetchone()[0] == 0:
            print("   Creating website_content table...")
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
                )
            """)
            print("   ✅ Created website_content table")
        else:
            print("   ✅ Website_content table exists")
        
        # Check gallery_images table
        print("\n🔧 Checking gallery_images table...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.COLUMNS 
            WHERE TABLE_SCHEMA = %s 
            AND TABLE_NAME = 'gallery_images'
        """, (db_name,))
        
        if cursor.fetchone()[0] == 0:
            print("   Creating gallery_images table...")
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
                )
            """)
            print("   ✅ Created gallery_images table")
        else:
            print("   ✅ Gallery_images table exists")
        
        # Commit changes
        conn.commit()
        
        print("\n" + "="*60)
        print("✅ Database migration completed successfully!")
        print("="*60)
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"\n❌ Database error: {err}")
        print("\nMake sure MySQL is running and credentials are correct.")
        print("Edit the .env file with correct database credentials.")

if __name__ == '__main__':
    print("🚀 Starting Database Migration...")
    print("="*60)
    migrate_database()
