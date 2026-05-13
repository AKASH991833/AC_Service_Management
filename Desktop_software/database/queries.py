"""
Database queries for AC Service Billing Software
"""
from datetime import datetime, timedelta

class Queries:
    """Centralized database queries"""
    
    # ========== AUTH QUERIES ==========
    @staticmethod
    def get_user_by_username():
        return """
        SELECT id, username, password_hash, full_name, email, phone, is_active 
        FROM users 
        WHERE username = %s AND is_active = TRUE
        """
    
    @staticmethod
    def update_user_password():
        return "UPDATE users SET password_hash = %s, updated_at = NOW() WHERE id = %s"
    
    @staticmethod
    def update_user_profile():
        return """
        UPDATE users 
        SET full_name = %s, email = %s, phone = %s, updated_at = NOW() 
        WHERE id = %s
        """
    
    # ========== DASHBOARD QUERIES ==========
    @staticmethod
    def get_total_customers():
        return "SELECT COUNT(*) as count FROM customers WHERE is_active = TRUE"

    @staticmethod
    def get_total_invoices(period_condition=None):
        # Returns (query, params) tuple for safe parameterized execution
        if period_condition and isinstance(period_condition, tuple):
            query = f"""
            SELECT COUNT(*) as count FROM invoices
            WHERE is_active = TRUE {period_condition[0]}
            """
            return query, period_condition[1] if len(period_condition) > 1 else ()
        return "SELECT COUNT(*) as count FROM invoices WHERE is_active = TRUE", ()

    @staticmethod
    def get_total_revenue(period_condition=None):
        # Returns (query, params) tuple for safe parameterized execution
        if period_condition and isinstance(period_condition, tuple):
            query = f"""
            SELECT COALESCE(SUM(total_amount), 0) as revenue FROM invoices
            WHERE is_active = TRUE {period_condition[0]}
            """
            return query, period_condition[1] if len(period_condition) > 1 else ()
        return "SELECT COALESCE(SUM(total_amount), 0) as revenue FROM invoices WHERE is_active = TRUE", ()

    @staticmethod
    def get_pending_payments():
        return """
        SELECT
            c.name as customer_name,
            i.balance_amount,
            DATE(i.created_at) as invoice_date,
            i.invoice_number,
            i.id as invoice_id
        FROM invoices i
        JOIN customers c ON i.customer_id = c.id
        WHERE i.is_active = TRUE
        AND i.balance_amount > 0
        AND i.payment_status != 'Paid'
        ORDER BY i.created_at DESC
        """

    @staticmethod
    def get_today_summary(date):
        # Use parameterized query pattern - date should be passed as parameter
        return {
            'services_done': """
                SELECT COUNT(*) as count FROM invoices
                WHERE is_active = TRUE AND DATE(created_at) = %s
            """,
            'payment_received': """
                SELECT COALESCE(SUM(advance_payment), 0) as amount
                FROM invoices
                WHERE is_active = TRUE AND DATE(created_at) = %s
                AND payment_mode != 'Pending'
            """,
            'new_customers': """
                SELECT COUNT(*) as count FROM customers
                WHERE is_active = TRUE AND DATE(created_at) = %s
            """,
            'date_param': date  # Return date as param to be used with query
        }
    
    # ========== CUSTOMER QUERIES ==========
    @staticmethod
    def search_customers():
        return """
        SELECT 
            id, name, mobile, email, address, landmark,
            DATE(created_at) as created_date,
            (SELECT COUNT(*) FROM invoices WHERE customer_id = customers.id AND is_active = TRUE) as total_services,
            (SELECT COALESCE(SUM(balance_amount), 0) FROM invoices WHERE customer_id = customers.id AND is_active = TRUE) as pending_amount,
            (SELECT COALESCE(SUM(total_amount), 0) FROM invoices WHERE customer_id = customers.id AND is_active = TRUE) as total_paid
        FROM customers 
        WHERE is_active = TRUE 
        AND (name LIKE %s OR mobile LIKE %s OR address LIKE %s)
        ORDER BY name
        """
    
    @staticmethod
    def get_customer_invoices():
        return """
        SELECT 
            i.id, i.invoice_number, DATE(i.created_at) as invoice_date,
            i.total_amount, i.advance_payment, i.balance_amount,
            i.payment_status, i.payment_mode,
            ab.brand_name as ac_brand,
            t.name as technician_name
        FROM invoices i
        LEFT JOIN ac_brands ab ON i.ac_brand_id = ab.id
        LEFT JOIN technicians t ON i.technician_id = t.id
        WHERE i.customer_id = %s AND i.is_active = TRUE
        ORDER BY i.created_at DESC
        """
    
    @staticmethod
    def insert_customer():
        return """
        INSERT INTO customers (name, mobile, email, address, landmark, is_active) 
        VALUES (%s, %s, %s, %s, %s, TRUE)
        """
    
    # ========== INVOICE QUERIES ==========
    @staticmethod
    def get_next_invoice_number():
        return """
        SELECT MAX(CAST(SUBSTRING(invoice_number, 4) AS UNSIGNED)) as max_num 
        FROM invoices
        """
    
    @staticmethod
    def insert_invoice():
        return """
        INSERT INTO invoices (
            invoice_number, customer_id, ac_brand_id, ac_type, star_rating,
            ton_capacity, inverter_type, technician_id, subtotal, gst_percentage,
            gst_amount, total_amount, advance_payment, balance_amount,
            payment_mode, payment_status, notes, is_active, is_deleted
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, FALSE)
        """
    
    @staticmethod
    def insert_invoice_item():
        return """
        INSERT INTO invoice_items (
            invoice_id, item_type, service_id, part_id, quantity, rate, amount
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
    
    @staticmethod
    def get_invoice_details():
        return """
        SELECT 
            i.*,
            c.name as customer_name, c.mobile, c.email as customer_email, 
            c.address as customer_address, c.landmark,
            ab.brand_name,
            t.name as technician_name, t.mobile as technician_mobile
        FROM invoices i
        JOIN customers c ON i.customer_id = c.id
        LEFT JOIN ac_brands ab ON i.ac_brand_id = ab.id
        LEFT JOIN technicians t ON i.technician_id = t.id
        WHERE i.id = %s AND i.is_active = TRUE
        """
    
    @staticmethod
    def get_invoice_items():
        return """
        SELECT 
            ii.*,
            s.service_name,
            p.part_name
        FROM invoice_items ii
        LEFT JOIN services s ON ii.service_id = s.id
        LEFT JOIN parts p ON ii.part_id = p.id
        WHERE ii.invoice_id = %s
        ORDER BY ii.id
        """
    
    # ========== MASTER DATA QUERIES ==========
    @staticmethod
    def get_ac_brands():
        return "SELECT id, brand_name FROM ac_brands WHERE is_active = TRUE ORDER BY brand_name"
    
    @staticmethod
    def get_services():
        return "SELECT id, service_name, default_rate FROM services WHERE is_active = TRUE ORDER BY service_name"
    
    @staticmethod
    def get_parts():
        return "SELECT id, part_name, default_rate, stock_quantity FROM parts WHERE is_active = TRUE ORDER BY part_name"
    
    @staticmethod
    def get_technicians():
        return "SELECT id, name, mobile FROM technicians WHERE is_active = TRUE ORDER BY name"
    
    @staticmethod
    def insert_ac_brand():
        return "INSERT INTO ac_brands (brand_name, is_active) VALUES (%s, TRUE)"
    
    @staticmethod
    def insert_service():
        return "INSERT INTO services (service_name, description, default_rate, is_active) VALUES (%s, %s, %s, TRUE)"
    
    @staticmethod
    def insert_part():
        return "INSERT INTO parts (part_name, description, default_rate, stock_quantity, is_active) VALUES (%s, %s, %s, %s, TRUE)"
    
    # ========== TECHNICIAN QUERIES ==========
    @staticmethod
    def get_technician_summary():
        return """
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
    
    @staticmethod
    def get_technician_work_history():
        return """
        SELECT
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
        ORDER BY i.created_at DESC
        """

    # ========== AMC QUERIES ==========
    @staticmethod
    def get_next_amc_number():
        return """
        SELECT MAX(CAST(SUBSTRING(amc_id, 4) AS UNSIGNED)) as max_num
        FROM amc_contracts
        """

    @staticmethod
    def insert_amc_contract():
        return """
        INSERT INTO amc_contracts (
            amc_id, customer_id, contract_type, start_date, end_date,
            no_of_units, services_per_year, services_remaining, contract_amount, gst_percent,
            total_amount, advance_paid, balance_amount, payment_mode, payment_status,
            next_due_date, amc_status, grace_period, renewal_reminder_date, notes, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        """

    @staticmethod
    def get_all_amc_contracts():
        return """
        SELECT
            ac.*,
            c.name as customer_name,
            c.mobile as customer_mobile,
            c.address as customer_address,
            (SELECT COUNT(*) FROM amc_units au WHERE au.amc_id = ac.id AND au.is_active = TRUE) as unit_count,
            (SELECT COUNT(*) FROM amc_visits av WHERE av.amc_id = ac.id AND av.visit_status = 'Completed' AND av.is_active = TRUE) as completed_visits
        FROM amc_contracts ac
        JOIN customers c ON ac.customer_id = c.id
        WHERE ac.is_active = TRUE
        ORDER BY ac.created_at DESC
        """

    @staticmethod
    def get_amc_by_customer_id():
        return """
        SELECT
            ac.*,
            c.name as customer_name,
            c.mobile as customer_mobile,
            c.address as customer_address
        FROM amc_contracts ac
        JOIN customers c ON ac.customer_id = c.id
        WHERE ac.customer_id = %s AND ac.is_active = TRUE
        ORDER BY ac.created_at DESC
        """

    @staticmethod
    def get_amc_contract_by_id():
        return """
        SELECT
            ac.*,
            c.name as customer_name,
            c.mobile as customer_mobile,
            c.email as customer_email,
            c.address as customer_address,
            c.landmark as customer_landmark
        FROM amc_contracts ac
        JOIN customers c ON ac.customer_id = c.id
        WHERE ac.id = %s AND ac.is_active = TRUE
        """

    @staticmethod
    def search_amc_contracts():
        return """
        SELECT
            ac.*,
            c.name as customer_name,
            c.mobile as customer_mobile
        FROM amc_contracts ac
        JOIN customers c ON ac.customer_id = c.id
        WHERE ac.is_active = TRUE
        AND (ac.amc_id LIKE %s OR c.name LIKE %s OR c.mobile LIKE %s)
        ORDER BY ac.created_at DESC
        """

    @staticmethod
    def insert_amc_unit():
        return """
        INSERT INTO amc_units (
            amc_id, brand, ac_type, ton, star_rating, inverter,
            model, serial_number, indoor_location, outdoor_location,
            installation_date, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        """

    @staticmethod
    def get_amc_units():
        return """
        SELECT * FROM amc_units
        WHERE amc_id = %s AND is_active = TRUE
        ORDER BY id
        """

    @staticmethod
    def insert_amc_visit():
        return """
        INSERT INTO amc_visits (
            amc_id, visit_number, visit_date, technician_id,
            work_done, parts_replaced, extra_charge, next_due_date,
            visit_status, notes, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        """

    @staticmethod
    def get_amc_visits():
        return """
        SELECT
            av.*,
            t.name as technician_name,
            t.mobile as technician_mobile
        FROM amc_visits av
        LEFT JOIN technicians t ON av.technician_id = t.id
        WHERE av.amc_id = %s AND av.is_active = TRUE
        ORDER BY av.visit_number
        """

    @staticmethod
    def get_upcoming_amc_visits():
        return """
        SELECT
            av.*,
            ac.amc_id,
            c.name as customer_name,
            c.mobile as customer_mobile,
            c.address as customer_address,
            t.name as technician_name
        FROM amc_visits av
        JOIN amc_contracts ac ON av.amc_id = ac.id
        JOIN customers c ON ac.customer_id = c.id
        LEFT JOIN technicians t ON av.technician_id = t.id
        WHERE av.visit_status = 'Scheduled'
        AND av.is_active = TRUE
        AND ac.amc_status = 'Active'
        AND av.visit_date >= CURDATE()
        ORDER BY av.visit_date
        LIMIT 10
        """

    @staticmethod
    def update_amc_status():
        return """
        UPDATE amc_contracts
        SET amc_status = %s, updated_at = NOW()
        WHERE id = %s
        """

    @staticmethod
    def update_amc_services_remaining():
        return """
        UPDATE amc_contracts
        SET services_remaining = services_remaining - 1, updated_at = NOW()
        WHERE id = %s AND services_remaining > 0
        """

    @staticmethod
    def update_amc_payment():
        return """
        UPDATE amc_contracts
        SET advance_paid = %s, balance_amount = %s, payment_status = %s,
            payment_mode = %s, next_due_date = %s, updated_at = NOW()
        WHERE id = %s
        """

    @staticmethod
    def update_visit_status():
        return """
        UPDATE amc_visits
        SET visit_status = %s, work_done = %s, parts_replaced = %s,
            extra_charge = %s, next_due_date = %s, notes = %s, updated_at = NOW()
        WHERE id = %s
        """

    @staticmethod
    def get_amc_expiry_stats():
        return """
        SELECT
            COUNT(*) as total_active,
            SUM(CASE WHEN end_date <= DATE_ADD(CURDATE(), INTERVAL 30 DAY) THEN 1 ELSE 0 END) as expiring_soon,
            SUM(CASE WHEN end_date < CURDATE() THEN 1 ELSE 0 END) as expired
        FROM amc_contracts
        WHERE amc_status = 'Active' AND is_active = TRUE
        """

    @staticmethod
    def get_amc_revenue():
        return """
        SELECT
            COALESCE(SUM(total_amount), 0) as total_revenue,
            COALESCE(SUM(advance_paid), 0) as collected,
            COALESCE(SUM(balance_amount), 0) as pending
        FROM amc_contracts
        WHERE is_active = TRUE
        """

    @staticmethod
    def search_customer_for_amc():
        return """
        SELECT
            id, name, mobile, email, address, landmark,
            (SELECT COUNT(*) FROM amc_contracts WHERE customer_id = customers.id AND amc_status = 'Active' AND is_active = TRUE) as active_amc_count
        FROM customers
        WHERE is_active = TRUE
        AND (name LIKE %s OR mobile LIKE %s)
        ORDER BY name
        """

    @staticmethod
    def insert_amc_invoice():
        return """
        INSERT INTO amc_invoices (
            amc_contract_id, invoice_number, invoice_date,
            subtotal, gst_percent, gst_amount, total_amount,
            advance_payment, balance_amount, payment_mode,
            payment_status, notes, is_active
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
        """

    @staticmethod
    def get_amc_invoice_details():
        return """
        SELECT
            ai.*,
            ac.amc_id,
            c.name as customer_name,
            c.mobile as customer_mobile,
            c.address as customer_address
        FROM amc_invoices ai
        JOIN amc_contracts ac ON ai.amc_contract_id = ac.id
        JOIN customers c ON ac.customer_id = c.id
        WHERE ai.id = %s AND ai.is_active = TRUE
        """

    @staticmethod
    def insert_customer():
        return """
        INSERT INTO customers (name, mobile, email, address, landmark, is_active)
        VALUES (%s, %s, %s, %s, %s, TRUE)
        """

    @staticmethod
    def get_customer_by_mobile():
        return """
        SELECT id, name, mobile, email, address, landmark
        FROM customers
        WHERE mobile = %s AND is_active = TRUE
        """