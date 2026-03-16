"""
Add missing columns to contact_messages table
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

print("Adding missing columns to contact_messages table...")
print()

# Add ac_type column
try:
    cursor.execute("""
        ALTER TABLE contact_messages 
        ADD COLUMN ac_type VARCHAR(20) DEFAULT 'Not Specified' AFTER service_type
    """)
    print("[OK] Added ac_type column")
except Exception as e:
    if "Duplicate column name" in str(e):
        print("[SKIP] ac_type column already exists")
    else:
        print(f"[ERROR] ac_type: {e}")

# Add source column
try:
    cursor.execute("""
        ALTER TABLE contact_messages 
        ADD COLUMN source VARCHAR(50) DEFAULT 'Website' AFTER status
    """)
    print("[OK] Added source column")
except Exception as e:
    if "Duplicate column name" in str(e):
        print("[SKIP] source column already exists")
    else:
        print(f"[ERROR] source: {e}")

# Add ip_address column
try:
    cursor.execute("""
        ALTER TABLE contact_messages 
        ADD COLUMN ip_address VARCHAR(45) AFTER source
    """)
    print("[OK] Added ip_address column")
except Exception as e:
    if "Duplicate column name" in str(e):
        print("[SKIP] ip_address column already exists")
    else:
        print(f"[ERROR] ip_address: {e}")

# Add user_agent column
try:
    cursor.execute("""
        ALTER TABLE contact_messages 
        ADD COLUMN user_agent TEXT AFTER ip_address
    """)
    print("[OK] Added user_agent column")
except Exception as e:
    if "Duplicate column name" in str(e):
        print("[SKIP] user_agent column already exists")
    else:
        print(f"[ERROR] user_agent: {e}")

# Modify email to allow NULL
try:
    cursor.execute("""
        ALTER TABLE contact_messages 
        MODIFY COLUMN email VARCHAR(100) NULL
    """)
    print("[OK] Modified email column to allow NULL")
except Exception as e:
    print(f"[ERROR] email modify: {e}")

# Modify address to allow NULL
try:
    cursor.execute("""
        ALTER TABLE contact_messages 
        MODIFY COLUMN address TEXT NULL
    """)
    print("[OK] Modified address column to allow NULL")
except Exception as e:
    print(f"[ERROR] address modify: {e}")

conn.commit()

print()
print("=== Table Structure ===")
cursor.execute("DESCRIBE contact_messages")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

cursor.close()
conn.close()

print()
print("[OK] Database migration complete!")
