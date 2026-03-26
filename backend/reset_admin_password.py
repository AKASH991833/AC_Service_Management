"""
Reset Admin Password and Unlock Account
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from main import create_app
from models import db, Admin
from sqlalchemy import text
import bcrypt

app = create_app()

print("=" * 70)
print("ADMIN PASSWORD RESET & UNLOCK")
print("=" * 70)

with app.app_context():
    try:
        # Find admin user
        admin = Admin.query.filter_by(username='admin').first()
        
        if admin:
            # Reset password to 'admin123'
            new_password = 'admin123'
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(rounds=12))
            
            admin.password_hash = hashed.decode('utf-8')
            admin.failed_login_attempts = 0  # Reset failed attempts
            admin.locked_until = None  # Unlock account
            
            db.session.commit()
            
            print("\n✅ SUCCESS! Admin account unlocked and password reset!")
            print("\n" + "=" * 70)
            print("NEW LOGIN CREDENTIALS:")
            print("=" * 70)
            print("  Username: admin")
            print("  Password: admin123")
            print("=" * 70)
            print("\nYou can now login at: http://localhost:5500/admin/index.html")
            print("=" * 70)
            
        else:
            print("\n❌ Admin user not found!")
            print("Creating new admin account...")
            
            # Create new admin
            new_password = 'admin123'
            hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt(rounds=12))
            
            new_admin = Admin(
                username='admin',
                password_hash=hashed.decode('utf-8'),
                email='admin@anshaircool.com',
                role='super_admin'
            )
            db.session.add(new_admin)
            db.session.commit()
            
            print("\n✅ New admin account created!")
            print("\n" + "=" * 70)
            print("LOGIN CREDENTIALS:")
            print("=" * 70)
            print("  Username: admin")
            print("  Password: admin123")
            print("=" * 70)
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTrying direct SQL reset...")
        
        try:
            # Direct SQL approach
            hashed = bcrypt.hashpw(b'admin123', bcrypt.gensalt(rounds=12)).decode('utf-8')
            
            db.session.execute(
                text("""
                    UPDATE admins 
                    SET password_hash = :hash, 
                        failed_login_attempts = 0, 
                        locked_until = NULL 
                    WHERE username = 'admin'
                """),
                {'hash': hashed}
            )
            db.session.commit()
            
            print("\n✅ SUCCESS! Password reset via SQL!")
            print("\n" + "=" * 70)
            print("LOGIN CREDENTIALS:")
            print("=" * 70)
            print("  Username: admin")
            print("  Password: admin123")
            print("=" * 70)
            
        except Exception as e2:
            print(f"\n❌ SQL reset also failed: {e2}")

print("=" * 70)
