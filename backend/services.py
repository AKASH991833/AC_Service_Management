"""
Service Layer - Business Logic
Separates business logic from routes for better maintainability
"""

from models import db, ServiceRequest, ContactMessage, Customer, Invoice, InvoiceItem
from models import Technician, AMCContract, AMCUnit, Service, Product, Testimonial
from datetime import datetime, date, timezone
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
            one_hour_ago = datetime.now(timezone.utc)
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
            request = db.session.get(ServiceRequest, request_id)
            if not request:
                return False, "Request not found"
            
            valid_statuses = ['Pending', 'In Progress', 'Completed', 'Cancelled']
            if new_status not in valid_statuses:
                return False, f"Invalid status. Must be one of: {valid_statuses}"
            
            request.request_status = new_status
            request.updated_at = datetime.now(timezone.utc)
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
            request = db.session.get(ServiceRequest, request_id)
            if not request:
                return False, "Request not found"
            
            request.is_deleted = True
            request.deleted_at = datetime.now(timezone.utc)
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
            message = db.session.get(ContactMessage, message_id)
            if not message:
                return False, "Message not found"
            
            message.status = 'read'
            message.updated_at = datetime.now(timezone.utc)
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
            # Validate required fields
            name = data.get('name', '').strip() if data.get('name') else ''
            mobile = data.get('mobile', data.get('phone', '')).replace(' ', '')
            
            if not name:
                return None, "Customer name is required"
            if len(name) < 2:
                return None, "Customer name must be at least 2 characters"
            if not mobile:
                return None, "Customer mobile number is required"
            
            # Check for existing customer by mobile
            existing = Customer.query.filter_by(mobile=mobile, is_active=True).first()
            
            if existing:
                return None, f"Customer with mobile {mobile} already exists"
            
            customer = Customer(
                name=name,
                mobile=mobile,
                email=data.get('email', '').strip() if data.get('email') else None,
                address=data.get('address', '').strip() if data.get('address') else None,
                landmark=data.get('landmark', '').strip() if data.get('landmark') else None
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
            customer = db.session.get(Customer, customer_id)
            if not customer or not customer.is_active:
                return None, "Customer not found"
            
            # Update fields
            if 'name' in data:
                customer.name = data['name'].strip()
            if 'mobile' in data or 'phone' in data:
                new_mobile = (data.get('mobile') or data.get('phone', '')).replace(' ', '')
                if new_mobile:
                    customer.mobile = new_mobile
            if 'email' in data:
                customer.email = data['email'].strip() if data['email'] else None
            if 'address' in data:
                customer.address = data['address'].strip() if data['address'] else None
            if 'landmark' in data:
                customer.landmark = data['landmark'].strip() if data['landmark'] else None
            
            customer.updated_at = datetime.now(timezone.utc)
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
            customer = db.session.get(Customer, customer_id)
            if not customer or not customer.is_active:
                return False, "Customer not found"
            
            customer.is_active = False
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
            mobile=phone.replace(' ', ''),
            is_active=True
        ).first()


