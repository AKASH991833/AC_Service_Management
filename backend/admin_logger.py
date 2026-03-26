"""
Admin Activity Logger
Utility functions for logging admin actions
"""

from models import AdminActivityLog, db
from flask import request, session
import json
from datetime import datetime


def log_admin_action(action_type, action_category, description, target_type=None, target_id=None, changes=None, status='success', error_message=None):
    """
    Log an admin action to the database
    
    Args:
        action_type: Type of action (CREATE, UPDATE, DELETE, LOGIN, LOGOUT, VIEW)
        action_category: Category (content, product, service, testimonial, gallery, settings)
        description: Human-readable description
        target_type: Type of target object (e.g., 'Product', 'Service')
        target_id: ID of target object
        changes: JSON string or dict of changes made
        status: success, failed, error
        error_message: Error message if failed
    
    Returns:
        AdminActivityLog: Created log entry
    """
    try:
        # Get admin info from session
        admin_id = session.get('admin_id')
        admin_username = session.get('admin_username', 'unknown')
        
        # If admin_username not in session, try to get from admin_id
        if admin_username == 'unknown' and admin_id:
            from models import Admin
            admin = Admin.query.get(admin_id)
            if admin:
                admin_username = admin.username
        
        # Convert changes to JSON if dict
        changes_json = None
        if changes:
            if isinstance(changes, dict):
                changes_json = json.dumps(changes)
            elif isinstance(changes, str):
                changes_json = changes
        
        # Create log entry
        log_entry = AdminActivityLog(
            admin_id=admin_id,
            admin_username=admin_username,
            action_type=action_type,
            action_category=action_category,
            description=description,
            target_type=target_type,
            target_id=target_id,
            changes=changes_json,
            ip_address=request.remote_addr if request else None,
            user_agent=request.headers.get('User-Agent', '')[:500] if request else None,
            status=status,
            error_message=error_message
        )
        
        db.session.add(log_entry)
        db.session.commit()
        
        return log_entry
        
    except Exception as e:
        # Don't fail the operation if logging fails
        # But log to app logger
        import logging
        logger = logging.getLogger('ansh_aircool.admin')
        if logger:
            logger.error(f"Failed to log admin action: {str(e)}")
        
        try:
            db.session.rollback()
        except:
            pass
        
        return None


def log_content_update(section_name, changes, admin_id=None):
    """Log website content update"""
    return log_admin_action(
        action_type='UPDATE',
        action_category='content',
        description=f'Updated {section_name} section content',
        target_type='WebsiteContent',
        changes=changes
    )


def log_product_action(action, product_name, product_id, changes=None):
    """Log product CRUD action"""
    return log_admin_action(
        action_type=action,
        action_category='product',
        description=f'{action.title()} product: {product_name}',
        target_type='Product',
        target_id=product_id,
        changes=changes
    )


def log_service_action(action, service_name, service_id, changes=None):
    """Log service CRUD action"""
    return log_admin_action(
        action_type=action,
        action_category='service',
        description=f'{action.title()} service: {service_name}',
        target_type='Service',
        target_id=service_id,
        changes=changes
    )


def log_testimonial_action(action, customer_name, testimonial_id):
    """Log testimonial CRUD action"""
    return log_admin_action(
        action_type=action,
        action_category='testimonial',
        description=f'{action.title()} testimonial from {customer_name}',
        target_type='Testimonial',
        target_id=testimonial_id
    )


def log_gallery_upload(image_filename, image_id):
    """Log gallery image upload"""
    return log_admin_action(
        action_type='CREATE',
        action_category='gallery',
        description=f'Uploaded image: {image_filename}',
        target_type='GalleryImage',
        target_id=image_id
    )


def log_settings_update(settings_changed):
    """Log settings update"""
    return log_admin_action(
        action_type='UPDATE',
        action_category='settings',
        description='Updated website settings',
        target_type='WebsiteSetting',
        changes=settings_changed
    )


def get_admin_logs(admin_id=None, limit=50, offset=0, action_type=None, category=None):
    """
    Get admin activity logs with filtering
    
    Args:
        admin_id: Filter by admin ID
        limit: Max results
        offset: Results offset
        action_type: Filter by action type
        category: Filter by category
    
    Returns:
        list: List of log entries
    """
    query = AdminActivityLog.query
    
    if admin_id:
        query = query.filter_by(admin_id=admin_id)
    
    if action_type:
        query = query.filter_by(action_type=action_type)
    
    if category:
        query = query.filter_by(action_category=category)
    
    logs = query.order_by(
        AdminActivityLog.created_at.desc()
    ).offset(offset).limit(limit).all()
    
    return [log.to_dict() for log in logs]


def get_recent_logs(limit=20):
    """Get most recent admin logs"""
    return get_admin_logs(limit=limit)
