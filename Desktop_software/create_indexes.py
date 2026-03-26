"""
Database Index Migration - Performance Optimization
Adds critical indexes to improve query performance
Run this once to optimize database queries
SECURITY: All credentials loaded from environment variables only
"""
import mysql.connector
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from Desktop_software/.env
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / '.env')

# ============================================================================
# SECURE DATABASE CONFIGURATION - NO HARDCODED VALUES
# ============================================================================
def get_database_config():
    """Get database configuration from environment variables"""
    db_password = os.getenv('DB_PASSWORD')
    
    if not db_password or db_password.strip() == '':
        print("\n" + "="*80)
        print("🔒 SECURITY ERROR: DB_PASSWORD environment variable not set!")
        print("="*80)
        print("\nPlease create .env file in Desktop_software directory:")
        print("  DB_PASSWORD=your_secure_password")
        print("  DB_USER=root")
        print("  DB_HOST=localhost")
        print("  DB_NAME=ac_service_billing")
        print("="*80 + "\n")
        sys.exit(1)
    
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': db_password,
        'database': os.getenv('DB_NAME', 'ac_service_billing'),
        'port': int(os.getenv('DB_PORT', '3306')),
    }

# Load secure configuration
DB_CONFIG = get_database_config()
# ============================================================================


def get_connection():
    """Get database connection"""
    return mysql.connector.connect(**DB_CONFIG)


