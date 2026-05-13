"""
Management Routes - Customers, Technicians, Invoices, AMC
CRUD operations for all management modules
"""

from flask import Blueprint, request, jsonify
from models import db, Customer, Technician, Invoice, InvoiceItem, AMCContract, AMCUnit
from security import require_admin_enhanced, sanitize_input
import logging
from datetime import datetime, timezone
import secrets
import re

logger = logging.getLogger(__name__)

mgmt_bp = Blueprint('management', __name__)
require_admin = require_admin_enhanced


# ========================================
# CUSTOMER MANAGEMENT
# ========================================

@mgmt_bp.route('/customers', methods=['GET'])
@require_admin
def get_customers():
    """Get all customers"""
    try:
        customers = Customer.query.filter_by(is_active=True).order_by(Customer.created_at.desc()).all()
        return jsonify({"success": True, "data": [c.to_dict() for c in customers]}), 200
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch customers"}), 500


@mgmt_bp.route('/customers/<int:id>', methods=['GET'])
@require_admin
def get_customer(id):
    """Get single customer"""
    try:
        customer = db.session.get(Customer, id)
        if not customer:
            return jsonify({"success": False, "message": "Customer not found"}), 404
        return jsonify({"success": True, "data": customer.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error fetching customer: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch customer"}), 500


@mgmt_bp.route('/customers', methods=['POST'])
@require_admin
def create_customer():
    """Create new customer"""
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('mobile'):
            return jsonify({"success": False, "message": "Name and mobile are required"}), 400
        
        name = sanitize_input(data['name'].strip(), max_length=100)
        mobile = re.sub(r'[\s\-\(\)\+]', '', data['mobile'].strip())
        
        if not re.match(r'^[6-9]\d{9}$', mobile):
            return jsonify({"success": False, "message": "Invalid mobile number"}), 400
        
        existing = Customer.query.filter_by(mobile=mobile).first()
        if existing:
            return jsonify({"success": False, "message": "Customer with this mobile number already exists"}), 400
        
        customer = Customer(
            name=name,
            mobile=mobile,
            email=sanitize_input(data.get('email', '').strip(), max_length=100) or None,
            address=sanitize_input(data.get('address', '').strip(), max_length=500) or None,
            landmark=sanitize_input(data.get('landmark', '').strip(), max_length=100) or None
        )
        
        db.session.add(customer)
        db.session.commit()
        return jsonify({"success": True, "message": "Customer added", "data": customer.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating customer: {str(e)}")
        return jsonify({"success": False, "message": "Failed to create customer"}), 500


@mgmt_bp.route('/customers/<int:id>', methods=['PUT'])
@require_admin
def update_customer(id):
    """Update customer"""
    try:
        data = request.get_json()
        customer = db.session.get(Customer, id)
        if not customer:
            return jsonify({"success": False, "message": "Customer not found"}), 404
        
        if 'mobile' in data and data['mobile'] != customer.mobile:
            new_mobile = re.sub(r'[\s\-\(\)\+]', '', data['mobile'].strip())
            existing = Customer.query.filter_by(mobile=new_mobile).first()
            if existing:
                return jsonify({"success": False, "message": "Another customer with this mobile exists"}), 400
            customer.mobile = new_mobile
        
        if 'name' in data: customer.name = sanitize_input(data['name'].strip(), max_length=100)
        if 'email' in data: customer.email = sanitize_input(data.get('email', '').strip(), max_length=100) or None
        if 'address' in data: customer.address = sanitize_input(data.get('address', '').strip(), max_length=500) or None
        if 'landmark' in data: customer.landmark = sanitize_input(data.get('landmark', '').strip(), max_length=100) or None
        if 'is_active' in data: customer.is_active = data['is_active']
        
        db.session.commit()
        return jsonify({"success": True, "message": "Customer updated", "data": customer.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating customer: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update customer"}), 500


@mgmt_bp.route('/customers/<int:id>', methods=['DELETE'])
@require_admin
def delete_customer(id):
    """Delete customer"""
    try:
        customer = db.session.get(Customer, id)
        if not customer:
            return jsonify({"success": False, "message": "Customer not found"}), 404
        
        customer.is_active = False
        db.session.commit()
        return jsonify({"success": True, "message": "Customer deleted"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting customer: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete customer"}), 500


# ========================================
# TECHNICIAN MANAGEMENT
# ========================================

@mgmt_bp.route('/technicians', methods=['GET'])
@require_admin
def get_technicians():
    """Get all technicians"""
    try:
        technicians = Technician.query.filter_by(is_active=True).order_by(Technician.name).all()
        return jsonify({"success": True, "data": [t.to_dict() for t in technicians]}), 200
    except Exception as e:
        logger.error(f"Error fetching technicians: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch technicians"}), 500


@mgmt_bp.route('/technicians/<int:id>', methods=['GET'])
@require_admin
def get_technician(id):
    """Get single technician"""
    try:
        tech = db.session.get(Technician, id)
        if not tech:
            return jsonify({"success": False, "message": "Technician not found"}), 404
        return jsonify({"success": True, "data": tech.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error fetching technician: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch technician"}), 500


@mgmt_bp.route('/technicians', methods=['POST'])
@require_admin
def create_technician():
    """Create new technician"""
    try:
        data = request.get_json()
        
        if not data.get('name') or not data.get('mobile'):
            return jsonify({"success": False, "message": "Name and mobile are required"}), 400
        
        mobile = re.sub(r'[\s\-\(\)\+]', '', data['mobile'].strip())
        if not re.match(r'^[6-9]\d{9}$', mobile):
            return jsonify({"success": False, "message": "Invalid mobile number"}), 400
        
        existing = Technician.query.filter_by(mobile=mobile).first()
        if existing:
            return jsonify({"success": False, "message": "Technician with this mobile already exists"}), 400
        
        tech = Technician(
            name=sanitize_input(data['name'].strip(), max_length=100),
            mobile=mobile,
            email=sanitize_input(data.get('email', '').strip(), max_length=100) or None,
            address=sanitize_input(data.get('address', '').strip(), max_length=500) or None,
            territory=sanitize_input(data.get('territory', '').strip(), max_length=100) or None,
            commission_rate=data.get('commission_rate', 0),
            availability_status=data.get('availability_status', 'Available')
        )
        
        db.session.add(tech)
        db.session.commit()
        return jsonify({"success": True, "message": "Technician added", "data": tech.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating technician: {str(e)}")
        return jsonify({"success": False, "message": "Failed to create technician"}), 500


@mgmt_bp.route('/technicians/<int:id>', methods=['PUT'])
@require_admin
def update_technician(id):
    """Update technician"""
    try:
        data = request.get_json()
        tech = db.session.get(Technician, id)
        if not tech:
            return jsonify({"success": False, "message": "Technician not found"}), 404
        
        if 'mobile' in data and data['mobile'] != tech.mobile:
            new_mobile = re.sub(r'[\s\-\(\)\+]', '', data['mobile'].strip())
            existing = Technician.query.filter_by(mobile=new_mobile).first()
            if existing:
                return jsonify({"success": False, "message": "Another technician with this mobile exists"}), 400
            tech.mobile = new_mobile
        
        if 'name' in data: tech.name = sanitize_input(data['name'].strip(), max_length=100)
        if 'email' in data: tech.email = sanitize_input(data.get('email', '').strip(), max_length=100) or None
        if 'address' in data: tech.address = sanitize_input(data.get('address', '').strip(), max_length=500) or None
        if 'territory' in data: tech.territory = sanitize_input(data.get('territory', '').strip(), max_length=100) or None
        if 'commission_rate' in data: tech.commission_rate = data['commission_rate']
        if 'availability_status' in data: tech.availability_status = data['availability_status']
        if 'is_active' in data: tech.is_active = data['is_active']
        
        db.session.commit()
        return jsonify({"success": True, "message": "Technician updated", "data": tech.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating technician: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update technician"}), 500


@mgmt_bp.route('/technicians/<int:id>', methods=['DELETE'])
@require_admin
def delete_technician(id):
    """Delete technician"""
    try:
        tech = db.session.get(Technician, id)
        if not tech:
            return jsonify({"success": False, "message": "Technician not found"}), 404
        
        tech.is_active = False
        db.session.commit()
        return jsonify({"success": True, "message": "Technician deleted"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting technician: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete technician"}), 500


# ========================================
# INVOICE MANAGEMENT
# ========================================

@mgmt_bp.route('/invoices', methods=['GET'])
@require_admin
def get_invoices():
    """Get all invoices"""
    try:
        invoices = Invoice.query.filter_by(is_deleted=False).order_by(Invoice.created_at.desc()).all()
        return jsonify({"success": True, "data": [inv.to_dict() for inv in invoices]}), 200
    except Exception as e:
        logger.error(f"Error fetching invoices: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch invoices"}), 500


@mgmt_bp.route('/invoices/<int:id>', methods=['GET'])
@require_admin
def get_invoice(id):
    """Get single invoice"""
    try:
        invoice = db.session.get(Invoice, id)
        if not invoice:
            return jsonify({"success": False, "message": "Invoice not found"}), 404
        
        items = InvoiceItem.query.filter_by(invoice_id=id).all()
        result = invoice.to_dict()
        result['items'] = [item.to_dict() for item in items]
        
        return jsonify({"success": True, "data": result}), 200
    except Exception as e:
        logger.error(f"Error fetching invoice: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch invoice"}), 500


@mgmt_bp.route('/invoices', methods=['POST'])
@require_admin
def create_invoice():
    """Create new invoice"""
    try:
        data = request.get_json()
        
        # Generate invoice number
        invoice_number = f"INV-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"
        
        invoice = Invoice(
            invoice_number=invoice_number,
            customer_id=data['customer_id'],
            ac_type=data.get('ac_type', 'Split'),
            star_rating=data.get('star_rating'),
            ton_capacity=data.get('ton_capacity'),
            inverter_type=data.get('inverter_type', 'Not Specified'),
            subtotal=data.get('subtotal', 0),
            gst_percentage=data.get('gst_percentage', 18),
            gst_amount=data.get('gst_amount', 0),
            total_amount=data.get('total_amount', 0),
            advance_payment=data.get('advance_payment', 0),
            balance_amount=data.get('balance_amount', 0),
            payment_mode=data.get('payment_mode', 'Pending'),
            payment_status='Paid' if data.get('advance_payment', 0) >= data.get('total_amount', 0) else ('Partial' if data.get('advance_payment', 0) > 0 else 'Pending'),
            notes=data.get('notes')
        )
        
        db.session.add(invoice)
        db.session.flush()
        
        # Add line items
        items = data.get('items', [])
        for item in items:
            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                item_type='service',
                quantity=item.get('quantity', 1),
                rate=item.get('rate', 0),
                amount=item.get('amount', 0)
            )
            db.session.add(invoice_item)
        
        db.session.commit()
        return jsonify({"success": True, "message": "Invoice created", "data": invoice.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating invoice: {str(e)}")
        return jsonify({"success": False, "message": "Failed to create invoice"}), 500


@mgmt_bp.route('/invoices/<int:id>', methods=['PUT'])
@require_admin
def update_invoice(id):
    """Update invoice"""
    try:
        data = request.get_json()
        invoice = db.session.get(Invoice, id)
        if not invoice:
            return jsonify({"success": False, "message": "Invoice not found"}), 404
        
        if 'payment_mode' in data: invoice.payment_mode = data['payment_mode']
        if 'advance_payment' in data:
            invoice.advance_payment = data['advance_payment']
            invoice.balance_amount = float(invoice.total_amount) - data['advance_payment']
            if data['advance_payment'] >= float(invoice.total_amount):
                invoice.payment_status = 'Paid'
            elif data['advance_payment'] > 0:
                invoice.payment_status = 'Partial'
        if 'payment_status' in data: invoice.payment_status = data['payment_status']
        if 'notes' in data: invoice.notes = data['notes']
        
        db.session.commit()
        return jsonify({"success": True, "message": "Invoice updated", "data": invoice.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating invoice: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update invoice"}), 500


@mgmt_bp.route('/invoices/<int:id>', methods=['DELETE'])
@require_admin
def delete_invoice(id):
    """Soft delete invoice"""
    try:
        invoice = db.session.get(Invoice, id)
        if not invoice:
            return jsonify({"success": False, "message": "Invoice not found"}), 404
        
        invoice.is_deleted = True
        db.session.commit()
        return jsonify({"success": True, "message": "Invoice deleted"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting invoice: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete invoice"}), 500


# ========================================
# AMC CONTRACT MANAGEMENT
# ========================================

@mgmt_bp.route('/amc', methods=['GET'])
@require_admin
def get_amc_contracts():
    """Get all AMC contracts"""
    try:
        contracts = AMCContract.query.filter_by(is_deleted=False).order_by(AMCContract.created_at.desc()).all()
        return jsonify({"success": True, "data": [c.to_dict() for c in contracts]}), 200
    except Exception as e:
        logger.error(f"Error fetching AMC contracts: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch AMC contracts"}), 500


@mgmt_bp.route('/amc/<int:id>', methods=['GET'])
@require_admin
def get_amc_contract(id):
    """Get single AMC contract"""
    try:
        contract = db.session.get(AMCContract, id)
        if not contract:
            return jsonify({"success": False, "message": "Contract not found"}), 404
        return jsonify({"success": True, "data": contract.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error fetching AMC contract: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch AMC contract"}), 500


@mgmt_bp.route('/amc', methods=['POST'])
@require_admin
def create_amc_contract():
    """Create new AMC contract"""
    try:
        data = request.get_json()
        
        contract_number = f"AMC-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{secrets.token_hex(3).upper()}"
        
        contract = AMCContract(
            contract_number=contract_number,
            customer_id=data['customer_id'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            total_amount=data['total_amount'],
            payment_frequency=data.get('payment_frequency', 'yearly'),
            status=data.get('status', 'active'),
            notes=data.get('notes')
        )
        
        db.session.add(contract)
        db.session.commit()
        return jsonify({"success": True, "message": "AMC contract created", "data": contract.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating AMC contract: {str(e)}")
        return jsonify({"success": False, "message": "Failed to create AMC contract"}), 500


@mgmt_bp.route('/amc/<int:id>', methods=['PUT'])
@require_admin
def update_amc_contract(id):
    """Update AMC contract"""
    try:
        data = request.get_json()
        contract = db.session.get(AMCContract, id)
        if not contract:
            return jsonify({"success": False, "message": "Contract not found"}), 404
        
        if 'start_date' in data: contract.start_date = data['start_date']
        if 'end_date' in data: contract.end_date = data['end_date']
        if 'total_amount' in data: contract.total_amount = data['total_amount']
        if 'payment_frequency' in data: contract.payment_frequency = data['payment_frequency']
        if 'status' in data: contract.status = data['status']
        if 'notes' in data: contract.notes = data['notes']
        
        db.session.commit()
        return jsonify({"success": True, "message": "AMC contract updated", "data": contract.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating AMC contract: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update AMC contract"}), 500


@mgmt_bp.route('/amc/<int:id>', methods=['DELETE'])
@require_admin
def delete_amc_contract(id):
    """Soft delete AMC contract"""
    try:
        contract = db.session.get(AMCContract, id)
        if not contract:
            return jsonify({"success": False, "message": "Contract not found"}), 404
        
        contract.is_deleted = True
        contract.status = 'cancelled'
        db.session.commit()
        return jsonify({"success": True, "message": "AMC contract deleted"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting AMC contract: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete AMC contract"}), 500
