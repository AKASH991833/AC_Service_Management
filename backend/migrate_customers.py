# Additional Migration Functions

def migrate_existing_customers():
    """Migrate existing customers from service requests and contact messages"""
    try:
        # Get all unique customers from service requests
        service_requests = ServiceRequest.query.all()
        contact_messages = ContactMessage.query.all()
        
        migrated_count = 0
        
        for request in service_requests:
            # Check if customer already exists
            existing = Customer.query.filter_by(phone=request.customer_phone).first()
            
            if not existing:
                customer = Customer(
                    name=request.customer_name,
                    phone=request.customer_phone,
                    email=request.customer_email,
                    address=request.customer_address,
                    total_services=1,
                    last_service_date=request.created_at
                )
                db.session.add(customer)
                migrated_count += 1
            else:
                # Update existing customer
                existing.total_services += 1
                existing.last_service_date = request.created_at
        
        for message in contact_messages:
            # Check if customer already exists
            existing = Customer.query.filter_by(phone=message.phone).first()
            
            if not existing:
                customer = Customer(
                    name=message.name,
                    phone=message.phone,
                    email=message.email,
                    address=message.address,
                    total_services=0
                )
                db.session.add(customer)
                migrated_count += 1
        
        db.session.commit()
        print(f"✅ Migrated {migrated_count} existing customers!")
        
    except Exception as e:
        db.session.rollback()
        print(f"⚠️ Migration error: {str(e)}")
