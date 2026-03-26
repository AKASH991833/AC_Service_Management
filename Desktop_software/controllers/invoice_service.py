"""
Invoice Service - Production Ready
Business logic for invoice operations with proper locking

INVOICE LOCKING RULES:
- 'draft': Can be edited and deleted
- 'final': Can be edited (not yet paid)
- 'paid': LOCKED - Read-only, cannot edit or delete
- 'cancelled': LOCKED - Read-only, cannot edit
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)


class InvoiceService:
    """Service layer for invoice management - Desktop Software"""

    def __init__(self, db_connection):
        self.db = db_connection

    def create_invoice(self, invoice_data: Dict[str, Any], items: List[Dict[str, Any]]) -> Tuple[Optional[int], Optional[str]]:
        """
        Create invoice with items atomically
        All or nothing transaction
        
        Returns: (invoice_id, error_message)
        """
        # Ensure connection exists
        if not hasattr(self.db, 'connection') or not self.db.connection:
            return None, "Database connection not available"

        # Disable autocommit for transaction
        original_autocommit = self.db.connection.autocommit
        self.db.connection.autocommit = False

        try:
            # 1. Validate customer exists
            customer_id = invoice_data.get('customer_id')
            customer_query = """
                SELECT id FROM customers 
                WHERE id = %s AND is_deleted = FALSE
            """
            customer = self.db.execute_query(customer_query, (customer_id,), fetch_one=True)
            
            if not customer:
                self.db.connection.rollback()
                return None, "Customer not found or deleted"

            # 2. Check for duplicate invoice number
            invoice_number = invoice_data.get('invoice_number')
            duplicate_query = """
                SELECT id FROM invoices 
                WHERE invoice_number = %s AND is_deleted = FALSE
            """
            existing = self.db.execute_query(duplicate_query, (invoice_number,), fetch_one=True)
            
            if existing:
                self.db.connection.rollback()
                return None, f"Invoice number {invoice_number} already exists"

            # 3. Create invoice record
            invoice_query = """
                INSERT INTO invoices (
                    invoice_number, customer_id, invoice_date, due_date,
                    ac_brand, ac_type, ac_model,
                    subtotal, discount, tax_percentage, tax_amount, total_amount,
                    paid_amount, balance_amount,
                    status, payment_mode, notes, created_by
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            invoice_params = (
                invoice_number,
                customer_id,
                invoice_data.get('invoice_date', datetime.now().date()),
                invoice_data.get('due_date'),
                invoice_data.get('ac_brand'),
                invoice_data.get('ac_type'),
                invoice_data.get('ac_model'),
                Decimal(str(invoice_data.get('subtotal', 0))),
                Decimal(str(invoice_data.get('discount', 0))),
                Decimal(str(invoice_data.get('tax_percentage', 18))),
                Decimal(str(invoice_data.get('tax_amount', 0))),
                Decimal(str(invoice_data['total_amount'])),
                Decimal(str(invoice_data.get('paid_amount', 0))),
                Decimal(str(invoice_data['balance_amount'])),
                invoice_data.get('status', 'draft'),
                invoice_data.get('payment_mode'),
                invoice_data.get('notes'),
                invoice_data.get('created_by')
            )
            
            invoice_id = self.db.execute_query(invoice_query, invoice_params)
            
            if not invoice_id:
                self.db.connection.rollback()
                return None, "Failed to create invoice"

            # 4. Create invoice items
            item_query = """
                INSERT INTO invoice_items (
                    invoice_id, item_type, service_id, part_id,
                    description, quantity, unit_price, total_price
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            for item in items:
                item_params = (
                    invoice_id,
                    item['item_type'],
                    item.get('service_id'),
                    item.get('part_id'),
                    item['description'],
                    item.get('quantity', 1),
                    Decimal(str(item['unit_price'])),
                    Decimal(str(item['total_price']))
                )
                self.db.execute_query(item_query, item_params)

            # Commit transaction
            self.db.connection.commit()
            
            logger.info(f"Invoice created: {invoice_number} (ID: {invoice_id})")
            return invoice_id, None

        except Exception as e:
            self.db.connection.rollback()
            logger.error(f"Error creating invoice: {e}")
            return None, f"Failed to create invoice: {str(e)}"

        finally:
            # Restore original autocommit setting
            try:
                self.db.connection.autocommit = original_autocommit
            except:
                pass

    def update_invoice(self, invoice_id: int, invoice_data: Dict[str, Any], 
                      items: List[Dict[str, Any]] = None) -> Tuple[bool, Optional[str]]:
        """
        Update invoice with lock check
        
        INVOICE LOCKING RULES:
        - 'draft': Can be edited and deleted
        - 'final': Can be edited (not yet paid)
        - 'paid': LOCKED - Read-only
        - 'cancelled': LOCKED - Read-only
        """
        try:
            # 1. Check if invoice exists and get status
            check_query = """
                SELECT id, status, is_deleted FROM invoices 
                WHERE id = %s
            """
            invoice = self.db.execute_query(check_query, (invoice_id,), fetch_one=True)
            
            if not invoice:
                return False, "Invoice not found"
            
            if invoice['is_deleted']:
                return False, "Invoice has been deleted"

            # 2. CRITICAL: Check if invoice is locked (paid or cancelled)
            if invoice['status'] in ['paid', 'cancelled']:
                return False, f"Cannot modify {invoice['status'].upper()} invoice. Only 'draft' and 'final' invoices can be edited."

            # 3. Update invoice fields
            update_fields = []
            params = []
            
            allowed_fields = [
                'customer_id', 'invoice_date', 'due_date',
                'ac_brand', 'ac_type', 'ac_model',
                'subtotal', 'discount', 'tax_percentage', 'tax_amount',
                'total_amount', 'paid_amount', 'balance_amount',
                'payment_mode', 'notes'
            ]
            
            for field in allowed_fields:
                if field in invoice_data:
                    update_fields.append(f"{field} = %s")
                    params.append(invoice_data[field])
            
            # Add updated_at
            update_fields.append("updated_at = NOW()")
            
            params.append(invoice_id)
            
            update_query = f"""
                UPDATE invoices 
                SET {', '.join(update_fields)}
                WHERE id = %s
            """
            
            self.db.execute_query(update_query, tuple(params))

            # 4. Update items if provided
            if items is not None:
                # Delete existing items
                delete_query = "DELETE FROM invoice_items WHERE invoice_id = %s"
                self.db.execute_query(delete_query, (invoice_id,))
                
                # Create new items
                item_query = """
                    INSERT INTO invoice_items (
                        invoice_id, item_type, service_id, part_id,
                        description, quantity, unit_price, total_price
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                for item in items:
                    item_params = (
                        invoice_id,
                        item['item_type'],
                        item.get('service_id'),
                        item.get('part_id'),
                        item['description'],
                        item.get('quantity', 1),
                        Decimal(str(item['unit_price'])),
                        Decimal(str(item['total_price']))
                    )
                    self.db.execute_query(item_query, item_params)

            logger.info(f"Invoice {invoice_id} updated successfully")
            return True, None

        except Exception as e:
            logger.error(f"Error updating invoice: {e}")
            return False, str(e)

    def mark_as_paid(self, invoice_id: int, payment_amount: Decimal) -> Tuple[bool, Optional[str]]:
        """
        Mark invoice as paid - LOCKS the invoice
        
        Once paid, invoice becomes READ-ONLY and cannot be modified.
        """
        try:
            # 1. Check if invoice exists
            check_query = """
                SELECT id, status, total_amount, is_deleted FROM invoices 
                WHERE id = %s
            """
            invoice = self.db.execute_query(check_query, (invoice_id,), fetch_one=True)
            
            if not invoice:
                return False, "Invoice not found"
            
            if invoice['is_deleted']:
                return False, "Invoice has been deleted"

            # 2. Check if already locked
            if invoice['status'] in ['paid', 'cancelled']:
                return False, f"Cannot modify {invoice['status'].upper()} invoice. Invoice is locked."

            # 3. Validate payment amount
            if payment_amount < invoice['total_amount']:
                return False, f"Payment amount ({payment_amount}) is less than total ({invoice['total_amount']})"

            # 4. Update payment and lock invoice
            update_query = """
                UPDATE invoices 
                SET paid_amount = %s, 
                    balance_amount = 0,
                    status = 'paid',
                    updated_at = NOW()
                WHERE id = %s
            """
            
            self.db.execute_query(update_query, (Decimal(str(payment_amount)), invoice_id))

            logger.info(f"Invoice {invoice_id} marked as PAID (LOCKED)")
            return True, None

        except Exception as e:
            logger.error(f"Error marking invoice as paid: {e}")
            return False, str(e)

    def cancel_invoice(self, invoice_id: int) -> Tuple[bool, Optional[str]]:
        """
        Cancel invoice - LOCKS the invoice
        
        Once cancelled, invoice becomes READ-ONLY.
        """
        try:
            # 1. Check if invoice exists
            check_query = """
                SELECT id, status, is_deleted FROM invoices 
                WHERE id = %s
            """
            invoice = self.db.execute_query(check_query, (invoice_id,), fetch_one=True)
            
            if not invoice:
                return False, "Invoice not found"
            
            if invoice['is_deleted']:
                return False, "Invoice has been deleted"

            # 2. Check if already locked
            if invoice['status'] in ['paid', 'cancelled']:
                return False, f"Cannot cancel {invoice['status'].upper()} invoice. Invoice is locked."

            # 3. Cancel invoice
            update_query = """
                UPDATE invoices 
                SET status = 'cancelled',
                    updated_at = NOW()
                WHERE id = %s
            """
            
            self.db.execute_query(update_query, (invoice_id,))

            logger.info(f"Invoice {invoice_id} CANCELLED (LOCKED)")
            return True, None

        except Exception as e:
            logger.error(f"Error cancelling invoice: {e}")
            return False, str(e)

    def soft_delete(self, invoice_id: int) -> Tuple[bool, Optional[str]]:
        """
        Soft delete invoice
        
        DELETION RULES:
        - 'draft': Can be deleted
        - 'final': Cannot delete (must cancel first)
        - 'paid': CANNOT delete (locked for audit trail)
        - 'cancelled': Cannot delete (already cancelled)
        """
        try:
            # 1. Check if invoice exists
            check_query = """
                SELECT id, status, is_deleted FROM invoices 
                WHERE id = %s
            """
            invoice = self.db.execute_query(check_query, (invoice_id,), fetch_one=True)
            
            if not invoice:
                return False, "Invoice not found"
            
            if invoice['is_deleted']:
                return False, "Invoice already deleted"

            # 2. Check deletion rules
            if invoice['status'] == 'paid':
                return False, "Cannot delete PAID invoices. Paid invoices must be retained for audit trail."
            
            if invoice['status'] == 'cancelled':
                return False, "Cannot delete CANCELLED invoices. Already cancelled."
            
            if invoice['status'] == 'final':
                return False, "Cannot delete FINAL invoices. Please cancel the invoice first."

            # 3. Soft delete
            delete_query = """
                UPDATE invoices 
                SET is_deleted = TRUE,
                    deleted_at = NOW()
                WHERE id = %s
            """
            
            self.db.execute_query(delete_query, (invoice_id,))

            logger.info(f"Invoice {invoice_id} soft deleted")
            return True, None

        except Exception as e:
            logger.error(f"Error soft deleting invoice: {e}")
            return False, str(e)

    def get_invoice(self, invoice_id: int) -> Optional[Dict[str, Any]]:
        """Get invoice by ID with customer and items"""
        try:
            # Get invoice details
            invoice_query = """
                SELECT i.*, c.name as customer_name, c.phone as customer_phone,
                       c.email as customer_email, c.address as customer_address
                FROM invoices i
                LEFT JOIN customers c ON i.customer_id = c.id
                WHERE i.id = %s AND i.is_deleted = FALSE
            """
            
            invoice = self.db.execute_query(invoice_query, (invoice_id,), fetch_one=True)
            
            if not invoice:
                return None

            # Get invoice items
            items_query = """
                SELECT * FROM invoice_items
                WHERE invoice_id = %s
                ORDER BY id
            """
            
            items = self.db.execute_query(items_query, (invoice_id,), fetch_all=True)
            
            invoice['items'] = items or []
            return invoice

        except Exception as e:
            logger.error(f"Error getting invoice: {e}")
            return None

    def get_all_invoices(self, status: str = None, customer_id: int = None, 
                        limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get invoices with optional filtering"""
        try:
            # Build query dynamically based on filters
            base_query = """
                SELECT i.*, c.name as customer_name, c.phone as customer_phone
                FROM invoices i
                LEFT JOIN customers c ON i.customer_id = c.id
                WHERE i.is_deleted = FALSE
            """
            
            params = []
            filters = []
            
            if status:
                filters.append("i.status = %s")
                params.append(status)
            
            if customer_id:
                filters.append("i.customer_id = %s")
                params.append(customer_id)
            
            if filters:
                base_query += " AND " + " AND ".join(filters)
            
            base_query += " ORDER BY i.created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            invoices = self.db.execute_query(base_query, tuple(params), fetch_all=True)
            
            return invoices or []

        except Exception as e:
            logger.error(f"Error getting invoices: {e}")
            return []
