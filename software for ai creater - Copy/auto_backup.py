"""
Auto Backup Script for Ansh Air Cool Billing Software
Automatic database backup with cleanup of old backups
"""
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Fix UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration - Use project-relative path
BACKUP_DIR = Path(__file__).parent / "backups"
DATABASE_NAME = "ac_service_billing"

# Use environment variables with proper defaults
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Akash@9918')  # Fallback to default if not set
DB_HOST = os.getenv('DB_HOST', 'localhost')
KEEP_DAYS = 30  # Keep backups for 30 days

def create_backup_directory():
    """Create backup directory if it doesn't exist"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[OK] Backup directory: {BACKUP_DIR}")

def take_backup():
    """Take MySQL database backup using Python"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{DATABASE_NAME}_{timestamp}.sql"
    backup_path = BACKUP_DIR / backup_filename
    
    print(f"\n{'='*60}")
    print(f"  BACKING UP DATABASE: {DATABASE_NAME}")
    print(f"{'='*60}")
    print(f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Backup File: {backup_filename}")
    
    try:
        import mysql.connector
        
        # Connect to database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DATABASE_NAME
        )
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        backup_sql = []
        backup_sql.append(f"-- Ansh Air Cool Database Backup")
        backup_sql.append(f"-- Database: {DATABASE_NAME}")
        backup_sql.append(f"-- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        backup_sql.append(f"-- Host: {DB_HOST}")
        backup_sql.append("")
        backup_sql.append("SET FOREIGN_KEY_CHECKS=0;")
        backup_sql.append("")
        
        for table_tuple in tables:
            table = table_tuple[0]
            print(f"  Backing up table: {table}...")
            
            # Add DROP TABLE
            backup_sql.append(f"DROP TABLE IF EXISTS `{table}`;")
            
            # Get CREATE TABLE statement
            cursor.execute(f"SHOW CREATE TABLE `{table}`")
            create_stmt = cursor.fetchone()[1]
            backup_sql.append(create_stmt + ";")
            backup_sql.append("")
            
            # Get all data
            cursor.execute(f"SELECT * FROM `{table}`")
            rows = cursor.fetchall()
            
            if rows:
                # Get column names
                columns = [desc[0] for desc in cursor.description]
                
                # Insert statements
                for row in rows:
                    values = []
                    for val in row:
                        if val is None:
                            values.append("NULL")
                        elif isinstance(val, str):
                            escaped = val.replace("'", "''")
                            values.append(f"'{escaped}'")
                        elif isinstance(val, datetime):
                            values.append(f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'")
                        else:
                            values.append(str(val))
                    
                    backup_sql.append(f"INSERT INTO `{table}` ({', '.join(columns)}) VALUES ({', '.join(values)});")
                
                backup_sql.append("")
                print(f"  [OK] {table}: {len(rows)} rows backed up")
        
        backup_sql.append("SET FOREIGN_KEY_CHECKS=1;")
        
        # Write to file
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(backup_sql))
        
        cursor.close()
        conn.close()
        
        # Get file size
        file_size = backup_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"\n  [OK] Backup completed successfully!")
        print(f"  [OK] File size: {file_size_mb:.2f} MB")
        
        return True, backup_path
        
    except Exception as e:
        print(f"  [ERROR] Error: {str(e)}")
        return False, None

def cleanup_old_backups():
    """Delete backups older than KEEP_DAYS"""
    print(f"\n{'='*60}")
    print(f"  CLEANING UP OLD BACKUPS (Keeping last {KEEP_DAYS} days)")
    print(f"{'='*60}")
    
    if not BACKUP_DIR.exists():
        print("  No backup directory found")
        return 0
    
    deleted_count = 0
    cutoff_date = datetime.now().timestamp() - (KEEP_DAYS * 24 * 60 * 60)
    
    for backup_file in BACKUP_DIR.glob("*.sql"):
        file_time = backup_file.stat().st_mtime
        
        if file_time < cutoff_date:
            try:
                file_size = backup_file.stat().st_size / (1024 * 1024)
                backup_file.unlink()
                print(f"  [OK] Deleted: {backup_file.name} ({file_size:.2f} MB)")
                deleted_count += 1
            except Exception as e:
                print(f"  [ERROR] Error deleting {backup_file.name}: {e}")
    
    if deleted_count == 0:
        print(f"  [OK] No old backups to delete")
    
    print(f"  Total deleted: {deleted_count} files")
    return deleted_count

def list_existing_backups():
    """List all existing backups"""
    print(f"\n{'='*60}")
    print(f"  EXISTING BACKUPS")
    print(f"{'='*60}")
    
    if not BACKUP_DIR.exists():
        print("  No backup directory found")
        return
    
    backups = sorted(BACKUP_DIR.glob("*.sql"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not backups:
        print("  No backups found")
        return
    
    print(f"  {'Filename':<50} {'Size':<15} {'Date'}")
    print(f"  {'-'*50} {'-'*15} {'-'*20}")
    
    for i, backup in enumerate(backups[:10], 1):  # Show last 10 backups
        size_mb = backup.stat().st_size / (1024 * 1024)
        date_str = datetime.fromtimestamp(backup.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        print(f"  {i:2}. {backup.name:<50} {size_mb:>10.2f} MB  {date_str}")
    
    if len(backups) > 10:
        print(f"  ... and {len(backups) - 10} more backups")
    
    total_size = sum(b.stat().st_size for b in backups) / (1024 * 1024)
    print(f"\n  Total: {len(backups)} backups, {total_size:.2f} MB")

def main():
    """Main backup function"""
    print("\n" + "="*60)
    print("  ANSH AIR COOL - AUTO BACKUP SYSTEM")
    print("="*60)
    
    # Create backup directory
    create_backup_directory()
    
    # Take backup
    success, backup_path = take_backup()
    
    # Cleanup old backups
    cleanup_old_backups()
    
    # List existing backups
    list_existing_backups()
    
    # Summary
    print(f"\n{'='*60}")
    print(f"  BACKUP SUMMARY")
    print(f"{'='*60}")
    
    if success:
        print(f"  [OK] Status: SUCCESS")
        print(f"  [OK] Backup saved at: {backup_path}")
        print(f"  [OK] Keep for: {KEEP_DAYS} days")
    else:
        print(f"  [ERROR] Status: FAILED")
        print(f"  [ERROR] Please check error messages above")
    
    print(f"\n{'='*60}\n")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
