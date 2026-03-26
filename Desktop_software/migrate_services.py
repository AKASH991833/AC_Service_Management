"""
Database Migration Script - Add default_rate column to services table
This script adds the missing 'default_rate' column to services and parts tables
for the desktop software.

Run: python Desktop_software/migrate_services.py
SECURITY: All credentials loaded from environment variables only
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from Desktop_software/.env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

# ============================================================================
# SECURE DATABASE CONFIGURATION - NO HARDCODED VALUES
# ============================================================================
def get_database_config():
    """Get database configuration from environment variables"""
    db_password = os.getenv('DB_PASSWORD')
    
    if not db_password or db_password.strip() == '':
        print("\n" + "="*80)
        print("🔒 SECURITY ERROR: DB_PASSWORD environment variable not set!")
        print("="*80)
        print("\nPlease create .env file in Desktop_software directory:")
        print("  DB_PASSWORD=your_secure_password")
        print("  DB_USER=root")
        print("  DB_HOST=localhost")
        print("  DB_NAME=ac_service_billing")
        print("="*80 + "\n")
        sys.exit(1)
    
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': db_password,
        'database': os.getenv('DB_NAME', 'ac_service_billing'),  # Standardized DB name
        'port': int(os.getenv('DB_PORT', '3306'))
    }

# Load secure configuration
DB_CONFIG = get_database_config()
DB_HOST = DB_CONFIG['host']
DB_USER = DB_CONFIG['user']
DB_PASSWORD = DB_CONFIG['password']
DB_NAME = DB_CONFIG['database']
# ============================================================================

try:
    import pymysql
    print("=" * 70)
    print("DATABASE MIGRATION - Add default_rate column")
    print("=" * 70)
    
    # Connect to database
    print(f"\nConnecting to database: {DB_NAME}@{DB_HOST}")
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    print("✓ Database connected successfully")
    
    # Check and add default_rate to services table
    print("\n[1/2] Checking services table...")
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'services' AND COLUMN_NAME = 'default_rate'
    """, (DB_NAME,))
    
    if not cursor.fetchone():
        print("      Adding 'default_rate' column to services table...")
        cursor.execute("""
            ALTER TABLE services 
            ADD COLUMN default_rate DECIMAL(10,2) DEFAULT 0
        """)
        conn.commit()
        print("      ✓ Column 'default_rate' added to services table")
        
        # Copy data from price_numeric to default_rate if exists
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'services' AND COLUMN_NAME = 'price_numeric'
        """, (DB_NAME,))
        if cursor.fetchone():
            print("      Copying data from price_numeric to default_rate...")
            cursor.execute("""
                UPDATE services 
                SET default_rate = COALESCE(price_numeric, 0)
                WHERE default_rate = 0
            """)
            conn.commit()
            print("      ✓ Data copied successfully")
    else:
        print("      ✓ Column 'default_rate' already exists in services table")
    
    # Check and add default_rate to parts table
    print("\n[2/2] Checking parts table...")
    
    # First check if parts table exists
    cursor.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'parts'
    """, (DB_NAME,))
    
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        print("      ℹ️  Parts table does not exist (skipping)")
    else:
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'parts' AND COLUMN_NAME = 'default_rate'
        """, (DB_NAME,))
        
        if not cursor.fetchone():
            print("      Adding 'default_rate' column to parts table...")
            cursor.execute("""
                ALTER TABLE parts 
                ADD COLUMN default_rate DECIMAL(10,2) DEFAULT 0
            """)
            conn.commit()
            print("      ✓ Column 'default_rate' added to parts table")
        else:
            print("      ✓ Column 'default_rate' already exists in parts table")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 70)
    print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nThe desktop software should now work correctly.")
    print("\nNext steps:")
    print("  1. Restart the desktop application")
    print("  2. Test the Online Requests view")
    print("  3. Test the Invoice view (uses services/parts)")
    
except ImportError:
    print("\n❌ ERROR: PyMySQL not installed")
    print("Install with: pip install pymysql")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ MIGRATION FAILED: {str(e)}")
    print("\nTroubleshooting:")
    print("  1. Check MySQL is running")
    print("  2. Verify database credentials in backend/.env")
    print("  3. Ensure database exists")
    import traceback
    traceback.print_exc()
    sys.exit(1)
