"""
Configuration settings for AC Service Billing Software
Production-ready with secure environment variable handling
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Base directory
BASE_DIR = Path(__file__).parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# ============================================================================
# DATABASE CONFIGURATION - SECURE & STANDARDIZED
# ============================================================================
# CRITICAL: All database credentials MUST be set via environment variables
# NO hardcoded fallbacks for security reasons
# ============================================================================

def validate_database_config():
    """Validate all required database configuration"""
    errors = []
    warnings = []
    
    # Required variables
    db_password = os.getenv('DB_PASSWORD')
    db_user = os.getenv('DB_USER', 'root')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME', 'ac_service_billing')
    db_port = os.getenv('DB_PORT', '3306')
    
    # Check DB_PASSWORD
    if db_password is None or db_password.strip() == '':
        errors.append("DB_PASSWORD environment variable is not set")
    
    # Check for weak passwords
    if db_password and len(db_password) < 8:
        warnings.append("DB_PASSWORD is less than 8 characters - consider using a stronger password")
    
    # Print warnings
    for warning in warnings:
        print(f"\n⚠️  WARNING: {warning}")
    
    # Print errors and exit if any
    if errors:
        print("\n" + "="*80)
        print("🔒 SECURITY ERROR: Database Configuration Incomplete")
        print("="*80)
        for error in errors:
            print(f"  ❌ {error}")
        print("\n" + "="*80)
        print("📋 SETUP INSTRUCTIONS:")
        print("="*80)
        print("\n1. Create/Edit .env file in Desktop_software directory:")
        print("   DB_PASSWORD=your_secure_password")
        print("   DB_USER=root")
        print("   DB_HOST=localhost")
        print("   DB_NAME=ac_service_billing")
        print("   DB_PORT=3306")
        print("\n2. Or set via system environment variable:")
        print("   Windows: setx DB_PASSWORD \"your_secure_password\"")
        print("   Linux/Mac: export DB_PASSWORD=\"your_secure_password\"")
        print("\n3. Restart the application after setting variables")
        print("="*80 + "\n")
        sys.exit(1)
    
    return {
        'password': db_password,
        'user': db_user,
        'host': db_host,
        'name': db_name,
        'port': int(db_port)
    }

# Validate and get database configuration
db_config = validate_database_config()

DB_CONFIG = {
    'host': db_config['host'],
    'user': db_config['user'],
    'password': db_config['password'],  # Secure - no fallback
    'database': db_config['name'],
    'port': db_config['port'],
    'charset': 'utf8mb4',
    'use_pure': True,  # Use Pure Python for better compatibility
    'use_unicode': True,
    'connection_timeout': 60,  # Increased timeout for stability
    'autocommit': True,
    'pool_name': 'ac_service_pool',
    'pool_size': 5,  # Connection pooling for better performance
    'pool_reset_session': True,
    'ssl_disabled': True,  # Disable SSL for local connections
    'ssl_verify_cert': False,  # Don't verify SSL certificate
    'ssl_verify_identity': False
}

# Database name constant for consistency
DATABASE_NAME = DB_CONFIG['database']

# Application settings
APP_NAME = "Ansh Air Cool - Billing System"
APP_VERSION = "1.0.0"
COMPANY_NAME = "Ansh Air Cool"

# Invoice settings
INVOICE_PREFIX = "INV"
INVOICE_START_NUMBER = 1001
GST_PERCENTAGE = 18.0

# File paths
LOGO_PATH = BASE_DIR / "assets" / "logo.png"
INVOICE_TEMPLATE_PATH = BASE_DIR / "assets" / "invoice_template.pdf"
EXPORT_DIR = BASE_DIR / "exports"
PDF_DIR = BASE_DIR / "pdfs"

# Create necessary directories
for directory in [EXPORT_DIR, PDF_DIR]:
    directory.mkdir(exist_ok=True)

# UI Settings - DARK THEME ONLY
COLORS = {
    'dark': {
        'bg': '#0f172a',           # Deep navy-slate background
        'fg': '#f1f5f9',           # Bright light gray for contrast
        'primary': '#22d3ee',      # Vibrant cyan for dark mode
        'primary_hover': '#67e8f9', # Bright cyan hover for dark mode
        'secondary': '#94a3b8',    # Light gray for secondary elements
        'success': '#34d399',      # Bright green for success
        'warning': '#fbbf24',      # Golden amber for warnings
        'danger': '#f87171',       # Soft red for errors
        'card_bg': '#1e293b',      # Slate card background
        'border': '#334155',       # Medium slate borders
        'hover': '#334155',        # Hover state highlight
        'alt_row': '#162032',      # Alternate row background (darker than card_bg)
        'sidebar': '#020617',      # Darker sidebar for depth
        'header': '#0e7490',       # Deep cyan header
        'accent': '#22d3ee',       # Bright cyan accent
        'muted': '#64748b'         # Muted gray for secondary text
    }
}

# Font settings - ENHANCED TYPOGRAPHY
FONTS = {
    'small': ('Segoe UI', 9),
    'normal': ('Segoe UI', 10),
    'medium': ('Segoe UI', 11),
    'large': ('Segoe UI', 12),
    'heading': ('Segoe UI', 14, 'bold'),
    'title': ('Segoe UI', 18, 'bold'),
    'display': ('Segoe UI', 24, 'bold'),
    'button': ('Segoe UI', 10, 'bold'),
    'label': ('Segoe UI', 10, 'bold'),
    'data': ('Segoe UI', 10),
    'body': ('Segoe UI', 10),                 # Standard body text
    'card_title': ('Segoe UI', 13, 'bold'),   # For card headers and section titles
    'metric_value': ('Segoe UI', 28, 'bold'), # For large numbers in metric cards
    'metric_label': ('Segoe UI', 11),         # For labels below metric values
    'table_header': ('Segoe UI', 11, 'bold'), # For treeview table headers
    'table_row': ('Segoe UI', 10),            # For treeview table rows
    'fab': ('Segoe UI', 20, 'bold'),          # For the Floating Action Button text
    'subheading': ('Segoe UI', 14),           # For date and revenue trend summary
}