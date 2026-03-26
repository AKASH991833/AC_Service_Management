"""
Show Admin Credentials from Database
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from main import create_app
from models import db, Admin
from sqlalchemy import text

app = create_app()

print("=" * 70)
print("ADMIN CREDENTIALS FROM DATABASE")
print("=" * 70)

with app.app_context():
    try:
        # Check if admins table exists and get all admins
        result = db.session.execute(text("SELECT * FROM admins"))
        admins = result.fetchall()
        
        if admins:
            print(f"\nFound {len(admins)} admin account(s):\n")
            for admin in admins:
                print(f"  Username: {admin[1]}")  # username is column 1
                print(f"  Password: [ENCRYPTED - cannot show]")
                print(f"  Role: {admin[3] if len(admin) > 3 else 'N/A'}")
                print(f"  Created: {admin[4] if len(admin) > 4 else 'N/A'}")
                print("-" * 40)
            
            print("\nDEFAULT CREDENTIALS (from code):")
            print("  Username: admin")
            print("  Password: admin123")
            print("\nNOTE: If default password doesn't work, it was changed.")
            print("You can reset it using: python reset_admin_password.py")
            
        else:
            print("\nNo admins found in database!")
            print("\nDEFAULT CREDENTIALS:")
            print("  Username: admin")
            print("  Password: admin123")
            print("\nRun 'python init_db.py' to create default admin.")
            
    except Exception as e:
        print(f"\nError: {e}")
        print("\nDEFAULT CREDENTIALS (from code):")
        print("  Username: admin")
        print("  Password: admin123")

print("=" * 70)
