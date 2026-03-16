-- ========================================
-- UPDATE contact_messages TABLE
-- Add missing columns to match backend models
-- ========================================

USE ac_service_billing;

-- Add missing columns to contact_messages table
ALTER TABLE contact_messages 
ADD COLUMN IF NOT EXISTS ac_type VARCHAR(20) DEFAULT 'Not Specified' AFTER service_type,
ADD COLUMN IF NOT EXISTS source VARCHAR(50) DEFAULT 'Website' AFTER status,
ADD COLUMN IF NOT EXISTS ip_address VARCHAR(45) AFTER source,
ADD COLUMN IF NOT EXISTS user_agent TEXT AFTER ip_address;

-- Modify email column to allow NULL
ALTER TABLE contact_messages 
MODIFY COLUMN email VARCHAR(100) NULL;

-- Modify address column to allow NULL  
ALTER TABLE contact_messages 
MODIFY COLUMN address TEXT NULL;

-- Verify columns added
SELECT 'Columns added successfully!' AS status;

-- Show table structure
DESCRIBE contact_messages;
