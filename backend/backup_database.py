"""
Database Backup Script
Creates automated MySQL database backups
Stores backups in backups/ folder with timestamps

Usage:
    python backup_database.py
    
Schedule (Windows Task Scheduler):
    Daily at 2:00 AM: python D:\Full_ac_website\backend\backup_database.py
"""

import os
import sys
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Configuration
BACKUP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups')
RETENTION_DAYS = 30  # Keep backups for 30 days

# Database configuration from .env
DATABASE_URL = os.getenv('DATABASE_URL', '')

def parse_database_url(url):
    """
    Parse MySQL database URL
    
    Format: mysql+pymysql://username:password@host:port/database_name
    
    Returns:
        dict: Database connection details
    """
    pattern = r'mysql\+pymysql://([^:]+):([^@]+)@([^:/]+):?(\d*)/([^?]+)'
    match = re.match(pattern, url)
    
    if not match:
        # Try without port
        pattern_simple = r'mysql+pymysql://([^:]+):([^@]+)@([^/]+)/([^?]+)'
        match = re.match(pattern_simple, url)
        if match:
            return {
                'user': match.group(1),
                'password': match.group(2),
                'host': match.group(3),
                'port': '3306',
                'database': match.group(4)
            }
        return None
    
    return {
        'user': match.group(1),
        'password': match.group(2),
        'host': match.group(3),
        'port': match.group(4) or '3306',
        'database': match.group(5)
    }


