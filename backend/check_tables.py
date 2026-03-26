"""
Check Database Tables
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from main import create_app
from models import db
from sqlalchemy import text

app = create_app()

print("=" * 70)
print("DATABASE TABLES INFO")
print("=" * 70)

with app.app_context():
    try:
        # Get all tables
        result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"))
        tables = [row[0] for row in result.fetchall()]
        
        print(f"\n📊 Total Tables: {len(tables)}")
        print("\n📋 Tables List:")
        print("-" * 70)
        
        for i, table_name in enumerate(tables, 1):
            # Count records in each table
            try:
                count_result = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                count = count_result.fetchone()[0]
                print(f"  {i:2}. {table_name:<30} ({count} records)")
            except:
                print(f"  {i:2}. {table_name:<30} (unknown)")
        
        print("-" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

print("=" * 70)
