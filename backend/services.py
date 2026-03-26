"""
Service Layer - Business Logic
Separates business logic from routes for better maintainability
"""

from models import db, ServiceRequest, ContactMessage, Customer, Invoice, InvoiceItem
from models import Technician, AMCContract, AMCUnit, Service, Product, Testimonial
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)


class ServiceRequestService:
    """Service layer for service requests"""
    
    @staticmethod
    def create_request(data: Dict[str, Any], ip_address: str = None, user_agent: str = None) -> Tuple[Optional[ServiceRequest], Optional[str]]:
        """
        Create a new service request
        Returns: (request_object, error_message)
        """
        try:
            # Validate phone format
            phone = data.get('phone', '').replace(' ', '')
            if not phone or len(phone) < 10:
                return None, "Invalid phone number"
            
            # Check for duplicate recent requests (same phone within 1 hour)
            one_hour_ago = datetime.utcnow()
            from datetime import timedelta
            one_hour_ago = one_hour_ago - timedelta(hours=1)
            
            recent = ServiceRequest.query.filter(
                ServiceRequest.customer_phone == phone,
                ServiceRequest.created_at >= one_hour_ago
            ).first()
            
            if recent:
                return None, "You have already submitted a request recently. Please wait before submitting again."
            
            # Create request
            request = ServiceRequest(
                customer_name=data['name'].strip(),
                customer_phone=phone,
                customer_email=data.get('email', '').strip() if data.get('email') else None,
                customer_address=data['address'].strip(),
                service_type=data['service_type'],
                ac_type=data.get('ac_type', 'Not Specified'),
                preferred_date=data.get('preferred_date'),
                time_slot=data.get('time_slot', 'Not Specified'),
                message=data.get('message', '').strip() if data.get('message') else None,
                source='Website',
                ip_address=ip_address,
                user_agent=user_agent[:500] if user_agent else None
            )
            
            db.session.add(request)
            db.session.commit()
            
            logger.info(f"Service request created: ID={request.id}, Phone={phone}")
            return request, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating service request: {e}")
            return None, f"Failed to create request: {str(e)}"
    
    @staticmethod
    def get_requests(status: str = None, limit: int = 50, offset: int = 0) -> List[ServiceRequest]:
        """Get service requests with optional filtering"""
        query = ServiceRequest.query.filter_by(is_deleted=False)
        
        if status:
            query = query.filter_by(request_status=status)
        
        return query.order_by(
            ServiceRequest.created_at.desc()
        ).offset(offset).limit(limit).all()
    
    @staticmethod
    def update_status(request_id: int, new_status: str) -> Tuple[bool, Optional[str]]:
        """Update service request status"""
        try:
            request = ServiceRequest.query.get(request_id)
            if not request:
                return False, "Request not found"
            
            valid_statuses = ['Pending', 'In Progress', 'Completed', 'Cancelled']
            if new_status not in valid_statuses:
                return False, f"Invalid status. Must be one of: {valid_statuses}"
            
            request.request_status = new_status
            request.updated_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Request {request_id} status updated to {new_status}")
            return True, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating request status: {e}")
            return False, str(e)
    
    @staticmethod
    def soft_delete(request_id: int) -> Tuple[bool, Optional[str]]:
        """Soft delete a service request"""
        try:
            request = ServiceRequest.query.get(request_id)
            if not request:
                return False, "Request not found"
            
            request.is_deleted = True
            request.deleted_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Request {request_id} soft deleted")
            return True, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error soft deleting request: {e}")
            return False, str(e)


