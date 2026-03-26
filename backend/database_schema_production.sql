-- ============================================================================
-- ANSH AIR COOL - PRODUCTION DATABASE SCHEMA
-- Database Name: ac_service_billing
-- Single Database for Flask Backend + Desktop Software (PySide6)
-- ============================================================================

-- Create database
CREATE DATABASE IF NOT EXISTS ac_service_billing
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ac_service_billing;

-- ============================================================================
# ADMINISTRATORS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    full_name VARCHAR(100),
    phone VARCHAR(15),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    
    INDEX idx_username (username),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# CUSTOMERS TABLE (CRM) - With SOFT DELETE
-- ============================================================================

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100),
    customer_type VARCHAR(50) DEFAULT 'Regular',
    address TEXT,
    city VARCHAR(100),
    pincode VARCHAR(10),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- SOFT DELETE SUPPORT
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    
    -- TIMESTAMPS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_name (name),
    INDEX idx_phone (phone),
    INDEX idx_email (email),
    INDEX idx_customer_type (customer_type),
    INDEX idx_is_active (is_active),
    INDEX idx_is_deleted (is_deleted),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# TECHNICIANS TABLE - With SOFT DELETE
-- ============================================================================

CREATE TABLE IF NOT EXISTS technicians (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    email VARCHAR(100),
    address TEXT,
    specialization VARCHAR(100),
    commission_rate DECIMAL(5,2) DEFAULT 10.00,
    is_active BOOLEAN DEFAULT TRUE,
    joined_date DATE,
    
    -- SOFT DELETE SUPPORT
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    
    -- TIMESTAMPS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_name (name),
    INDEX idx_phone (phone),
    INDEX idx_is_active (is_active),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# SERVICES TABLE - With SOFT DELETE
-- ============================================================================

CREATE TABLE IF NOT EXISTS services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    service_slug VARCHAR(100) UNIQUE NOT NULL,
    starting_price VARCHAR(50) NOT NULL,
    price_numeric INT,
    description TEXT,
    duration VARCHAR(50),
    icon_class VARCHAR(50),
    features TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    is_featured BOOLEAN DEFAULT FALSE,
    service_image VARCHAR(500),
    
    -- SOFT DELETE SUPPORT
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    
    -- TIMESTAMPS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_service_name (service_name),
    INDEX idx_service_slug (service_slug),
    INDEX idx_price_numeric (price_numeric),
    INDEX idx_is_active (is_active),
    INDEX idx_is_featured (is_featured),
    INDEX idx_display_order (display_order),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# PRODUCTS TABLE - With SOFT DELETE
-- ============================================================================

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_type VARCHAR(20) NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    brand VARCHAR(50),
    capacity VARCHAR(20),
    ac_type VARCHAR(20),
    star_rating INT DEFAULT 3,
    is_inverter BOOLEAN DEFAULT FALSE,
    price VARCHAR(50) NOT NULL,
    price_numeric INT,
    description TEXT,
    features TEXT,
    product_image VARCHAR(500),
    image_gallery TEXT,
    is_available BOOLEAN DEFAULT TRUE,
    stock_status VARCHAR(20) DEFAULT 'In Stock',
    rental_min_months INT,
    rental_deposit VARCHAR(50),
    rental_includes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    badge_text VARCHAR(50),
    
    -- SOFT DELETE SUPPORT
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    
    -- TIMESTAMPS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_product_type (product_type),
    INDEX idx_product_name (product_name),
    INDEX idx_brand (brand),
    INDEX idx_price_numeric (price_numeric),
    INDEX idx_is_available (is_available),
    INDEX idx_is_featured (is_featured),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# INVOICES TABLE - With STATUS LOCKING
-- Status: draft -> final -> paid (LOCKED) or cancelled (LOCKED)
-- ============================================================================

CREATE TABLE IF NOT EXISTS invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    invoice_date DATE NOT NULL,
    due_date DATE,
    ac_brand VARCHAR(100),
    ac_type VARCHAR(20),
    ac_model VARCHAR(100),
    subtotal DECIMAL(10,2) NOT NULL,
    discount DECIMAL(10,2) DEFAULT 0.00,
    tax_percentage DECIMAL(5,2) DEFAULT 18.00,
    tax_amount DECIMAL(10,2) DEFAULT 0.00,
    total_amount DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) DEFAULT 0.00,
    balance_amount DECIMAL(10,2) NOT NULL,
    
    -- INVOICE STATUS (CRITICAL FOR LOCKING)
    status ENUM('draft', 'final', 'paid', 'cancelled') NOT NULL DEFAULT 'draft',
    
    -- PAYMENT DETAILS
    payment_mode VARCHAR(20),
    
    -- NOTES
    notes TEXT,
    created_by INT,
    
    -- SOFT DELETE SUPPORT
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    
    -- TIMESTAMPS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- FOREIGN KEY
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT,
    
    -- INDEXES
    INDEX idx_invoice_number (invoice_number),
    INDEX idx_customer_id (customer_id),
    INDEX idx_invoice_date (invoice_date),
    INDEX idx_status (status),
    INDEX idx_paid_amount (paid_amount),
    INDEX idx_balance_amount (balance_amount),
    INDEX idx_is_deleted (is_deleted),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# INVOICE ITEMS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS invoice_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT NOT NULL,
    item_type VARCHAR(20) NOT NULL,
    service_id INT,
    part_id INT,
    description VARCHAR(500) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- FOREIGN KEY
    FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
    
    -- INDEXES
    INDEX idx_invoice_id (invoice_id),
    INDEX idx_item_type (item_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# AMC CONTRACTS TABLE - With SOFT DELETE
-- ============================================================================

CREATE TABLE IF NOT EXISTS amc_contracts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contract_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    paid_amount DECIMAL(10,2) DEFAULT 0.00,
    payment_frequency VARCHAR(20) DEFAULT 'yearly',
    status VARCHAR(20) DEFAULT 'active',
    notes TEXT,
    
    -- SOFT DELETE SUPPORT
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    
    -- TIMESTAMPS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- FOREIGN KEY
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE RESTRICT,
    
    -- INDEXES
    INDEX idx_contract_number (contract_number),
    INDEX idx_customer_id (customer_id),
    INDEX idx_start_date (start_date),
    INDEX idx_end_date (end_date),
    INDEX idx_status (status),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# AMC UNITS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS amc_units (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id INT NOT NULL,
    ac_brand VARCHAR(100) NOT NULL,
    ac_type VARCHAR(20),
    ac_model VARCHAR(100),
    serial_number VARCHAR(100),
    capacity_tonnage VARCHAR(10),
    installation_year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- FOREIGN KEY
    FOREIGN KEY (contract_id) REFERENCES amc_contracts(id) ON DELETE CASCADE,
    
    -- INDEXES
    INDEX idx_contract_id (contract_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# SERVICE REQUESTS TABLE - With SOFT DELETE
-- ============================================================================

CREATE TABLE IF NOT EXISTS service_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_phone VARCHAR(15) NOT NULL,
    customer_email VARCHAR(100),
    customer_address TEXT NOT NULL,
    service_type VARCHAR(50) NOT NULL,
    ac_type VARCHAR(20) DEFAULT 'Not Specified',
    preferred_date DATE,
    time_slot VARCHAR(20) DEFAULT 'Not Specified',
    message TEXT,
    request_status VARCHAR(20) DEFAULT 'Pending',
    assigned_technician_id INT,
    source VARCHAR(50) DEFAULT 'Website',
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- SOFT DELETE SUPPORT
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    
    -- TIMESTAMPS
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_customer_name (customer_name),
    INDEX idx_customer_phone (customer_phone),
    INDEX idx_customer_email (customer_email),
    INDEX idx_service_type (service_type),
    INDEX idx_request_status (request_status),
    INDEX idx_is_active (is_active),
    INDEX idx_is_deleted (is_deleted),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# CONTACT MESSAGES TABLE - With SOFT DELETE
-- ============================================================================

CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    address TEXT,
    service_type VARCHAR(50) NOT NULL,
    ac_type VARCHAR(20) DEFAULT 'Not Specified',
    message TEXT,
    status VARCHAR(20) DEFAULT 'unread',
    source VARCHAR(50) DEFAULT 'Website',
    ip_address VARCHAR(45),
    user_agent TEXT,
    
    -- SOFT DELETE SUPPORT
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL,
    
    -- TIMESTAMPS
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_name (name),
    INDEX idx_phone (phone),
    INDEX idx_email (email),
    INDEX idx_service_type (service_type),
    INDEX idx_status (status),
    INDEX idx_is_deleted (is_deleted),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# TESTIMONIALS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    customer_location VARCHAR(100),
    review_text TEXT NOT NULL,
    rating INT DEFAULT 5,
    customer_photo VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_rating (rating),
    INDEX idx_is_active (is_active),
    INDEX idx_is_featured (is_featured),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# GALLERY IMAGES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS gallery_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_path VARCHAR(500) NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'gallery',
    alt_text VARCHAR(200),
    file_size INT,
    mime_type VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_category (category),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# WEBSITE SETTINGS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS website_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    setting_type VARCHAR(20) DEFAULT 'text',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_setting_key (setting_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# WEBSITE CONTENT TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS website_content (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section_name VARCHAR(50) NOT NULL,
    content_key VARCHAR(100) NOT NULL,
    content_value TEXT NOT NULL,
    content_type VARCHAR(20) DEFAULT 'text',
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- INDEXES
    INDEX idx_section_name (section_name),
    INDEX idx_content_key (content_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# ADMIN ACTIVITY LOGS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS admin_activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id INT,
    admin_username VARCHAR(50),
    action_type VARCHAR(50) NOT NULL,
    action_category VARCHAR(50),
    target_type VARCHAR(50),
    target_id INT,
    description TEXT NOT NULL,
    changes TEXT,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    status VARCHAR(20) DEFAULT 'success',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- FOREIGN KEY
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE SET NULL,
    
    -- INDEXES
    INDEX idx_admin_username (admin_username),
    INDEX idx_action_type (action_type),
    INDEX idx_action_category (action_category),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# USERS TABLE (For Desktop Software Login)
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    
    -- INDEXES
    INDEX idx_username (username),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
# INSERT DEFAULT DATA
-- ============================================================================

-- Default admin user (password: Admin@123)
INSERT INTO admins (username, password_hash, full_name, email, is_active) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'Admin User', 'admin@anshaircool.com', TRUE)
ON DUPLICATE KEY UPDATE username=username;

-- Default user for desktop software (password: Admin@123)
INSERT INTO users (username, password_hash, full_name, email, is_active) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'Admin User', 'admin@anshaircool.com', TRUE)
ON DUPLICATE KEY UPDATE username=username;

-- Default website settings
INSERT INTO website_settings (setting_key, setting_value, setting_type) VALUES
('site_title', 'Ansh Air Cool', 'text'),
('site_description', 'Professional AC Service & Installation', 'text'),
('contact_phone', '+91 9819104977', 'text'),
('contact_email', 'anshaircool@gmail.com', 'text'),
('contact_address', 'Mumbai, Maharashtra, India', 'text')
ON DUPLICATE KEY UPDATE setting_key=setting_key;

-- Default website content
INSERT INTO website_content (section_name, content_key, content_value, content_type) VALUES
('hero', 'title', 'Professional AC Service & Installation at Your Doorstep', 'text'),
('hero', 'subtitle', 'Certified Technicians | Same Day Service | Trusted by 1000+ Customers', 'text'),
('hero', 'cta_text', 'Book Now', 'text'),
('hero', 'cta_phone', '+91 9819104977', 'text'),
('contact', 'phone', '+91 9819104977', 'text'),
('contact', 'email', 'anshaircool@gmail.com', 'text'),
('footer', 'company_name', 'Ansh Air Cool', 'text'),
('footer', 'copyright', '© 2026 Ansh Air Cool. All rights reserved.', 'text')
ON DUPLICATE KEY UPDATE section_name=section_name;

-- Default services
INSERT INTO services (service_name, service_slug, starting_price, price_numeric, description, is_active) VALUES
('AC Installation', 'installation', '₹500', 500, 'Professional installation of new AC units', TRUE),
('AC Repair', 'repair', '₹300', 300, 'Expert repair for all AC brands and models', TRUE),
('Gas Refill', 'gas_refill', '₹800', 800, 'Complete gas refill with quality checked refrigerant', TRUE),
('AC Maintenance', 'maintenance', '₹400', 400, 'Comprehensive maintenance and servicing', TRUE),
('AMC', 'amc', '₹2000', 2000, 'Annual Maintenance Contract for hassle-free operation', TRUE)
ON DUPLICATE KEY UPDATE service_name=service_name;

-- ============================================================================
# CREATE VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Active customers view
CREATE OR REPLACE VIEW active_customers AS
SELECT * FROM customers WHERE is_deleted = FALSE AND is_active = TRUE;

-- Active invoices view
CREATE OR REPLACE VIEW active_invoices AS
SELECT * FROM invoices WHERE is_deleted = FALSE;

-- Paid invoices view (LOCKED)
CREATE OR REPLACE VIEW paid_invoices AS
SELECT * FROM invoices WHERE status = 'paid' AND is_deleted = FALSE;

-- Draft invoices view (EDITABLE)
CREATE OR REPLACE VIEW draft_invoices AS
SELECT * FROM invoices WHERE status = 'draft' AND is_deleted = FALSE;

-- ============================================================================
# VERIFICATION QUERY
-- ============================================================================

SELECT 'Database schema created successfully!' AS status;
SELECT COUNT(*) AS total_tables FROM information_schema.tables WHERE table_schema = 'ac_service_billing';
