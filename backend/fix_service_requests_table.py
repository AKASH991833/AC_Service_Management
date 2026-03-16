"""
Fix service_requests table - Rename columns to match backend models
"""
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user='root',
    password=os.getenv('DB_PASSWORD', 'Akash@9918'),
    database='ac_service_billing'
)

cursor = conn.cursor()

print("Fixing service_requests table columns...")
print()

# Rename name -> customer_name
try:
    cursor.execute("""
        ALTER TABLE service_requests 
        CHANGE COLUMN name customer_name VARCHAR(100) NOT NULL
    """)
    print("[OK] Renamed 'name' to 'customer_name'")
except Exception as e:
    if "Unknown column" in str(e):
        print("[SKIP] 'name' column doesn't exist, checking for 'customer_name'...")
        # Check if customer_name already exists
        cursor.execute("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'service_requests' AND COLUMN_NAME = 'customer_name'
        """)
        if cursor.fetchone():
            print("[OK] 'customer_name' already exists")
        else:
            print(f"[ERROR] {e}")
    else:
        print(f"[ERROR] Renaming name: {e}")

# Rename email -> customer_email
try:
    cursor.execute("""
        ALTER TABLE service_requests 
        CHANGE COLUMN email customer_email VARCHAR(100)
    """)
    print("[OK] Renamed 'email' to 'customer_email'")
except Exception as e:
    if "Unknown column" in str(e):
        print("[SKIP] 'email' column doesn't exist")
    else:
        print(f"[ERROR] Renaming email: {e}")

# Rename phone -> customer_phone
try:
    cursor.execute("""
        ALTER TABLE service_requests 
        CHANGE COLUMN phone customer_phone VARCHAR(15) NOT NULL
    """)
    print("[OK] Renamed 'phone' to 'customer_phone'")
except Exception as e:
    if "Unknown column" in str(e):
        print("[SKIP] 'phone' column doesn't exist")
    else:
        print(f"[ERROR] Renaming phone: {e}")

# Rename address -> customer_address with TEXT type
try:
    cursor.execute("""
        ALTER TABLE service_requests 
        CHANGE COLUMN address customer_address TEXT NOT NULL
    """)
    print("[OK] Renamed 'address' to 'customer_address' (TEXT)")
except Exception as e:
    if "Unknown column" in str(e):
        print("[SKIP] 'address' column doesn't exist")
    else:
        print(f"[ERROR] Renaming address: {e}")

# Rename status -> request_status
try:
    cursor.execute("""
        ALTER TABLE service_requests 
        CHANGE COLUMN status request_status VARCHAR(20) DEFAULT 'Pending'
    """)
    print("[OK] Renamed 'status' to 'request_status'")
except Exception as e:
    if "Unknown column" in str(e):
        print("[SKIP] 'status' column doesn't exist")
    else:
        print(f"[ERROR] Renaming status: {e}")

# Add is_active column if not exists
try:
    cursor.execute("""
        ALTER TABLE service_requests 
        ADD COLUMN is_active BOOLEAN DEFAULT TRUE AFTER user_agent
    """)
    print("[OK] Added 'is_active' column")
except Exception as e:
    if "Duplicate column name" in str(e):
        print("[SKIP] 'is_active' column already exists")
    else:
        print(f"[ERROR] Adding is_active: {e}")

conn.commit()

print()
print("=== Updated Table Structure ===")
cursor.execute("DESCRIBE service_requests")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]} {row[2]} {row[3]}")

cursor.close()
conn.close()

print()
print("[OK] service_requests table migration complete!")
