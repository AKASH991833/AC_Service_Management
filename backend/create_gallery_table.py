"""
Database Migration Script - Add Gallery Images Table
Run this to create the gallery_images table
"""

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Akash@9918',  # From .env file
    'database': 'ac_service_billing'
}

def create_gallery_table():
    """Create gallery_images table if it doesn't exist"""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS gallery_images (
            id INT AUTO_INCREMENT PRIMARY KEY,
            image_path VARCHAR(500) NOT NULL,
            image_url VARCHAR(500) NOT NULL,
            category VARCHAR(50) NOT NULL DEFAULT 'gallery',
            alt_text VARCHAR(200),
            file_size INT,
            mime_type VARCHAR(50),
            is_active BOOLEAN DEFAULT TRUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_category (category),
            INDEX idx_active (is_active)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """

        cursor.execute(create_table_query)
        conn.commit()

        print("[OK] Gallery images table created successfully!")
        print("\nTable structure:")
        print("- id: Primary key")
        print("- image_path: File system path")
        print("- image_url: Web URL")
        print("- category: services, products, gallery, banner")
        print("- alt_text: Image description")
        print("- file_size: File size in bytes")
        print("- mime_type: Content type")
        print("- is_active: Soft delete flag")
        print("- created_at: Upload timestamp")
        print("- updated_at: Last update timestamp")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"[ERROR] Error: {err}")
        return False

    return True


if __name__ == '__main__':
    print("=" * 60)
    print("MIGRATION: Creating Gallery Images Table")
    print("=" * 60)
    print()

    success = create_gallery_table()

    print()
    print("=" * 60)
    if success:
        print("[OK] MIGRATION COMPLETED SUCCESSFULLY")
        print("\nYou can now:")
        print("1. Start the backend server: python main.py")
        print("2. Open admin panel: http://localhost:5500/admin/index.html")
        print("3. Upload images to gallery")
    else:
        print("[ERROR] MIGRATION FAILED")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database credentials are correct in .env")
        print("3. Database 'ac_service_billing' exists")
    print("=" * 60)
