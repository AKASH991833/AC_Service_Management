"""
Database Migration Script - Production Updates
Applies critical schema improvements to existing database

Migrations:
1. Add soft delete columns to all main tables
2. Add unique constraints
3. Add indexes for performance
4. Add invoice status column with locking support
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'ac_service_billing'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': 'utf8mb4',
    'use_pure': True
}


def get_connection():
    """Get database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print(f"✅ Connected to database: {DB_CONFIG['database']}")
        return conn
    except Error as e:
        print(f"❌ Connection error: {e}")
        raise


def column_exists(cursor, table, column):
    """Check if column exists in table"""
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
    """, (DB_CONFIG['database'], table, column))
    return cursor.fetchone()[0] > 0


def constraint_exists(cursor, constraint_name):
    """Check if constraint exists"""
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.TABLE_CONSTRAINTS 
        WHERE CONSTRAINT_SCHEMA = %s AND CONSTRAINT_NAME = %s
    """, (DB_CONFIG['database'], constraint_name))
    return cursor.fetchone()[0] > 0


def index_exists(cursor, table, index_name):
    """Check if index exists"""
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.STATISTICS 
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND INDEX_NAME = %s
    """, (DB_CONFIG['database'], table, index_name))
    return cursor.fetchone()[0] > 0


def migrate_database():
    """Run all migrations"""
    print("=" * 80)
    print("  DATABASE MIGRATION - ANSH AIR COOL")
    print("=" * 80)
    print()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    migrations_applied = 0
    
    try:
        # =====================================================================
        # MIGRATION 1: Add soft delete columns
        # =====================================================================
        print("[1/5] Adding SOFT DELETE columns...")
        
        tables_with_soft_delete = [
            'customers', 'invoices', 'invoice_items', 'technicians',
            'services', 'products', 'amc_contracts', 'amc_units',
            'service_requests', 'contact_messages'
        ]
        
        for table in tables_with_soft_delete:
            if not column_exists(cursor, table, 'is_deleted'):
                cursor.execute(f"""
                    ALTER TABLE {table} 
                    ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE,
                    ADD COLUMN deleted_at TIMESTAMP NULL
                """)
                print(f"      ✅ Added soft delete to: {table}")
                migrations_applied += 1
            else:
                print(f"      ℹ️  Soft delete already exists: {table}")
        
        # =====================================================================
        # MIGRATION 2: Add unique constraints
        # =====================================================================
        print("\n[2/5] Adding UNIQUE constraints...")
        
        # Customer phone unique
        if not constraint_exists(cursor, 'uk_customer_phone'):
            cursor.execute("ALTER TABLE customers ADD CONSTRAINT uk_customer_phone UNIQUE (phone)")
            print("      ✅ Added UNIQUE constraint: customers.phone")
            migrations_applied += 1
        else:
            print("      ℹ️  UNIQUE already exists: customers.phone")
        
        # Invoice invoice_number unique
        if not constraint_exists(cursor, 'uk_invoice_number'):
            cursor.execute("ALTER TABLE invoices ADD CONSTRAINT uk_invoice_number UNIQUE (invoice_number)")
            print("      ✅ Added UNIQUE constraint: invoices.invoice_number")
            migrations_applied += 1
        else:
            print("      ℹ️  UNIQUE already exists: invoices.invoice_number")
        
        # =====================================================================
        # MIGRATION 3: Add performance indexes
        # =====================================================================
        print("\n[3/5] Adding PERFORMANCE INDEXES...")
        
        indexes_to_add = [
            ('customers', 'idx_phone', 'phone'),
            ('customers', 'idx_created_at', 'created_at'),
            ('invoices', 'idx_customer_id', 'customer_id'),
            ('invoices', 'idx_invoice_date', 'invoice_date'),
            ('invoices', 'idx_status', 'status'),
            ('service_requests', 'idx_customer_phone', 'customer_phone'),
            ('service_requests', 'idx_created_at', 'created_at'),
            ('contact_messages', 'idx_phone', 'phone'),
            ('contact_messages', 'idx_created_at', 'created_at'),
        ]
        
        for table, index_name, column in indexes_to_add:
            if not index_exists(cursor, table, index_name):
                cursor.execute(f"CREATE INDEX {index_name} ON {table} ({column})")
                print(f"      ✅ Created index: {table}.{index_name}")
                migrations_applied += 1
            else:
                print(f"      ℹ️  Index already exists: {table}.{index_name}")
        
        # =====================================================================
        # MIGRATION 4: Update invoice status column
        # =====================================================================
        print("\n[4/5] Updating INVOICE STATUS column...")
        
        if column_exists(cursor, 'invoices', 'status'):
            # Check if it's the right type
            cursor.execute("""
                SELECT COLUMN_TYPE FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND COLUMN_NAME = %s
            """, (DB_CONFIG['database'], 'invoices', 'status'))
            
            col_type = cursor.fetchone()[0]
            if 'enum' not in col_type.lower():
                cursor.execute("""
                    ALTER TABLE invoices 
                    MODIFY COLUMN status ENUM('draft', 'final', 'paid', 'cancelled') 
                    NOT NULL DEFAULT 'draft'
                """)
                print("      ✅ Updated invoice.status to ENUM type")
                migrations_applied += 1
            else:
                print("      ℹ️  Invoice status already ENUM type")
        else:
            cursor.execute("""
                ALTER TABLE invoices 
                ADD COLUMN status ENUM('draft', 'final', 'paid', 'cancelled') 
                NOT NULL DEFAULT 'draft'
            """)
            print("      ✅ Added invoice.status column")
            migrations_applied += 1
        
        # =====================================================================
        # MIGRATION 5: Add foreign keys
        # =====================================================================
        print("\n[5/5] Adding FOREIGN KEYS...")
        
        # Invoice -> Customer
        if not constraint_exists(cursor, 'fk_invoice_customer'):
            cursor.execute("""
                ALTER TABLE invoices 
                ADD CONSTRAINT fk_invoice_customer 
                FOREIGN KEY (customer_id) REFERENCES customers(id) 
                ON DELETE RESTRICT
            """)
            print("      ✅ Added FK: invoices.customer_id -> customers.id")
            migrations_applied += 1
        else:
            print("      ℹ️  FK already exists: invoices.customer_id")
        
        # Invoice Items -> Invoice
        if not constraint_exists(cursor, 'fk_invoice_item_invoice'):
            cursor.execute("""
                ALTER TABLE invoice_items 
                ADD CONSTRAINT fk_invoice_item_invoice 
                FOREIGN KEY (invoice_id) REFERENCES invoices(id) 
                ON DELETE CASCADE
            """)
            print("      ✅ Added FK: invoice_items.invoice_id -> invoices.id")
            migrations_applied += 1
        else:
            print("      ℹ️  FK already exists: invoice_items.invoice_id")
        
        # =====================================================================
        # SUMMARY
        # =====================================================================
        print("\n" + "=" * 80)
        print(f"  ✅ MIGRATION COMPLETE!")
        print("=" * 80)
        print(f"\n📊 Migrations Applied: {migrations_applied}")
        print("\n📋 Changes Summary:")
        print("   • Soft delete support added to all main tables")
        print("   • UNIQUE constraints on customer.phone and invoice.invoice_number")
        print("   • Performance indexes on frequently queried columns")
        print("   • Invoice status ENUM with locking support")
        print("   • Foreign keys for referential integrity")
        
        print("\n🔒 Invoice Locking Rules:")
        print("   • 'draft' invoices: Can be edited/deleted")
        print("   • 'final' invoices: Can be edited (not paid yet)")
        print("   • 'paid' invoices: LOCKED - Read-only")
        print("   • 'cancelled' invoices: LOCKED - Read-only")
        
        print("\n" + "=" * 80)
        
        conn.commit()
        
    except Error as e:
        conn.rollback()
        print(f"\n❌ MIGRATION ERROR: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    try:
        migrate_database()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