class InvoiceService:
    """Service layer for invoice management with transaction support"""
    
    @staticmethod
    def create_invoice(invoice_data: Dict[str, Any], items: List[Dict[str, Any]]) -> Tuple[Optional[Invoice], Optional[str]]:
        """Create invoice with items atomically - matches MySQL schema"""
        try:
            # Validate customer exists
            customer = Customer.query.filter_by(id=invoice_data['customer_id'], is_active=True).first()
            if not customer:
                return None, "Customer not found"
            
            # Check for duplicate invoice number
            existing = Invoice.query.filter_by(
                invoice_number=invoice_data['invoice_number'],
                is_active=True
            ).first()
            
            if existing:
                return None, f"Invoice number {invoice_data['invoice_number']} already exists"
            
            # Create invoice
            invoice = Invoice(
                invoice_number=invoice_data['invoice_number'],
                customer_id=invoice_data['customer_id'],
                ac_brand_id=invoice_data.get('ac_brand_id'),
                ac_type=invoice_data.get('ac_type', 'Split'),
                star_rating=invoice_data.get('star_rating'),
                ton_capacity=invoice_data.get('ton_capacity'),
                inverter_type=invoice_data.get('inverter_type', 'Not Specified'),
                technician_id=invoice_data.get('technician_id'),
                subtotal=Decimal(str(invoice_data.get('subtotal', 0))),
                gst_percentage=Decimal(str(invoice_data.get('gst_percentage', 18))),
                gst_amount=Decimal(str(invoice_data.get('gst_amount', 0))),
                total_amount=Decimal(str(invoice_data['total_amount'])),
                advance_payment=Decimal(str(invoice_data.get('advance_payment', 0))),
                balance_amount=Decimal(str(invoice_data.get('balance_amount', 0))),
                payment_mode=invoice_data.get('payment_mode', 'Pending'),
                payment_status=invoice_data.get('payment_status', 'Pending'),
                notes=invoice_data.get('notes')
            )
            
            db.session.add(invoice)
            db.session.flush()
            
            # Create invoice items
            for item_data in items:
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    item_type=item_data.get('item_type', 'service'),
                    service_id=item_data.get('service_id'),
                    part_id=item_data.get('part_id'),
                    quantity=item_data.get('quantity', 1),
                    rate=Decimal(str(item_data.get('rate', item_data.get('unit_price', 0)))),
                    amount=Decimal(str(item_data.get('amount', item_data.get('total_price', 0))))
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
        """Update invoice with lock check - matches MySQL schema"""
        try:
            invoice = db.session.get(Invoice, invoice_id)
            if not invoice or not invoice.is_active:
                return None, "Invoice not found"

            # Check if invoice is locked (paid)
            if invoice.payment_status == 'Paid':
                return None, "Cannot modify PAID invoice. Invoice is locked."

            # Update fields
            if 'customer_id' in invoice_data:
                customer = db.session.get(Customer, invoice_data['customer_id'])
                if not customer:
                    return None, "Customer not found"
                invoice.customer_id = invoice_data['customer_id']
            
            if 'ac_brand_id' in invoice_data:
                invoice.ac_brand_id = invoice_data['ac_brand_id']
            if 'ac_type' in invoice_data:
                invoice.ac_type = invoice_data['ac_type']
            if 'star_rating' in invoice_data:
                invoice.star_rating = invoice_data['star_rating']
            if 'ton_capacity' in invoice_data:
                invoice.ton_capacity = invoice_data['ton_capacity']
            if 'inverter_type' in invoice_data:
                invoice.inverter_type = invoice_data['inverter_type']
            if 'technician_id' in invoice_data:
                invoice.technician_id = invoice_data['technician_id']
            
            if 'subtotal' in invoice_data:
                invoice.subtotal = Decimal(str(invoice_data['subtotal']))
            if 'gst_percentage' in invoice_data:
                invoice.gst_percentage = Decimal(str(invoice_data['gst_percentage']))
            if 'gst_amount' in invoice_data:
                invoice.gst_amount = Decimal(str(invoice_data['gst_amount']))
            if 'total_amount' in invoice_data:
                invoice.total_amount = Decimal(str(invoice_data['total_amount']))
            if 'advance_payment' in invoice_data:
                invoice.advance_payment = Decimal(str(invoice_data['advance_payment']))
            if 'balance_amount' in invoice_data:
                invoice.balance_amount = Decimal(str(invoice_data['balance_amount']))
            if 'payment_status' in invoice_data:
                invoice.payment_status = invoice_data['payment_status']
            if 'payment_mode' in invoice_data:
                invoice.payment_mode = invoice_data['payment_mode']
            if 'notes' in invoice_data:
                invoice.notes = invoice_data['notes']
            
            invoice.updated_at = datetime.now(timezone.utc)
            
            # Update items if provided
            if items is not None:
                # Delete existing items
                InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()
                
                # Create new items
                for item_data in items:
                    item = InvoiceItem(
                        invoice_id=invoice.id,
                        item_type=item_data.get('item_type', 'service'),
                        service_id=item_data.get('service_id'),
                        part_id=item_data.get('part_id'),
                        quantity=item_data.get('quantity', 1),
                        rate=Decimal(str(item_data.get('rate', item_data.get('unit_price', 0)))),
                        amount=Decimal(str(item_data.get('amount', item_data.get('total_price', 0))))
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
        """Mark invoice as paid - locks the invoice"""
        try:
            invoice = db.session.get(Invoice, invoice_id)
            if not invoice or not invoice.is_active:
                return False, "Invoice not found"

            # Check if already locked
            if invoice.payment_status == 'Paid':
                return False, "Cannot modify PAID invoice. Invoice is locked."

            # Validate payment amount
            if payment_amount < invoice.total_amount:
                return False, f"Payment amount ({payment_amount}) is less than total ({invoice.total_amount})"

            # Update payment and lock invoice
            invoice.advance_payment = payment_amount
            invoice.balance_amount = Decimal('0')
            invoice.payment_status = 'Paid'
            invoice.payment_mode = invoice.payment_mode if invoice.payment_mode != 'Pending' else 'Cash'
            invoice.updated_at = datetime.now(timezone.utc)

            db.session.commit()

            logger.info(f"Invoice {invoice_id} marked as PAID (LOCKED)")
            return True, None

        except Exception as e:
            db.session.rollback()
            return False, str(e)
    
    @staticmethod
    def soft_delete(invoice_id: int) -> Tuple[bool, Optional[str]]:
        """Soft delete invoice - matches MySQL schema"""
        try:
            invoice = db.session.get(Invoice, invoice_id)
            if not invoice or not invoice.is_active:
                return False, "Invoice not found"

            # Don't allow deleting paid invoices
            if invoice.payment_status == 'Paid':
                return False, "Cannot delete PAID invoices. Must be retained for audit trail."

            invoice.is_active = False
            db.session.commit()

            logger.info(f"Invoice {invoice_id} soft deleted")
            return True, None

        except Exception as e:
            db.session.rollback()
            return False, str(e)
