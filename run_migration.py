# Run This Script to Create Tables
import sys
import os

# Add backend to path
backend_path = r'E:\WEBISTE UI ADN BAC - Copy\backend'
sys.path.insert(0, backend_path)
os.chdir(backend_path)

# Import and run
from create_new_tables import create_new_tables
from main import create_app

print("🔧 Creating database tables...")
print()

app = create_app()

with app.app_context():
    create_new_tables()
    print()
    print("✅ All tables created successfully!")
    print()
    print("Next Steps:")
    print("1. Restart backend")
    print("2. Login to admin dashboard")
    print("3. Check new sections in sidebar")
