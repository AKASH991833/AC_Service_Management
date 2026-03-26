"""
Settings and master data controller
"""
from datetime import datetime

class SettingsController:
    def __init__(self, db_connection):
        self.db = db_connection
    
    # ========== SERVICES MANAGEMENT ==========
    def get_all_services(self):
        """Get all services"""
        query = "SELECT * FROM services ORDER BY service_name"
        return self.db.execute_query(query, fetch_all=True)
    
    def get_active_services(self):
        """Get active services only"""
        query = "SELECT * FROM services WHERE is_active = TRUE ORDER BY service_name"
        return self.db.execute_query(query, fetch_all=True)
    
    def add_service(self, service_name, description, default_rate):
        """Add new service"""
        # Check if service already exists
        check_query = "SELECT id FROM services WHERE service_name = %s"
        existing = self.db.execute_query(check_query, (service_name,), fetch_one=True)
        
        if existing:
            return False, "Service with this name already exists"
        
        # Insert new service
        query = """
        INSERT INTO services (service_name, description, default_rate, is_active)
        VALUES (%s, %s, %s, TRUE)
        """
        
        try:
            self.db.execute_query(query, (service_name, description, float(default_rate)))
            return True, "Service added successfully"
        except Exception as e:
            return False, f"Failed to add service: {str(e)}"
    
    def update_service(self, service_id, service_name, description, default_rate, is_active):
        """Update service"""
        # Check if name conflicts with other service
        check_query = "SELECT id FROM services WHERE service_name = %s AND id != %s"
        existing = self.db.execute_query(check_query, (service_name, service_id), fetch_one=True)
        
        if existing:
            return False, "Service with this name already exists"
        
        # Update service
        query = """
        UPDATE services 
        SET service_name = %s, description = %s, default_rate = %s, is_active = %s
        WHERE id = %s
        """
        
        try:
            self.db.execute_query(query, (service_name, description, float(default_rate), is_active, service_id))
            return True, "Service updated successfully"
        except Exception as e:
            return False, f"Failed to update service: {str(e)}"
    
    def delete_service(self, service_id):
        """Soft delete service"""
        # Check if service is used in any invoice
        check_query = """
        SELECT COUNT(*) as count FROM invoice_items 
        WHERE service_id = %s
        """
        result = self.db.execute_query(check_query, (service_id,), fetch_one=True)
        
        if result['count'] > 0:
            return False, "Cannot delete service that is used in invoices"
        
        # Soft delete
        query = "UPDATE services SET is_active = FALSE WHERE id = %s"
        
        try:
            self.db.execute_query(query, (service_id,))
            return True, "Service deleted successfully"
        except Exception as e:
            return False, f"Failed to delete service: {str(e)}"
    
    # ========== PARTS MANAGEMENT ==========
    def get_all_parts(self):
        """Get all parts"""
        query = "SELECT * FROM parts ORDER BY part_name"
        return self.db.execute_query(query, fetch_all=True)
    
    def get_active_parts(self):
        """Get active parts only"""
        query = "SELECT * FROM parts WHERE is_active = TRUE ORDER BY part_name"
        return self.db.execute_query(query, fetch_all=True)
    
    def add_part(self, part_name, description, default_rate, stock_quantity):
        """Add new part"""
        # Check if part already exists
        check_query = "SELECT id FROM parts WHERE part_name = %s"
        existing = self.db.execute_query(check_query, (part_name,), fetch_one=True)
        
        if existing:
            return False, "Part with this name already exists"
        
        # Insert new part
        query = """
        INSERT INTO parts (part_name, description, default_rate, stock_quantity, is_active)
        VALUES (%s, %s, %s, %s, TRUE)
        """
        
        try:
            self.db.execute_query(query, (part_name, description, float(default_rate), int(stock_quantity)))
            return True, "Part added successfully"
        except Exception as e:
            return False, f"Failed to add part: {str(e)}"
    
    def update_part(self, part_id, part_name, description, default_rate, stock_quantity, is_active):
        """Update part"""
        # Check if name conflicts with other part
        check_query = "SELECT id FROM parts WHERE part_name = %s AND id != %s"
        existing = self.db.execute_query(check_query, (part_name, part_id), fetch_one=True)
        
        if existing:
            return False, "Part with this name already exists"
        
        # Update part
        query = """
        UPDATE parts 
        SET part_name = %s, description = %s, default_rate = %s, 
            stock_quantity = %s, is_active = %s
        WHERE id = %s
        """
        
        try:
            self.db.execute_query(query, (part_name, description, float(default_rate), 
                                         int(stock_quantity), is_active, part_id))
            return True, "Part updated successfully"
        except Exception as e:
            return False, f"Failed to update part: {str(e)}"
    
    def delete_part(self, part_id):
        """Soft delete part"""
        # Check if part is used in any invoice
        check_query = """
        SELECT COUNT(*) as count FROM invoice_items 
        WHERE part_id = %s
        """
        result = self.db.execute_query(check_query, (part_id,), fetch_one=True)
        
        if result['count'] > 0:
            return False, "Cannot delete part that is used in invoices"
        
        # Soft delete
        query = "UPDATE parts SET is_active = FALSE WHERE id = %s"
        
        try:
            self.db.execute_query(query, (part_id,))
            return True, "Part deleted successfully"
        except Exception as e:
            return False, f"Failed to delete part: {str(e)}"
    
    def update_stock(self, part_id, quantity_change):
        """Update stock quantity for part"""
        query = "UPDATE parts SET stock_quantity = stock_quantity + %s WHERE id = %s"
        
        try:
            self.db.execute_query(query, (quantity_change, part_id))
            return True, "Stock updated successfully"
        except Exception as e:
            return False, f"Failed to update stock: {str(e)}"
    
    def get_low_stock_parts(self, threshold=5):
        """Get parts with low stock"""
        query = """
        SELECT * FROM parts 
        WHERE is_active = TRUE AND stock_quantity <= %s
        ORDER BY stock_quantity
        """
        return self.db.execute_query(query, (threshold,), fetch_all=True)
    
    # ========== AC BRANDS MANAGEMENT ==========
    def get_all_ac_brands(self):
        """Get all AC brands"""
        query = "SELECT * FROM ac_brands ORDER BY brand_name"
        return self.db.execute_query(query, fetch_all=True)
    
    def get_active_ac_brands(self):
        """Get active AC brands only"""
        query = "SELECT * FROM ac_brands WHERE is_active = TRUE ORDER BY brand_name"
        return self.db.execute_query(query, fetch_all=True)
    
    def add_ac_brand(self, brand_name):
        """Add new AC brand"""
        # Check if brand already exists
        check_query = "SELECT id FROM ac_brands WHERE brand_name = %s"
        existing = self.db.execute_query(check_query, (brand_name,), fetch_one=True)
        
        if existing:
            return False, "Brand with this name already exists"
        
        # Insert new brand
        query = "INSERT INTO ac_brands (brand_name, is_active) VALUES (%s, TRUE)"
        
        try:
            self.db.execute_query(query, (brand_name,))
            return True, "Brand added successfully"
        except Exception as e:
            return False, f"Failed to add brand: {str(e)}"
    
    def update_ac_brand(self, brand_id, brand_name, is_active):
        """Update AC brand"""
        # Check if name conflicts with other brand
        check_query = "SELECT id FROM ac_brands WHERE brand_name = %s AND id != %s"
        existing = self.db.execute_query(check_query, (brand_name, brand_id), fetch_one=True)
        
        if existing:
            return False, "Brand with this name already exists"
        
        # Update brand
        query = "UPDATE ac_brands SET brand_name = %s, is_active = %s WHERE id = %s"
        
        try:
            self.db.execute_query(query, (brand_name, is_active, brand_id))
            return True, "Brand updated successfully"
        except Exception as e:
            return False, f"Failed to update brand: {str(e)}"
    
    def delete_ac_brand(self, brand_id):
        """Soft delete AC brand"""
        # Check if brand is used in any invoice
        check_query = """
        SELECT COUNT(*) as count FROM invoices 
        WHERE ac_brand_id = %s
        """
        result = self.db.execute_query(check_query, (brand_id,), fetch_one=True)
        
        if result['count'] > 0:
            return False, "Cannot delete brand that is used in invoices"
        
        # Soft delete
        query = "UPDATE ac_brands SET is_active = FALSE WHERE id = %s"
        
        try:
            self.db.execute_query(query, (brand_id,))
            return True, "Brand deleted successfully"
        except Exception as e:
            return False, f"Failed to delete brand: {str(e)}"
    
    # ========== PRICE LIST ==========
    def get_price_list(self):
        """Get combined price list of services and parts"""
        # Get services
        services_query = """
        SELECT 
            'service' as type,
            id,
            service_name as name,
            description,
            default_rate as rate,
            NULL as stock_quantity,
            is_active
        FROM services
        WHERE is_active = TRUE
        """
        services = self.db.execute_query(services_query, fetch_all=True)
        
        # Get parts
        parts_query = """
        SELECT 
            'part' as type,
            id,
            part_name as name,
            description,
            default_rate as rate,
            stock_quantity,
            is_active
        FROM parts
        WHERE is_active = TRUE
        """
        parts = self.db.execute_query(parts_query, fetch_all=True)
        
        # Combine and return
        return services + parts
    
    def update_prices(self, price_updates):
        """Update multiple prices at once"""
        try:
            # Update services
            for update in price_updates.get('services', []):
                query = "UPDATE services SET default_rate = %s WHERE id = %s"
                self.db.execute_query(query, (update['rate'], update['id']))
            
            # Update parts
            for update in price_updates.get('parts', []):
                query = "UPDATE parts SET default_rate = %s WHERE id = %s"
                self.db.execute_query(query, (update['rate'], update['id']))
            
            return True, "Prices updated successfully"
        except Exception as e:
            return False, f"Failed to update prices: {str(e)}"
    
    # ========== APPLICATION SETTINGS ==========
    def get_application_settings(self):
        """Get application settings"""
        # In a real application, these would be stored in a settings table
        # For now, return default settings
        return {
            'invoice_prefix': 'INV',
            'default_gst_percentage': 18.0,
            'company_name': 'AC Service Center',
            'currency_symbol': '₹',
            'date_format': 'dd-mm-yyyy',
            'print_auto': False,
            'email_notifications': False
        }
    
    def save_application_settings(self, settings):
        """Save application settings"""
        # In a real application, these would be saved to a settings table
        # For now, just return success
        return True, "Settings saved successfully"
    
    # ========== BACKUP & RESTORE ==========
    def create_backup(self, backup_path):
        """Create database backup"""
        import subprocess
        import os
        from config import DB_CONFIG
        
        try:
            # Create backup using mysqldump
            cmd = [
                'mysqldump',
                '-h', DB_CONFIG['host'],
                '-u', DB_CONFIG['user'],
                '-p' + DB_CONFIG['password'],
                DB_CONFIG['database']
            ]
            
            with open(backup_path, 'w') as backup_file:
                subprocess.run(cmd, stdout=backup_file, stderr=subprocess.PIPE)
            
            return True, f"Backup created successfully: {backup_path}"
        except Exception as e:
            return False, f"Failed to create backup: {str(e)}"
    
    def restore_backup(self, backup_path):
        """Restore database from backup"""
        import subprocess
        from config import DB_CONFIG
        
        try:
            # Restore using mysql command
            cmd = [
                'mysql',
                '-h', DB_CONFIG['host'],
                '-u', DB_CONFIG['user'],
                '-p' + DB_CONFIG['password'],
                DB_CONFIG['database']
            ]
            
            with open(backup_path, 'r') as backup_file:
                subprocess.run(cmd, stdin=backup_file, stderr=subprocess.PIPE)
            
            return True, "Backup restored successfully"
        except Exception as e:
            return False, f"Failed to restore backup: {str(e)}"
    
    # ========== REPORTS ==========
    def get_inventory_report(self):
        """Get inventory report"""
        query = """
        SELECT 
            p.part_name,
            p.description,
            p.default_rate,
            p.stock_quantity,
            COALESCE(SUM(ii.quantity), 0) as total_sold,
            COALESCE(SUM(ii.amount), 0) as total_revenue,
            (p.stock_quantity * p.default_rate) as stock_value
        FROM parts p
        LEFT JOIN invoice_items ii ON p.id = ii.part_id
        WHERE p.is_active = TRUE
        GROUP BY p.id, p.part_name, p.description, p.default_rate, p.stock_quantity
        ORDER BY p.part_name
        """
        return self.db.execute_query(query, fetch_all=True)
    
    def get_service_usage_report(self, start_date=None, end_date=None):
        """Get service usage report"""
        if not start_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        query = """
        SELECT 
            s.service_name,
            s.description,
            s.default_rate,
            COUNT(ii.id) as times_used,
            COALESCE(SUM(ii.quantity), 0) as total_quantity,
            COALESCE(SUM(ii.amount), 0) as total_revenue
        FROM services s
        LEFT JOIN invoice_items ii ON s.id = ii.service_id
        LEFT JOIN invoices i ON ii.invoice_id = i.id
            AND i.is_active = TRUE
            AND DATE(i.created_at) BETWEEN %s AND %s
        WHERE s.is_active = TRUE
        GROUP BY s.id, s.service_name, s.description, s.default_rate
        ORDER BY total_revenue DESC
        """
        return self.db.execute_query(query, (start_date, end_date), fetch_all=True)