def create_backup_directory():
    """Create backup directory if it doesn't exist"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    print(f"✓ Backup directory: {BACKUP_DIR}")


def backup_database():
    """
    Create database backup using mysqldump
    
    Returns:
        tuple: (success: bool, message: str, filepath: str)
    """
    print("=" * 60)
    print("DATABASE BACKUP")
    print("=" * 60)
    
    # Parse database URL
    db_config = parse_database_url(DATABASE_URL)
    
    if not db_config:
        error_msg = "Failed to parse DATABASE_URL. Check .env file"
        print(f"✗ ERROR: {error_msg}")
        return False, error_msg, None
    
    database = db_config['database']
    user = db_config['user']
    password = db_config['password']
    host = db_config['host']
    port = db_config['port']
    
    print(f"Database: {database}")
    print(f"Host: {host}:{port}")
    print(f"User: {user}")
    print()
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"{database}_backup_{timestamp}.sql"
    backup_filepath = os.path.join(BACKUP_DIR, backup_filename)
    
    # Create backup directory
    create_backup_directory()
    
    # Build mysqldump command
    # Note: Using --set-gtid-purged=OFF for compatibility
    mysqldump_cmd = [
        'mysqldump',
        f'--host={host}',
        f'--port={port}',
        f'--user={user}',
        f'--password={password}',
        '--set-gtid-purged=OFF',
        '--single-transaction',
        '--quick',
        '--lock-tables=false',
        '--routines',
        '--triggers',
        '--events',
        database
    ]
    
    print(f"Starting backup...")
    print(f"Output file: {backup_filename}")
    print()
    
    try:
        # Execute mysqldump
        with open(backup_filepath, 'w', encoding='utf-8') as f:
            process = subprocess.Popen(
                mysqldump_cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode('utf-8', errors='ignore') if stderr else f"mysqldump exited with code {process.returncode}"
                print(f"✗ ERROR: mysqldump failed")
                print(f"  Details: {error_msg}")
                return False, f"mysqldump failed: {error_msg}", None
        
        # Check if file was created and has content
        if not os.path.exists(backup_filepath):
            error_msg = "Backup file was not created"
            print(f"✗ ERROR: {error_msg}")
            return False, error_msg, None
        
        file_size = os.path.getsize(backup_filepath)
        if file_size == 0:
            error_msg = "Backup file is empty"
            print(f"✗ ERROR: {error_msg}")
            os.remove(backup_filepath)  # Clean up empty file
            return False, error_msg, None
        
        # Get file size
        file_size_mb = file_size / 1024 / 1024
        
        print(f"✓ Backup completed successfully!")
        print(f"  File: {backup_filename}")
        print(f"  Size: {file_size_mb:.2f} MB")
        print()
        
        return True, "Backup completed successfully", backup_filepath
        
    except FileNotFoundError as e:
        error_msg = "mysqldump not found. Please install MySQL or MariaDB"
        print(f"✗ ERROR: {error_msg}")
        print(f"  Details: {str(e)}")
        return False, error_msg, None
    except PermissionError as e:
        error_msg = f"Permission denied: {str(e)}"
        print(f"✗ ERROR: {error_msg}")
        return False, error_msg, None
    except Exception as e:
        error_msg = f"Backup failed: {str(e)}"
        print(f"✗ ERROR: {error_msg}")
        import traceback
        print(f"  Details: {traceback.format_exc()}")
        return False, error_msg, None


def cleanup_old_backups():
    """Remove backups older than RETENTION_DAYS"""
    print("Cleaning up old backups...")
    
    if not os.path.exists(BACKUP_DIR):
        print("  No backup directory found")
        return
    
    deleted_count = 0
    current_time = datetime.now()
    
    for filename in os.listdir(BACKUP_DIR):
        if not filename.endswith('.sql'):
            continue
        
        filepath = os.path.join(BACKUP_DIR, filename)
        file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        age_days = (current_time - file_mtime).days
        
        if age_days > RETENTION_DAYS:
            try:
                os.remove(filepath)
                print(f"  Deleted: {filename} ({age_days} days old)")
                deleted_count += 1
            except Exception as e:
                print(f"  Error deleting {filename}: {str(e)}")
    
    if deleted_count == 0:
        print("  No old backups to delete")
    else:
        print(f"  Deleted {deleted_count} old backup(s)")
    
    print()


def list_backups():
    """List all existing backups"""
    print("Existing backups:")
    print("-" * 60)
    
    if not os.path.exists(BACKUP_DIR):
        print("  No backup directory found")
        return
    
    backups = []
    for filename in sorted(os.listdir(BACKUP_DIR)):
        if filename.endswith('.sql'):
            filepath = os.path.join(BACKUP_DIR, filename)
            size = os.path.getsize(filepath)
            size_mb = size / 1024 / 1024
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            backups.append({
                'filename': filename,
                'size_mb': size_mb,
                'date': mtime
            })
    
    if not backups:
        print("  No backups found")
        return
    
    for backup in backups:
        print(f"  {backup['filename']}")
        print(f"    Size: {backup['size_mb']:.2f} MB")
        print(f"    Date: {backup['date'].strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    print(f"Total: {len(backups)} backup(s)")
    print()


def main():
    """Main function"""
    # Fix Unicode encoding for Windows console
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'list':
            list_backups()
            return
        elif command == 'help':
            print("Database Backup Script")
            print()
            print("Usage:")
            print("  python backup_database.py        - Create new backup")
            print("  python backup_database.py list   - List existing backups")
            print("  python backup_database.py help   - Show this help")
            print()
            return
    
    # Create backup
    success, message, filepath = backup_database()
    
    if success:
        # Cleanup old backups
        cleanup_old_backups()
        
        print("=" * 60)
        print("BACKUP SUMMARY")
        print("=" * 60)
        print(f"Status: ✓ SUCCESS")
        print(f"File: {os.path.basename(filepath)}")
        print(f"Location: {BACKUP_DIR}")
        print()
        print("Next steps:")
        print("  • Verify backup file exists")
        print("  • Consider copying to external storage")
        print("  • Old backups (>30 days) have been deleted")
        print("=" * 60)
        sys.exit(0)
    else:
        print("=" * 60)
        print("BACKUP FAILED")
        print("=" * 60)
        print(f"Status: ✗ FAILED")
        print(f"Error: {message}")
        print()
        print("Troubleshooting:")
        print("  1. Check MySQL/MariaDB is installed")
        print("  2. Verify mysqldump is in PATH")
        print("  3. Check DATABASE_URL in .env file")
        print("  4. Ensure database server is running")
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    main()
