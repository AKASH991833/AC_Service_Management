"""
Configuration settings for AC Service Billing Software
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
# DATABASE CONFIGURATION - SECURE
# ============================================================================
# CRITICAL: DB_PASSWORD MUST be set via environment variable or .env file
# No hardcoded fallback for security reasons
# ============================================================================

# Get password from environment - NO fallback
db_password = os.getenv('DB_PASSWORD')

# Validate DB_PASSWORD is set
if db_password is None or db_password.strip() == '':
    print("\n" + "="*70)
    print("SECURITY ERROR: DB_PASSWORD environment variable not set!")
    print("="*70)
    print("\nPlease set DB_PASSWORD using one of these methods:")
    print("\n1. Via .env file (RECOMMENDED):")
    print("   Create/Edit .env file in project root:")
    print("   DB_PASSWORD=your_secure_password")
    print("\n2. Via system environment variable:")
    print("   Windows: setx DB_PASSWORD \"your_secure_password\"")
    print("   Linux/Mac: export DB_PASSWORD=\"your_secure_password\"")
    print("\n3. Via command line:")
    print("   python -c \"import os; os.environ['DB_PASSWORD']='your_password'\"")
    print("="*70 + "\n")
    sys.exit(1)

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': db_password,  # Required - no fallback
    'database': os.getenv('DB_NAME', 'ac_service_billing'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'charset': 'utf8mb4',
    'use_pure': True,  # Pure Python driver for better compatibility
    'ssl_disabled': True,  # Disable SSL for local connections
    'ssl_verify_cert': False,  # Don't verify SSL certificate
    'connection_timeout': 60,  # Increased timeout for stability
    'autocommit': True,
    'pool_name': 'ac_service_pool',
    'pool_size': 5,  # Connection pooling for better performance
    'pool_reset_session': True
}

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