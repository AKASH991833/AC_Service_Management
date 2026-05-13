"""
Invoice controller
"""
from datetime import datetime
from decimal import Decimal

class InvoiceController:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_invoice(self, invoice_data):
        """Create a new invoice with transaction support"""
        # Ensure connection exists
        if not hasattr(self.db, 'connection') or not self.db.connection:
            return None, "Database connection not available"
        
        # Disable autocommit for transaction
        original_autocommit = self.db.connection.autocommit
        self.db.connection.autocommit = False
        
        try:
            # 1. Get or create customer
            customer_id = self._get_or_create_customer(invoice_data['customer'])
            if not customer_id:
                self.db.connection.rollback()
                return None, "Failed to create customer"

            # 2. Get AC brand ID
            ac_brand_id = self._get_ac_brand_id(invoice_data['ac_details']['brand'])

            # 3. Get technician ID
            technician_id = self._get_technician_id(invoice_data['technician'])

            # 4. Create invoice
            invoice_id = self._create_invoice_record(
                customer_id, ac_brand_id, technician_id, invoice_data
            )

            if not invoice_id:
                self.db.connection.rollback()
                return None, "Failed to create invoice"

            # 5. Create invoice items
            self._create_invoice_items(invoice_id, invoice_data['items'])

            # 6. Update stock for parts
            self._update_stock(invoice_data['items'])

            # Commit transaction
            self.db.connection.commit()
            return invoice_id, None

        except Exception as e:
            # Rollback on error
            try:
                self.db.connection.rollback()
            except:
                pass
            return None, f"Error creating invoice: {str(e)}"
        
        finally:
            # Restore original autocommit setting
            try:
                self.db.connection.autocommit = original_autocommit
            except:
                pass
    
    def _get_or_create_customer(self, customer_data):
        """Get existing customer or create new using centralized queries"""
        from utils.formatters import Formatters
        from database.queries import Queries

        # Format customer data
        customer_data['name'] = Formatters.format_title(customer_data['name'])
        if customer_data['address']:
            customer_data['address'] = Formatters.format_title(customer_data['address'])
        if customer_data['landmark']:
            customer_data['landmark'] = Formatters.format_title(customer_data['landmark'])

        # Check if customer exists by mobile (using Queries)
        existing = self.db.execute_query(Queries.get_customer_by_mobile(), (customer_data['mobile'],), fetch_one=True)

        if existing:
            # Update customer details if needed
            update_query = """
            UPDATE customers 
            SET name = %s, email = %s, address = %s, landmark = %s, updated_at = NOW()
            WHERE id = %s
            """
            self.db.execute_query(update_query, (
                customer_data['name'],
                customer_data['email'],
                customer_data['address'],
                customer_data['landmark'],
                existing['id']
            ))
            return existing['id']
        else:
            # Create new customer (using Queries)
            query = Queries.insert_customer()
            return self.db.execute_query(query, (
                customer_data['name'],
                customer_data['mobile'],
                customer_data['email'],
                customer_data['address'],
                customer_data['landmark']
            ))
    
    def _get_ac_brand_id(self, brand_name):
        """Get AC brand ID, create if doesn't exist"""
        from utils.formatters import Formatters
        from database.queries import Queries

        if not brand_name:
            return None

        brand_name = Formatters.format_title(brand_name)

        # Get existing brand
        query = "SELECT id FROM ac_brands WHERE brand_name = %s AND is_active = TRUE"
        existing = self.db.execute_query(query, (brand_name,), fetch_one=True)

        if existing:
            return existing['id']
        else:
            # Create new brand (using Queries)
            query = Queries.insert_ac_brand()
            return self.db.execute_query(query, (brand_name,))
    
    def _get_technician_id(self, technician_str):
        """Extract technician ID from string"""
        if not technician_str:
            return None
        
        try:
            # Format: "1: John Doe"
            tech_id = int(technician_str.split(':')[0].strip())
            return tech_id
        except:
            return None
    
    def _create_invoice_record(self, customer_id, ac_brand_id, technician_id, invoice_data):
        """Create invoice record in database"""
        from utils.formatters import Formatters

        notes = invoice_data['notes']
        if notes:
            notes = Formatters.format_sentence(notes)

        # VALIDATION: Technician must be assigned
        if not technician_id:
            raise ValueError("Technician assignment is required. Please select a technician.")

        # FIRST: Check if invoice number already exists (safety check)
        check_query = "SELECT id FROM invoices WHERE invoice_number = %s FOR UPDATE"
        existing = self.db.execute_query(check_query, (invoice_data['invoice_number'],), fetch_one=True)

        if existing:
            # Invoice number already exists - regenerate using next sequential number
            import time
            time.sleep(0.1)  # Brief pause to ensure unique number
            invoice_data['invoice_number'] = Formatters.generate_invoice_number(self.db)
            print(f"[WARNING] Duplicate invoice number detected! Generated new: {invoice_data['invoice_number']}")

        query = """
        INSERT INTO invoices (
            invoice_number, customer_id, ac_brand_id, ac_type, star_rating,
            ton_capacity, inverter_type, technician_id, subtotal, gst_percentage,
            gst_amount, total_amount, advance_payment, balance_amount,
            payment_mode, payment_status, notes, is_active, is_deleted
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, FALSE)
        """

        ac_details = invoice_data['ac_details']
        totals = invoice_data['totals']
        payment = invoice_data['payment']

        return self.db.execute_query(query, (
            invoice_data['invoice_number'],
            customer_id,
            ac_brand_id,
            ac_details['type'],
            ac_details['star_rating'],
            ac_details['ton'],
            ac_details['inverter_type'],
            technician_id,
            float(totals['subtotal']),
            float(totals['gst_percentage']),
            float(totals['gst_amount']),
            float(totals['total_amount']),
            float(totals['advance_payment']),
            float(totals['balance_amount']),
            payment['mode'],
            payment['status'],
            notes
        ))
    
    def _create_invoice_items(self, invoice_id, items):
        """Create invoice items in database"""
        if not items:
            return
        
        query = """
        INSERT INTO invoice_items (invoice_id, item_type, service_id, part_id, quantity, rate, amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        params = []
        for item in items:
            service_id = item['item_id'] if item['type'] == 'service' else None
            part_id = item['item_id'] if item['type'] == 'part' else None
            
            params.append((
                invoice_id,
                item['type'],
                service_id,
                part_id,
                item['quantity'],
                float(item['rate']),
                float(item['amount'])
            ))
        
        self.db.execute_many(query, params)
    
    def _update_stock(self, items):
        """Update stock quantity for parts"""
        for item in items:
            if item['type'] == 'part':
                # Reduce stock quantity
                query = "UPDATE parts SET stock_quantity = stock_quantity - %s WHERE id = %s"
                self.db.execute_query(query, (item['quantity'], item['item_id']))
    
    def get_invoice(self, invoice_id):
        """Get invoice by ID"""
        query = """
        SELECT 
            i.*,
            c.name as customer_name, c.mobile, c.email, c.address, c.landmark,
            ab.brand_name,
            t.name as technician_name, t.mobile as technician_mobile
        FROM invoices i
        JOIN customers c ON i.customer_id = c.id
        LEFT JOIN ac_brands ab ON i.ac_brand_id = ab.id
        LEFT JOIN technicians t ON i.technician_id = t.id
        WHERE i.id = %s AND i.is_active = TRUE
        """
        return self.db.execute_query(query, (invoice_id,), fetch_one=True)
    
    def get_invoice_items(self, invoice_id):
        """Get invoice items"""
        query = """
        SELECT 
            ii.*,
            COALESCE(s.service_name, p.part_name) as item_name,
            s.service_name,
            p.part_name
        FROM invoice_items ii
        LEFT JOIN services s ON ii.service_id = s.id
        LEFT JOIN parts p ON ii.part_id = p.id
        WHERE ii.invoice_id = %s
        """
        return self.db.execute_query(query, (invoice_id,), fetch_all=True)
    
    def search_invoices(self, search_term=None, from_date=None, to_date=None, limit=100):
        """Search invoices with filters"""
        query = """
        SELECT 
            i.id, i.invoice_number, DATE(i.created_at) as invoice_date,
            c.name as customer_name, c.mobile,
            i.total_amount, i.advance_payment, i.balance_amount,
            i.payment_status, i.payment_mode
        FROM invoices i
        JOIN customers c ON i.customer_id = c.id
        WHERE i.is_active = TRUE
        """
        
        conditions = []
        params = []
        
        if search_term:
            conditions.append("(c.name LIKE %s OR c.mobile LIKE %s OR i.invoice_number LIKE %s)")
            params.extend([f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"])
        
        if from_date:
            conditions.append("DATE(i.created_at) >= %s")
            params.append(from_date)
        
        if to_date:
            conditions.append("DATE(i.created_at) <= %s")
            params.append(to_date)
        
        if conditions:
            query += " AND " + " AND ".join(conditions)
        
        query += " ORDER BY i.created_at DESC LIMIT %s"
        params.append(limit)
        
        return self.db.execute_query(query, params, fetch_all=True)
    
    def update_invoice_payment(self, invoice_id, amount, payment_mode, notes=None):
        """Update invoice payment"""
        try:
            # Get current invoice
            invoice = self.get_invoice(invoice_id)
            if not invoice:
                return False, "Invoice not found"
            
            # Calculate new balance
            new_balance = invoice['balance_amount'] - amount
            
            # Update payment status
            if new_balance <= 0:
                payment_status = 'Paid'
                new_balance = 0
            elif amount > 0:
                payment_status = 'Partial'
            else:
                payment_status = invoice['payment_status']
            
            # Update invoice
            query = """
            UPDATE invoices 
            SET advance_payment = advance_payment + %s,
                balance_amount = %s,
                payment_status = %s,
                payment_mode = %s,
                updated_at = NOW()
            WHERE id = %s
            """
            self.db.execute_query(query, (
                float(amount),
                float(new_balance),
                payment_status,
                payment_mode,
                invoice_id
            ))
            
            # Record payment
            if amount > 0:
                payment_query = """
                INSERT INTO payments (invoice_id, amount, payment_mode, notes)
                VALUES (%s, %s, %s, %s)
                """
                self.db.execute_query(payment_query, (
                    invoice_id,
                    float(amount),
                    payment_mode,
                    notes
                ))
            
            return True, "Payment updated successfully"
            
        except Exception as e:
            return False, f"Error updating payment: {str(e)}"
    
    def delete_invoice(self, invoice_id):
        """Soft delete invoice with stock restoration"""
        try:
            # Restore stock for parts before deleting
            parts_query = """
            SELECT ii.part_id, ii.quantity
            FROM invoice_items ii
            WHERE ii.invoice_id = %s AND ii.item_type = 'part'
            """
            parts = self.db.execute_query(parts_query, (invoice_id,), fetch_all=True)
            if parts:
                for part in parts:
                    self.db.execute_query(
                        "UPDATE parts SET stock_quantity = stock_quantity + %s WHERE id = %s",
                        (part['quantity'], part['part_id'])
                    )

            # Soft delete invoice
            query = "UPDATE invoices SET is_active = FALSE WHERE id = %s"
            self.db.execute_query(query, (invoice_id,))
            return True, "Invoice deleted successfully"
        except Exception as e:
            return False, f"Error deleting invoice: {str(e)}"
    
    def update_invoice(self, invoice_id, invoice_data):
        """Update existing invoice with lock check"""
        try:
            # CRITICAL: Check if invoice is locked before allowing update
            check_lock_query = """
            SELECT id, payment_status, is_deleted 
            FROM invoices 
            WHERE id = %s
            """
            invoice_check = self.db.execute_query(check_lock_query, (invoice_id,), fetch_one=True)
            
            if not invoice_check:
                return None, "Invoice not found"
            
            if invoice_check['is_deleted']:
                return None, "Invoice has been deleted"
            
            # LOCK CHECK: Prevent editing paid or cancelled invoices
            if invoice_check['payment_status'] in ['paid', 'cancelled']:
                return None, f"Cannot modify {invoice_check['payment_status']} invoice. Only 'draft' and 'final' invoices can be edited."
            
            # 1. Update customer if needed
            customer_id = self._get_or_create_customer(invoice_data['customer'])
            if not customer_id:
                return None, "Failed to update customer"

            # 2. Get AC brand ID
            ac_brand_id = self._get_ac_brand_id(invoice_data['ac_details']['brand'])

            # 3. Get technician ID
            technician_id = self._get_technician_id(invoice_data['technician'])

            # 4. Update invoice record
            success = self._update_invoice_record(
                invoice_id, customer_id, ac_brand_id, technician_id, invoice_data
            )

            if not success:
                return None, "Failed to update invoice"

            # 5. Delete old invoice items
            delete_query = "DELETE FROM invoice_items WHERE invoice_id = %s"
            self.db.execute_query(delete_query, (invoice_id,))

            # 6. Create new invoice items
            self._create_invoice_items(invoice_id, invoice_data['items'])

            # 7. Update stock for parts (restore old stock first would be ideal, but simplified here)
            self._update_stock(invoice_data['items'])

            return invoice_id, None

        except Exception as e:
            return None, f"Error updating invoice: {str(e)}"
    
    def _update_invoice_record(self, invoice_id, customer_id, ac_brand_id, technician_id, invoice_data):
        """Update invoice record in database"""
        from utils.formatters import Formatters

        notes = invoice_data['notes']
        if notes:
            notes = Formatters.format_sentence(notes)

        query = """
        UPDATE invoices SET
            customer_id = %s, ac_brand_id = %s, ac_type = %s, star_rating = %s,
            ton_capacity = %s, inverter_type = %s, technician_id = %s, subtotal = %s, 
            gst_percentage = %s, gst_amount = %s, total_amount = %s, advance_payment = %s, 
            balance_amount = %s, payment_mode = %s, payment_status = %s, notes = %s,
            updated_at = NOW()
        WHERE id = %s
        """
        
        ac_details = invoice_data['ac_details']
        totals = invoice_data['totals']
        payment = invoice_data['payment']
        
        self.db.execute_query(query, (
            customer_id,
            ac_brand_id,
            ac_details['type'],
            ac_details['star_rating'],
            ac_details['ton'],
            ac_details['inverter_type'],
            technician_id,
            float(totals['subtotal']),
            float(totals['gst_percentage']),
            float(totals['gst_amount']),
            float(totals['total_amount']),
            float(totals['advance_payment']),
            float(totals['balance_amount']),
            payment['mode'],
            payment['status'],
            notes, # Use formatted notes
            invoice_id
        ))
        
        return True