"""
Initialize Admin Database
Creates default admin user and website settings
Run this script once to setup admin dashboard
"""

import sys
import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
import bcrypt

# Load environment variables
load_dotenv()

# Get database credentials
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/ansh_aircool')

def parse_db_url(url):
    """Parse MySQL database URL"""
    # Remove mysql+pymysql:// prefix
    if url.startswith('mysql+pymysql://'):
        url = url[16:]
    
    # Parse user:password@host:port/database
    try:
        user_pass, rest = url.split('@')
        host_db = rest.split('/')
        database = host_db[1] if len(host_db) > 1 else ''
        host_port = host_db[0].split(':')
        host = host_port[0]
        port = int(host_port[1]) if len(host_port) > 1 else 3306
        
        user_pass_parts = user_pass.split(':')
        user = user_pass_parts[0]
        password = user_pass_parts[1] if len(user_pass_parts) > 1 else ''
        
        # URL decode password
        from urllib.parse import unquote
        password = unquote(password)
        
        return {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
    except Exception as e:
        print(f"Error parsing database URL: {e}")
        return None

def init_admin_db():
    """Initialize admin database with default data"""
    
    print("Initializing Admin Database...")
    
    db_config = parse_db_url(DATABASE_URL)
    if not db_config:
        print("Error: Could not parse database URL")
        return
    
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = conn.cursor()
        
        print("Connected to database successfully!")
        
        # Create admins table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                full_name VARCHAR(100),
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        """)
        
        # Create website_settings table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS website_settings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                setting_key VARCHAR(100) UNIQUE NOT NULL,
                setting_value TEXT,
                setting_type VARCHAR(20) DEFAULT 'text',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        
        # Check if admin already exists
        cursor.execute("SELECT id FROM admins WHERE username = %s", ('admin',))
        existing_admin = cursor.fetchone()
        
        if existing_admin:
            print("Warning: Admin user already exists!")
        else:
            # Create default admin user
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute("""
                INSERT INTO admins (username, password_hash, email, full_name, is_active)
                VALUES (%s, %s, %s, %s, %s)
            """, ('admin', password_hash, 'admin@anshaircool.com', 'Admin User', True))
            
            conn.commit()
            
            print("Success: Default admin user created!")
            print("   Username: admin")
            print("   Password: admin123")
            print("   Warning: Please change the password after first login!")
        
        # Initialize default website settings
        default_settings = {
            'hero_title': 'Professional AC Service & Installation at Your Doorstep',
            'hero_subtitle': 'Certified Technicians | Same Day Service | Trusted by 1000+ Customers',
            'contact_phone': '+91 9819104977',
            'contact_email': 'anshaircool@gmail.com',
            'business_hours': 'Mon - Sat: 9 AM - 8 PM | Sunday: 10 AM - 6 PM',
            'address': 'Mumbai, Maharashtra',
            'whatsapp_number': '919819104977',
            'whatsapp_enabled': 'true',
            'installation_price': 'Rs. 1,499',
            'repair_price': 'Rs. 499',
            'gas_price': 'Rs. 2,499'
        }
        
        settings_created = 0
        for key, value in default_settings.items():
            cursor.execute("SELECT id FROM website_settings WHERE setting_key = %s", (key,))
            existing = cursor.fetchone()
            
            if not existing:
                cursor.execute("""
                    INSERT INTO website_settings (setting_key, setting_value, setting_type)
                    VALUES (%s, %s, %s)
                """, (key, value, 'text'))
                settings_created += 1
        
        conn.commit()
        
        if settings_created > 0:
            print(f"Success: Created {settings_created} default website settings!")
        else:
            print("Info: Website settings already exist!")
        
        cursor.close()
        conn.close()
        
        print("")
        print("Admin Dashboard initialization complete!")
        print("")
        print("Login Details:")
        print("   URL: http://localhost:5500/admin/index.html")
        print("   Username: admin")
        print("   Password: admin123")
        print("")
        print("SECURITY WARNING:")
        print("   Please change the default password immediately after login!")
        
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        print("Make sure MySQL is running and credentials are correct in .env file")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    init_admin_db()
