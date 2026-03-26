"""
Setup Script - Create required directories and verify dependencies
Run this once after deployment: python setup_system.py
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_directory(path, description):
    """Create directory if it doesn't exist"""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"✓ Created: {path} ({description})")
        return True
    except Exception as e:
        print(f"✗ Failed to create {path}: {str(e)}")
        return False

def check_dependency(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ Installed: {package_name}")
        return True
    except ImportError:
        print(f"✗ Missing: {package_name} - Run: pip install {package_name}")
        return False

def main():
    print("=" * 60)
    print("ANSH AIR COOL - SYSTEM SETUP")
    print("=" * 60)
    print()
    
    # Create required directories
    print("Creating required directories...")
    print("-" * 60)
    
    directories = [
        (os.path.join(PROJECT_ROOT, 'logs'), 'Application logs'),
        (os.path.join(PROJECT_ROOT, 'backups'), 'Database backups'),
        (os.path.join(PROJECT_ROOT, 'uploads'), 'User uploads'),
        (os.path.join(PROJECT_ROOT, 'uploads', 'gallery'), 'Gallery images'),
        (os.path.join(PROJECT_ROOT, 'uploads', 'products'), 'Product images'),
        (os.path.join(PROJECT_ROOT, 'uploads', 'website'), 'Website images'),
    ]
    
    all_dirs_ok = True
    for path, description in directories:
        if not create_directory(path, description):
            all_dirs_ok = False
    
    print()
    
    # Check Python dependencies
    print("Checking Python dependencies...")
    print("-" * 60)
    
    dependencies = [
        ('Flask', 'flask'),
        ('Flask-SQLAlchemy', 'flask_sqlalchemy'),
        ('Flask-Limiter', 'flask_limiter'),
        ('Flask-CORS', 'flask_cors'),
        ('PyMySQL', 'pymysql'),
        ('bcrypt', 'bcrypt'),
        ('Pillow', 'PIL'),
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv'),
    ]
    
    all_deps_ok = True
    for package, import_name in dependencies:
        if not check_dependency(package, import_name):
            all_deps_ok = False
    
    print()
    
    # Summary
    print("=" * 60)
    print("SETUP SUMMARY")
    print("=" * 60)
    
    if all_dirs_ok and all_deps_ok:
        print("✓ All directories created successfully")
        print("✓ All dependencies installed")
        print()
        print("Next steps:")
        print("  1. Run: python migrate_indexes.py")
        print("  2. Test: python main.py")
        print("  3. Open: http://localhost:5000/health")
        sys.exit(0)
    else:
        if not all_dirs_ok:
            print("✗ Some directories failed to create")
        if not all_deps_ok:
            print("✗ Some dependencies are missing")
            print()
            print("Install missing dependencies:")
            print("  pip install -r requirements.txt")
        sys.exit(1)

if __name__ == '__main__':
    # Fix Unicode encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    main()
