"""
Technician controller
"""
from datetime import datetime, timedelta

class TechnicianController:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def get_technicians_summary(self, start_date=None, end_date=None):
        """Get technicians with work summary"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        query = """
        SELECT 
            t.id,
            t.name,
            t.mobile,
            COUNT(i.id) as services_done,
            COALESCE(SUM(i.advance_payment), 0) as amount_collected,
            COALESCE(SUM(i.balance_amount), 0) as pending_amount
        FROM technicians t
        LEFT JOIN invoices i ON t.id = i.technician_id
            AND i.is_active = TRUE
            AND DATE(i.created_at) BETWEEN %s AND %s
        WHERE t.is_active = TRUE
        GROUP BY t.id, t.name, t.mobile
        ORDER BY t.name
        """
        
        return self.db.execute_query(query, (start_date, end_date), fetch_all=True)
    
    def get_technician_profile(self, technician_id):
        """Get technician profile with statistics"""
        # Basic info
        query = """
        SELECT 
            t.*,
            (SELECT COUNT(*) FROM invoices i WHERE i.technician_id = t.id AND i.is_active = TRUE) as total_services,
            (SELECT COALESCE(SUM(i.total_amount), 0) FROM invoices i WHERE i.technician_id = t.id AND i.is_active = TRUE) as total_revenue,
            (SELECT COALESCE(SUM(i.advance_payment), 0) FROM invoices i WHERE i.technician_id = t.id AND i.is_active = TRUE) as amount_collected,
            (SELECT COALESCE(SUM(i.balance_amount), 0) FROM invoices i WHERE i.technician_id = t.id AND i.is_active = TRUE) as pending_amount
        FROM technicians t
        WHERE t.id = %s
        """
        
        profile = self.db.execute_query(query, (technician_id,), fetch_one=True)
        
        if not profile:
            return None
        
        # Calculate commission
        commission_earned = profile['total_revenue'] * (profile['commission_rate'] / 100)
        profile['commission_earned'] = commission_earned
        
        return profile
    
    def get_work_summary(self, technician_id, start_date, end_date):
        """Get daily work summary for technician"""
        # Daily summary
        daily_query = """
        SELECT 
            DATE(i.created_at) as work_date,
            COUNT(*) as services_done,
            COALESCE(SUM(i.advance_payment), 0) as amount_collected,
            COALESCE(SUM(i.balance_amount), 0) as pending_amount,
            GROUP_CONCAT(DISTINCT c.name SEPARATOR ', ') as customers_served
        FROM invoices i
        JOIN customers c ON i.customer_id = c.id
        WHERE i.technician_id = %s
        AND i.is_active = TRUE
        AND DATE(i.created_at) BETWEEN %s AND %s
        GROUP BY DATE(i.created_at)
        ORDER BY work_date DESC
        """
        
        daily_summary = self.db.execute_query(daily_query, (technician_id, start_date, end_date), fetch_all=True)
        
        # Statistics
        stats_query = """
        SELECT 
            COUNT(DISTINCT DATE(i.created_at)) as days_worked,
            COUNT(*) as total_services,
            COALESCE(SUM(i.advance_payment), 0) as total_collected,
            COALESCE(SUM(i.balance_amount), 0) as total_pending
        FROM invoices i
        WHERE i.technician_id = %s
        AND i.is_active = TRUE
        AND DATE(i.created_at) BETWEEN %s AND %s
        """
        
        stats = self.db.execute_query(stats_query, (technician_id, start_date, end_date), fetch_one=True)
        
        return {
            'daily_summary': daily_summary,
            'statistics': stats or {
                'days_worked': 0,
                'total_services': 0,
                'total_collected': 0,
                'total_pending': 0
            }
        }
    
    def get_service_history(self, technician_id, start_date, end_date):
        """Get service history for technician"""
        query = """
        SELECT 
            i.id as invoice_id,
            i.invoice_number,
            DATE(i.created_at) as work_date,
            c.name as customer_name,
            c.mobile,
            i.total_amount,
            i.payment_status,
            i.payment_mode,
            (SELECT GROUP_CONCAT(s.service_name SEPARATOR ', ') 
             FROM invoice_items ii 
             JOIN services s ON ii.service_id = s.id 
             WHERE ii.invoice_id = i.id) as services_performed
        FROM invoices i
        JOIN customers c ON i.customer_id = c.id
        WHERE i.technician_id = %s
        AND i.is_active = TRUE
        AND DATE(i.created_at) BETWEEN %s AND %s
        ORDER BY i.created_at DESC
        """
        
        return self.db.execute_query(query, (technician_id, start_date, end_date), fetch_all=True)
    
    def add_technician(self, name, mobile, email=None, address=None, commission_rate=10):
        """Add new technician"""
        from utils.formatters import Formatters

        name = Formatters.format_upper(name)
        if address:
            address = Formatters.format_title(address) # Address should be title case

        query = """
        INSERT INTO technicians (name, mobile, email, address, commission_rate, is_active)
        VALUES (%s, %s, %s, %s, %s, TRUE)
        """
        
        try:
            return self.db.execute_query(query, (name, mobile, email, address, commission_rate))
        except Exception as e:
            raise Exception(f"Failed to add technician: {str(e)}")
    
    def update_technician(self, technician_id, name, mobile, email=None, address=None, commission_rate=10, is_active=True):
        """Update technician"""
        from utils.formatters import Formatters

        name = Formatters.format_upper(name)
        if address:
            address = Formatters.format_title(address) # Address should be title case

        query = """
        UPDATE technicians 
        SET name = %s, mobile = %s, email = %s, address = %s, 
            commission_rate = %s, is_active = %s, updated_at = NOW()
        WHERE id = %s
        """
        
        try:
            self.db.execute_query(query, (name, mobile, email, address, commission_rate, is_active, technician_id))
            return True
        except Exception as e:
            raise Exception(f"Failed to update technician: {str(e)}")
    
    def delete_technician(self, technician_id):
        """Soft delete technician"""
        query = "UPDATE technicians SET is_active = FALSE WHERE id = %s"
        
        try:
            self.db.execute_query(query, (technician_id,))
            return True
        except Exception as e:
            raise Exception(f"Failed to delete technician: {str(e)}")
    
    def get_technician_performance_report(self, start_date=None, end_date=None):
        """Get performance report for all technicians"""
        if not start_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        query = """
        SELECT 
            t.id,
            t.name,
            t.mobile,
            t.commission_rate,
            COUNT(i.id) as total_services,
            COALESCE(SUM(i.total_amount), 0) as total_revenue,
            COALESCE(SUM(i.advance_payment), 0) as amount_collected,
            COALESCE(SUM(i.balance_amount), 0) as pending_amount,
            COUNT(DISTINCT DATE(i.created_at)) as days_worked,
            COALESCE(SUM(i.total_amount) / NULLIF(COUNT(i.id), 0), 0) as avg_service_value
        FROM technicians t
        LEFT JOIN invoices i ON t.id = i.technician_id
            AND i.is_active = TRUE
            AND DATE(i.created_at) BETWEEN %s AND %s
        WHERE t.is_active = TRUE
        GROUP BY t.id, t.name, t.mobile, t.commission_rate
        ORDER BY total_revenue DESC
        """
        
        return self.db.execute_query(query, (start_date, end_date), fetch_all=True)
    
    def assign_invoice_to_technician(self, invoice_id, technician_id):
        """Assign invoice to technician"""
        query = "UPDATE invoices SET technician_id = %s, updated_at = NOW() WHERE id = %s"
        
        try:
            self.db.execute_query(query, (technician_id, invoice_id))
            return True
        except Exception as e:
            raise Exception(f"Failed to assign invoice: {str(e)}")
    
    def get_available_technicians(self):
        """Get list of active technicians"""
        query = "SELECT id, name, mobile FROM technicians WHERE is_active = TRUE ORDER BY name"
        return self.db.execute_query(query, fetch_all=True)
    
    def calculate_commission(self, technician_id, start_date=None, end_date=None):
        """Calculate commission for technician"""
        if not start_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Get technician commission rate
        tech_query = "SELECT commission_rate FROM technicians WHERE id = %s"
        tech = self.db.execute_query(tech_query, (technician_id,), fetch_one=True)
        
        if not tech:
            return 0
        
        commission_rate = tech['commission_rate']
        
        # Get total revenue for period
        revenue_query = """
        SELECT COALESCE(SUM(total_amount), 0) as total_revenue
        FROM invoices
        WHERE technician_id = %s
        AND is_active = TRUE
        AND DATE(created_at) BETWEEN %s AND %s
        """
        
        revenue = self.db.execute_query(revenue_query, (technician_id, start_date, end_date), fetch_one=True)
        
        commission = revenue['total_revenue'] * (commission_rate / 100)
        return commission