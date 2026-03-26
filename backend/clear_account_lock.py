"""
TEMPORARY: Disable Account Lock for Testing
Run this to clear all locks
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Clear the locked accounts in security module
import security

print("=" * 70)
print("CLEARING ACCOUNT LOCKS")
print("=" * 70)

# Clear all locked accounts
security.locked_accounts.clear()
security.login_attempts.clear()

print("\n✅ All account locks cleared!")
print("\n" + "=" * 70)
print("NOW YOU CAN LOGIN!")
print("=" * 70)
print("  URL: http://localhost:5500/admin/index.html")
print("  Username: admin")
print("  Password: admin123")
print("=" * 70)
