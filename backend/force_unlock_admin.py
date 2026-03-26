"""
Force Unlock Admin Account - Direct SQL
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from main import create_app
from models import db
from sqlalchemy import text
from datetime import datetime

app = create_app()

print("=" * 70)
print("FORCE UNLOCK ADMIN ACCOUNT")
print("=" * 70)

with app.app_context():
    try:
        # Direct SQL to unlock and reset
        db.session.execute(
            text("""
                UPDATE admins 
                SET failed_login_attempts = 0, 
                    locked_until = NULL 
                WHERE username = 'admin'
            """)
        )
        db.session.commit()
        
        print("\n✅ Account unlocked via SQL!")
        
        # Verify
        result = db.session.execute(
            text("SELECT username, failed_login_attempts, locked_until FROM admins WHERE username='admin'")
        )
        admin = result.fetchone()
        
        print("\nCurrent admin status:")
        print(f"  Username: {admin[0]}")
        print(f"  Failed attempts: {admin[1]}")
        print(f"  Locked until: {admin[2]}")
        
        print("\n" + "=" * 70)
        print("✅ NOW YOU CAN LOGIN!")
        print("=" * 70)
        print("  URL: http://localhost:5500/admin/index.html")
        print("  Username: admin")
        print("  Password: admin123")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

print("=" * 70)
