
# ========================================
# CUSTOMER MANAGEMENT ROUTES
# ========================================

@api_bp.route('/admin/customers', methods=['GET'])
@require_admin
def get_customers():
    """Get all customers with optional search"""
    try:
        search = request.args.get('search', '')
        
        query = Customer.query
        
        if search:
            # Search by name or phone
            query = query.filter(
                db.or_(
                    Customer.name.ilike(f'%{search}%'),
                    Customer.phone.ilike(f'%{search}%')
                )
            )
        
        customers = query.order_by(Customer.created_at.desc()).all()
        
        return jsonify({
            "success": True,
            "data": [c.to_dict() for c in customers]
        }), 200
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch customers"}), 500


@api_bp.route('/admin/customers/<int:id>', methods=['GET'])
@require_admin
def get_customer(id):
    """Get single customer"""
    try:
        customer = Customer.query.get(id)
        if not customer:
            return jsonify({"success": False, "message": "Customer not found"}), 404
        
        return jsonify({"success": True, "data": customer.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error fetching customer: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch customer"}), 500


@api_bp.route('/admin/customers', methods=['POST'])
@require_admin
def create_customer():
    """Create new customer"""
    try:
        data = request.get_json()
        
        # Check if phone already exists
        existing = Customer.query.filter_by(phone=data['phone']).first()
        if existing:
            return jsonify({"success": False, "message": "Customer with this phone number already exists"}), 400
        
        customer = Customer(
            name=data['name'],
            phone=data['phone'],
            email=data.get('email'),
            customer_type=data.get('customer_type', 'Regular'),
            address=data.get('address'),
            city=data.get('city'),
            pincode=data.get('pincode'),
            notes=data.get('notes'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(customer)
        db.session.commit()
        
        logger.info(f"Customer created: ID={customer.id}, Name={customer.name}")
        return jsonify({"success": True, "message": "Customer added successfully", "data": customer.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating customer: {str(e)}")
        return jsonify({"success": False, "message": "Failed to create customer"}), 500


@api_bp.route('/admin/customers/<int:id>', methods=['PUT'])
@require_admin
def update_customer(id):
    """Update customer"""
    try:
        data = request.get_json()
        customer = Customer.query.get(id)
        
        if not customer:
            return jsonify({"success": False, "message": "Customer not found"}), 404
        
        # Check phone uniqueness if changing phone
        if 'phone' in data and data['phone'] != customer.phone:
            existing = Customer.query.filter_by(phone=data['phone']).first()
            if existing:
                return jsonify({"success": False, "message": "Another customer with this phone number already exists"}), 400
        
        customer.name = data.get('name', customer.name)
        customer.phone = data.get('phone', customer.phone)
        customer.email = data.get('email', customer.email)
        customer.customer_type = data.get('customer_type', customer.customer_type)
        customer.address = data.get('address', customer.address)
        customer.city = data.get('city', customer.city)
        customer.pincode = data.get('pincode', customer.pincode)
        customer.notes = data.get('notes', customer.notes)
        customer.is_active = data.get('is_active', customer.is_active)
        
        db.session.commit()
        
        logger.info(f"Customer updated: ID={customer.id}")
        return jsonify({"success": True, "message": "Customer updated successfully", "data": customer.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating customer: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update customer"}), 500


@api_bp.route('/admin/customers/<int:id>', methods=['DELETE'])
@require_admin
def delete_customer(id):
    """Delete customer"""
    try:
        customer = Customer.query.get(id)
        
        if not customer:
            return jsonify({"success": False, "message": "Customer not found"}), 404
        
        db.session.delete(customer)
        db.session.commit()
        
        logger.info(f"Customer deleted: ID={id}")
        return jsonify({"success": True, "message": "Customer deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting customer: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete customer"}), 500