def create_indexes():
    """Create performance indexes - comprehensive optimization"""
    print("=" * 80)
    print("DATABASE INDEX MIGRATION - PERFORMANCE OPTIMIZATION")
    print("=" * 80)

    conn = get_connection()
    cursor = conn.cursor()

    indexes = [
        # =====================================================================
        # USERS TABLE - Authentication & Profile
        # =====================================================================
        ("users", "idx_username", "CREATE INDEX idx_username ON users(username)"),
        ("users", "idx_email", "CREATE INDEX idx_email ON users(email)"),
        ("users", "idx_is_active", "CREATE INDEX idx_is_active ON users(is_active)"),
        ("users", "idx_created_at", "CREATE INDEX idx_created_at ON users(created_at)"),

        # =====================================================================
        # CUSTOMERS TABLE - Search & Lookup
        # =====================================================================
        ("customers", "idx_mobile", "CREATE INDEX idx_mobile ON customers(mobile)"),
        ("customers", "idx_name", "CREATE INDEX idx_name ON customers(name)"),
        ("customers", "idx_is_active_cust", "CREATE INDEX idx_is_active_cust ON customers(is_active)"),
        ("customers", "idx_email_cust", "CREATE INDEX idx_email_cust ON customers(email)"),
        ("customers", "idx_city", "CREATE INDEX idx_city ON customers(city)"),

        # =====================================================================
        # INVOICES TABLE - Billing & Reports
        # =====================================================================
        ("invoices", "idx_invoice_number", "CREATE INDEX idx_invoice_number ON invoices(invoice_number)"),
        ("invoices", "idx_customer_id", "CREATE INDEX idx_customer_id ON invoices(customer_id)"),
        ("invoices", "idx_created_at", "CREATE INDEX idx_created_at ON invoices(created_at)"),
        ("invoices", "idx_payment_status", "CREATE INDEX idx_payment_status ON invoices(payment_status)"),
        ("invoices", "idx_technician_id", "CREATE INDEX idx_technician_id ON invoices(technician_id)"),
        ("invoices", "idx_is_active_inv", "CREATE INDEX idx_is_active_inv ON invoices(is_active)"),
        ("invoices", "idx_total_amount", "CREATE INDEX idx_total_amount ON invoices(total_amount)"),
        ("invoices", "idx_due_date", "CREATE INDEX idx_due_date ON invoices(due_date)"),

        # =====================================================================
        # AMC CONTRACTS TABLE - Annual Maintenance
        # =====================================================================
        ("amc_contracts", "idx_contract_number", "CREATE INDEX idx_contract_number ON amc_contracts(contract_number)"),
        ("amc_contracts", "idx_customer_id_amc", "CREATE INDEX idx_customer_id_amc ON amc_contracts(customer_id)"),
        ("amc_contracts", "idx_status", "CREATE INDEX idx_status ON amc_contracts(status)"),
        ("amc_contracts", "idx_next_visit_date", "CREATE INDEX idx_next_visit_date ON amc_contracts(next_visit_date)"),
        ("amc_contracts", "idx_created_at_amc", "CREATE INDEX idx_created_at_amc ON amc_contracts(created_at)"),

        # =====================================================================
        # TECHNICIANS TABLE - Service Assignment
        # =====================================================================
        ("technicians", "idx_mobile_tech", "CREATE INDEX idx_mobile_tech ON technicians(mobile)"),
        ("technicians", "idx_is_active_tech", "CREATE INDEX idx_is_active_tech ON technicians(is_active)"),
        ("technicians", "idx_name_tech", "CREATE INDEX idx_name_tech ON technicians(name)"),

        # =====================================================================
        # SERVICE REQUESTS TABLE - Online Requests
        # =====================================================================
        ("service_requests", "idx_customer_phone", "CREATE INDEX idx_customer_phone ON service_requests(customer_phone)"),
        ("service_requests", "idx_request_status", "CREATE INDEX idx_request_status ON service_requests(request_status)"),
        ("service_requests", "idx_created_at_req", "CREATE INDEX idx_created_at_req ON service_requests(created_at)"),
        ("service_requests", "idx_service_type", "CREATE INDEX idx_service_type ON service_requests(service_type)"),
        ("service_requests", "idx_assigned_to", "CREATE INDEX idx_assigned_to ON service_requests(assigned_to)"),

        # =====================================================================
        # CONTACT MESSAGES TABLE - Website Inquiries
        # =====================================================================
        ("contact_messages", "idx_phone_contact", "CREATE INDEX idx_phone_contact ON contact_messages(phone)"),
        ("contact_messages", "idx_status_contact", "CREATE INDEX idx_status_contact ON contact_messages(status)"),
        ("contact_messages", "idx_created_at_contact", "CREATE INDEX idx_created_at_contact ON contact_messages(created_at)"),

        # =====================================================================
        # INVOICE ITEMS TABLE - Line Items
        # =====================================================================
        ("invoice_items", "idx_invoice_id_item", "CREATE INDEX idx_invoice_id_item ON invoice_items(invoice_id)"),
        ("invoice_items", "idx_service_id", "CREATE INDEX idx_service_id ON invoice_items(service_id)"),
        ("invoice_items", "idx_part_id", "CREATE INDEX idx_part_id ON invoice_items(part_id)"),

        # =====================================================================
        # AMC VISITS TABLE - Scheduled Visits
        # =====================================================================
        ("amc_visits", "idx_contract_id", "CREATE INDEX idx_contract_id ON amc_visits(contract_id)"),
        ("amc_visits", "idx_visit_date", "CREATE INDEX idx_visit_date ON amc_visits(visit_date)"),
        ("amc_visits", "idx_status_visit", "CREATE INDEX idx_status_visit ON amc_visits(status)"),

        # =====================================================================
        # SERVICES & PARTS TABLES - Catalog
        # =====================================================================
        ("services", "idx_service_name", "CREATE INDEX idx_service_name ON services(service_name)"),
        ("services", "idx_is_active_svc", "CREATE INDEX idx_is_active_svc ON services(is_active)"),
        ("parts", "idx_part_name", "CREATE INDEX idx_part_name ON parts(part_name)"),
        ("parts", "idx_is_active_part", "CREATE INDEX idx_is_active_part ON parts(is_active)"),

        # =====================================================================
        # COMPOSITE INDEXES - Multi-column queries
        # =====================================================================
        ("invoices", "idx_customer_status", "CREATE INDEX idx_customer_status ON invoices(customer_id, payment_status)"),
        ("invoices", "idx_status_date", "CREATE INDEX idx_status_date ON invoices(payment_status, created_at)"),
        ("invoices", "idx_customer_date", "CREATE INDEX idx_customer_date ON invoices(customer_id, created_at)"),
        ("amc_contracts", "idx_status_date_amc", "CREATE INDEX idx_status_date_amc ON amc_contracts(status, next_visit_date)"),
        ("service_requests", "idx_status_created", "CREATE INDEX idx_status_created ON service_requests(request_status, created_at)"),
        ("customers", "idx_name_mobile", "CREATE INDEX idx_name_mobile ON customers(name, mobile)"),
    ]
    
    created = 0
    skipped = 0
    errors = 0
    
    for table, index_name, create_sql in indexes:
        try:
            # Check if index already exists
            check_query = """
            SELECT COUNT(*) as count
            FROM information_schema.statistics
            WHERE table_schema = %s AND table_name = %s AND index_name = %s
            """
            cursor.execute(check_query, (DB_CONFIG['database'], table, index_name))
            result = cursor.fetchone()
            
            if result[0] > 0:
                print(f"⚠️  Index {index_name} already exists on {table}")
                skipped += 1
                continue
            
            # Create index
            cursor.execute(create_sql)
            conn.commit()
            print(f"✅ Created index {index_name} on {table}")
            created += 1
            
        except mysql.connector.Error as e:
            print(f"❌ Error creating index {index_name} on {table}: {e}")
            errors += 1
            if 'Duplicate key name' in str(e):
                skipped += 1
                errors -= 1
    
    cursor.close()
    conn.close()

    print("\n" + "=" * 80)
    print("MIGRATION SUMMARY")
    print("=" * 80)
    print(f"✅ Indexes Created: {created}")
    print(f"⚠️  Already Exists: {skipped}")
    print(f"❌ Errors: {errors}")
    print("=" * 80)

    if errors == 0:
        print("\n🎉 Database optimization completed successfully!")
        print("\n📈 Performance improvements:")
        print("  ✅ Faster customer lookups by mobile number, name, email")
        print("  ✅ Quicker invoice searches by number, date, customer, status")
        print("  ✅ Improved AMC contract queries by status and visit date")
        print("  ✅ Better service request filtering by status and type")
        print("  ✅ Optimized join operations with composite indexes")
        print("  ✅ Faster technician and service/part lookups")
        print("  ✅ Improved contact message tracking")
        print("\n⚡ Expected query speedup: 10-100x for large tables")
    else:
        print(f"\n⚠️  Completed with {errors} errors. Check logs for details.")

    return created, skipped, errors


if __name__ == "__main__":
    try:
        print("\n🚀 Starting database index optimization...")
        print("This may take a few moments depending on data size.\n")
        
        created, skipped, errors = create_indexes()
        
        sys.exit(0 if errors == 0 else 1)
        
    except mysql.connector.Error as e:
        print(f"\n❌ Database connection error: {e}")
        print("\nPlease ensure:")
        print("  1. MySQL server is running")
        print("  2. Database credentials in .env are correct")
        print("  3. Database 'ac_service_billing' exists")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
