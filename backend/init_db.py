"""
Database Initialization Script
Creates tables in the existing billing database (ac_service_billing)
Matches the billing software schema
"""

from main import create_app
from models import db, ServiceRequest, ContactMessage
from sqlalchemy import text
import sys

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

app = create_app()

with app.app_context():
    try:
        # Create all tables
        db.create_all()
        print("[OK] Tables created successfully!")
        
        # Verify tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("\n=== Database Tables ===")
        for table in tables:
            print(f"  [OK] {table}")
        
        print(f"\nTotal tables in database: {len(tables)}")
        
        # Check specifically for our tables
        print("\n=== Website Tables Status ===")
        if 'service_requests' in tables:
            print("  [OK] service_requests table exists")
            # Count records
            result = db.session.execute(text("SELECT COUNT(*) as count FROM service_requests"))
            count = result.fetchone()[0]
            print(f"    Records: {count}")
        else:
            print("  [ERROR] service_requests table NOT found")
            
        if 'contact_messages' in tables:
            print("  [OK] contact_messages table exists")
            # Count records
            result = db.session.execute(text("SELECT COUNT(*) as count FROM contact_messages"))
            count = result.fetchone()[0]
            print(f"    Records: {count}")
        else:
            print("  [ERROR] contact_messages table NOT found")
        
        print("\n[OK] Database initialization complete!")
        print("\nNext steps:")
        print("  1. Run the backend: python main.py")
        print("  2. Open frontend in browser (use Live Server on port 5500)")
        print("  3. Test form submissions")
        print("  4. Check billing software for online requests")
        
    except Exception as e:
        print(f"\n[ERROR] Database initialization failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Check MySQL is running")
        print("  2. Verify database 'ac_service_billing' exists")
        print("  3. Check .env file has correct credentials")
        print("  4. Run the SQL migration: sql/add_contact_messages_table.sql")