class ContactMessageService:
    """Service layer for contact messages"""
    
    @staticmethod
    def create_message(data: Dict[str, Any], ip_address: str = None, user_agent: str = None) -> Tuple[Optional[ContactMessage], Optional[str]]:
        """Create a new contact message"""
        try:
            phone = data.get('phone', '').replace(' ', '')
            if not phone or len(phone) < 10:
                return None, "Invalid phone number"
            
            message = ContactMessage(
                name=data['name'].strip(),
                phone=phone,
                email=data.get('email', '').strip() if data.get('email') else None,
                address=data.get('address', '').strip() if data.get('address') else None,
                service_type=data['service_type'],
                ac_type=data.get('ac_type', 'Not Specified'),
                message=data.get('message', '').strip() if data.get('message') else None,
                source='Website',
                ip_address=ip_address,
                user_agent=user_agent[:500] if user_agent else None
            )
            
            db.session.add(message)
            db.session.commit()
            
            logger.info(f"Contact message created: ID={message.id}")
            return message, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating contact message: {e}")
            return None, f"Failed to create message: {str(e)}"
    
    @staticmethod
    def mark_as_read(message_id: int) -> Tuple[bool, Optional[str]]:
        """Mark message as read"""
        try:
            message = ContactMessage.query.get(message_id)
            if not message:
                return False, "Message not found"
            
            message.status = 'read'
            message.updated_at = datetime.utcnow()
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)


class CustomerService:
    """Service layer for customer management"""
    
    @staticmethod
    def create_customer(data: Dict[str, Any]) -> Tuple[Optional[Customer], Optional[str]]:
        """Create a new customer"""
        try:
            # Check for existing customer by phone
            phone = data['phone'].replace(' ', '')
            existing = Customer.query.filter_by(phone=phone, is_deleted=False).first()
            
            if existing:
                return None, f"Customer with phone {phone} already exists"
            
            customer = Customer(
                name=data['name'].strip(),
                phone=phone,
                email=data.get('email', '').strip() if data.get('email') else None,
                customer_type=data.get('customer_type', 'Regular'),
                address=data.get('address', '').strip() if data.get('address') else None,
                city=data.get('city', '').strip() if data.get('city') else None,
                pincode=data.get('pincode', '').strip() if data.get('pincode') else None,
                notes=data.get('notes', '').strip() if data.get('notes') else None
            )
            
            db.session.add(customer)
            db.session.commit()
            
            logger.info(f"Customer created: ID={customer.id}")
            return customer, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating customer: {e}")
            return None, f"Failed to create customer: {str(e)}"
    
    @staticmethod
    def update_customer(customer_id: int, data: Dict[str, Any]) -> Tuple[Optional[Customer], Optional[str]]:
        """Update customer details"""
        try:
            customer = Customer.query.get(customer_id)
            if not customer or customer.is_deleted:
                return None, "Customer not found"
            
            # Update fields
            if 'name' in data:
                customer.name = data['name'].strip()
            if 'email' in data:
                customer.email = data['email'].strip() if data['email'] else None
            if 'customer_type' in data:
                customer.customer_type = data['customer_type']
            if 'address' in data:
                customer.address = data['address'].strip() if data['address'] else None
            if 'city' in data:
                customer.city = data['city'].strip() if data['city'] else None
            if 'pincode' in data:
                customer.pincode = data['pincode'].strip() if data['pincode'] else None
            if 'notes' in data:
                customer.notes = data['notes'].strip() if data['notes'] else None
            
            customer.updated_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Customer {customer_id} updated")
            return customer, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating customer: {e}")
            return None, str(e)
    
    @staticmethod
    def soft_delete(customer_id: int) -> Tuple[bool, Optional[str]]:
        """Soft delete a customer"""
        try:
            customer = Customer.query.get(customer_id)
            if not customer or customer.is_deleted:
                return False, "Customer not found"
            
            customer.is_deleted = True
            customer.deleted_at = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Customer {customer_id} soft deleted")
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def get_customer_by_phone(phone: str) -> Optional[Customer]:
        """Get customer by phone number"""
        return Customer.query.filter_by(
            phone=phone.replace(' ', ''),
            is_deleted=False
        ).first()


