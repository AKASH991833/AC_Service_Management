"""
Add missing columns to service_requests table
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

print("Adding missing columns to service_requests table...")
print()

# Add source column
try:
    cursor.execute("""
        ALTER TABLE service_requests 
        ADD COLUMN source VARCHAR(50) DEFAULT 'Website' AFTER request_status
    """)
    print("[OK] Added source column")
except Exception as e:
    if "Duplicate column name" in str(e):
        print("[SKIP] source column already exists")
    else:
        print(f"[ERROR] source: {e}")

# Already have ip_address and user_agent from before

conn.commit()

print()
print("=== Updated Table Structure ===")
cursor.execute("DESCRIBE service_requests")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

cursor.close()
conn.close()

print()
print("[OK] service_requests table migration complete!")