class InvoiceService:
    """Service layer for invoice management with transaction support"""
    
    @staticmethod
    def create_invoice(invoice_data: Dict[str, Any], items: List[Dict[str, Any]]) -> Tuple[Optional[Invoice], Optional[str]]:
        """
        Create invoice with items atomically
        All or nothing transaction
        """
        try:
            # Validate customer exists
            customer = Customer.query.get(invoice_data['customer_id'])
            if not customer or customer.is_deleted:
                return None, "Customer not found"
            
            # Check for duplicate invoice number
            existing = Invoice.query.filter_by(
                invoice_number=invoice_data['invoice_number']
            ).first()
            
            if existing:
                return None, f"Invoice number {invoice_data['invoice_number']} already exists"
            
            # Create invoice
            invoice = Invoice(
                invoice_number=invoice_data['invoice_number'],
                customer_id=invoice_data['customer_id'],
                invoice_date=invoice_data.get('invoice_date', date.today()),
                due_date=invoice_data.get('due_date'),
                ac_brand=invoice_data.get('ac_brand'),
                ac_type=invoice_data.get('ac_type'),
                ac_model=invoice_data.get('ac_model'),
                subtotal=Decimal(str(invoice_data.get('subtotal', 0))),
                discount=Decimal(str(invoice_data.get('discount', 0))),
                tax_percentage=Decimal(str(invoice_data.get('tax_percentage', 18))),
                tax_amount=Decimal(str(invoice_data.get('tax_amount', 0))),
                total_amount=Decimal(str(invoice_data['total_amount'])),
                paid_amount=Decimal(str(invoice_data.get('paid_amount', 0))),
                balance_amount=Decimal(str(invoice_data['balance_amount'])),
                status=invoice_data.get('status', 'draft'),
                payment_mode=invoice_data.get('payment_mode'),
                notes=invoice_data.get('notes'),
                created_by=invoice_data.get('created_by')
            )
            
            db.session.add(invoice)
            db.session.flush()  # Get invoice ID
            
            # Create invoice items
            for item_data in items:
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    item_type=item_data['item_type'],
                    service_id=item_data.get('service_id'),
                    part_id=item_data.get('part_id'),
                    description=item_data['description'],
                    quantity=item_data.get('quantity', 1),
                    unit_price=Decimal(str(item_data['unit_price'])),
                    total_price=Decimal(str(item_data['total_price']))
                )
                db.session.add(item)
            
            db.session.commit()
            
            logger.info(f"Invoice created: {invoice.invoice_number}")
            return invoice, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating invoice: {e}")
            return None, f"Failed to create invoice: {str(e)}"
    
    @staticmethod
    def update_invoice(invoice_id: int, invoice_data: Dict[str, Any],
                      items: List[Dict[str, Any]] = None) -> Tuple[Optional[Invoice], Optional[str]]:
        """
        Update invoice with lock check
        
        INVOICE LOCKING RULES:
        - 'draft': Can be edited and deleted
        - 'final': Can be edited (not yet paid)
        - 'paid': LOCKED - Read-only
        - 'cancelled': LOCKED - Read-only
        """
        try:
            invoice = Invoice.query.get(invoice_id)
            if not invoice or invoice.is_deleted:
                return None, "Invoice not found"

            # CRITICAL: Check if invoice is locked (paid or cancelled)
            if invoice.status in ['paid', 'cancelled']:
                return None, f"Cannot modify {invoice.status.upper()} invoice. Only 'draft' and 'final' invoices can be edited."

            # Update fields
            if 'customer_id' in invoice_data:
                customer = Customer.query.get(invoice_data['customer_id'])
                if not customer:
                    return None, "Customer not found"
                invoice.customer_id = invoice_data['customer_id']
            
            if 'invoice_date' in invoice_data:
                invoice.invoice_date = invoice_data['invoice_date']
            if 'due_date' in invoice_data:
                invoice.due_date = invoice_data['due_date']
            if 'ac_brand' in invoice_data:
                invoice.ac_brand = invoice_data['ac_brand']
            if 'ac_type' in invoice_data:
                invoice.ac_type = invoice_data['ac_type']
            if 'ac_model' in invoice_data:
                invoice.ac_model = invoice_data['ac_model']
            
            if 'subtotal' in invoice_data:
                invoice.subtotal = Decimal(str(invoice_data['subtotal']))
            if 'discount' in invoice_data:
                invoice.discount = Decimal(str(invoice_data['discount']))
            if 'tax_percentage' in invoice_data:
                invoice.tax_percentage = Decimal(str(invoice_data['tax_percentage']))
            if 'tax_amount' in invoice_data:
                invoice.tax_amount = Decimal(str(invoice_data['tax_amount']))
            if 'total_amount' in invoice_data:
                invoice.total_amount = Decimal(str(invoice_data['total_amount']))
            if 'paid_amount' in invoice_data:
                invoice.paid_amount = Decimal(str(invoice_data['paid_amount']))
            if 'balance_amount' in invoice_data:
                invoice.balance_amount = Decimal(str(invoice_data['balance_amount']))
            if 'status' in invoice_data:
                # Validate status transition
                valid_transitions = {
                    'draft': ['final', 'cancelled'],
                    'final': ['paid', 'cancelled'],
                    'paid': [],  # Locked
                    'cancelled': []  # Locked
                }
                new_status = invoice_data['status']
                if new_status not in valid_transitions.get(invoice.status, []):
                    return None, f"Cannot transition from {invoice.status} to {new_status}"
                invoice.status = new_status
            if 'payment_mode' in invoice_data:
                invoice.payment_mode = invoice_data['payment_mode']
            if 'notes' in invoice_data:
                invoice.notes = invoice_data['notes']
            
            invoice.updated_at = datetime.utcnow()
            
            # Update items if provided
            if items is not None:
                # Delete existing items
                InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()
                
                # Create new items
                for item_data in items:
                    item = InvoiceItem(
                        invoice_id=invoice.id,
                        item_type=item_data['item_type'],
                        service_id=item_data.get('service_id'),
                        part_id=item_data.get('part_id'),
                        description=item_data['description'],
                        quantity=item_data.get('quantity', 1),
                        unit_price=Decimal(str(item_data['unit_price'])),
                        total_price=Decimal(str(item_data['total_price']))
                    )
                    db.session.add(item)
            
            db.session.commit()
            
            logger.info(f"Invoice {invoice_id} updated")
            return invoice, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating invoice: {e}")
            return None, str(e)
    
    @staticmethod
    def mark_as_paid(invoice_id: int, payment_amount: Decimal) -> Tuple[bool, Optional[str]]:
        """
        Mark invoice as paid - LOCKS the invoice
        
        Once paid, invoice becomes READ-ONLY and cannot be modified.
        """
        try:
            invoice = Invoice.query.get(invoice_id)
            if not invoice or invoice.is_deleted:
                return False, "Invoice not found"

            # Check if already locked
            if invoice.status in ['paid', 'cancelled']:
                return False, f"Cannot modify {invoice.status.upper()} invoice. Invoice is locked."

            # Validate payment amount
            if payment_amount < invoice.total_amount:
                return False, f"Payment amount ({payment_amount}) is less than total ({invoice.total_amount})"

            # Update payment and lock invoice
            invoice.paid_amount = payment_amount
            invoice.balance_amount = Decimal('0')
            invoice.status = 'paid'  # This LOCKS the invoice
            invoice.updated_at = datetime.utcnow()

            db.session.commit()

            logger.info(f"Invoice {invoice_id} marked as PAID (LOCKED)")
            return True, None

        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def soft_delete(invoice_id: int) -> Tuple[bool, Optional[str]]:
        """
        Soft delete invoice
        
        DELETION RULES:
        - 'draft': Can be deleted
        - 'final': Cannot delete (must cancel first)
        - 'paid': CANNOT delete (locked for audit trail)
        - 'cancelled': Cannot delete (already cancelled)
        """
        try:
            invoice = Invoice.query.get(invoice_id)
            if not invoice or invoice.is_deleted:
                return False, "Invoice not found"

            # CRITICAL: Don't allow deleting paid invoices - audit trail requirement
            if invoice.status == 'paid':
                return False, "Cannot delete PAID invoices. Paid invoices must be retained for audit trail."
            
            # Don't allow deleting cancelled invoices
            if invoice.status == 'cancelled':
                return False, "Cannot delete CANCELLED invoices. Already cancelled."
            
            # Final invoices should be cancelled first
            if invoice.status == 'final':
                return False, "Cannot delete FINAL invoices. Please cancel the invoice first."

            invoice.is_deleted = True
            invoice.deleted_at = datetime.utcnow()
            db.session.commit()

            logger.info(f"Invoice {invoice_id} soft deleted")
            return True, None

        except Exception as e:
            db.session.rollback()
            return False, str(e)
