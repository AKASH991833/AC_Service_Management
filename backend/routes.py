"""
API Routes - Security Hardened
REST endpoints for service requests and contact forms
With API Key Authentication and Enhanced Validation
Includes Admin Dashboard endpoints
"""

from flask import Blueprint, request, jsonify, session, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
import logging
import os
from functools import wraps
from models import db, ServiceRequest, ContactMessage, Admin, WebsiteSetting, GalleryImage, Testimonial, Service, Product
from whatsapp import send_whatsapp_service_confirmation, send_whatsapp_contact_confirmation
from datetime import datetime
from security import (
    log_security_event,
    validate_session,
    sanitize_input,
    validate_password_strength,
    hash_password_secure,
    verify_password_secure
)

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)

# Create a separate limiter for API routes
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")


def require_api_key(f):
    """Decorator to require API key authentication"""
    from functools import wraps
    import os
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from header
        api_key = request.headers.get('X-API-KEY')
        
        # Get expected key from environment variable
        expected_key = os.getenv('API_KEY')
        
        if not expected_key:
            logger.error("API_KEY not configured in environment")
            return jsonify({
                "success": False,
                "error": "Server configuration error"
            }), 500
        
        # Validate API key
        if not api_key:
            logger.warning(f"Unauthorized access attempt from {request.remote_addr} - Missing API key")
            return jsonify({
                "success": False,
                "error": "Unauthorized access - Missing API key"
            }), 401
        
        if api_key != expected_key:
            logger.warning(f"Unauthorized access attempt from {request.remote_addr} - Invalid API key")
            return jsonify({
                "success": False,
                "error": "Unauthorized access - Invalid API key"
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def validate_phone(phone):
    """Validate Indian phone number format"""
    if not phone:
        return False
    # Remove spaces and check if it's a valid 10-digit Indian number
    cleaned = re.sub(r'\s', '', phone)
    return bool(re.match(r'^[6-9]\d{9}$', cleaned))


def validate_ac_type(ac_type):
    """Validate AC type"""
    if not ac_type:
        return True  # Optional field
    
    valid_ac_types = ['Split', 'Window', 'Central', 'Tower', 'Not Specified']
    return ac_type.title() in valid_ac_types or ac_type in valid_ac_types


def validate_service_request(data):
    """Validate service request data - Enhanced"""
    errors = []

    # Validate name
    if not data.get('name') or len(data.get('name', '').strip()) < 2:
        errors.append('Name must be at least 2 characters')
    elif len(data.get('name', '').strip()) > 100:
        errors.append('Name must be less than 100 characters')

    # Validate phone
    if not data.get('phone'):
        errors.append('Phone number is required')
    elif not validate_phone(data.get('phone', '')):
        errors.append('Please enter a valid 10-digit mobile number')

    # Validate address
    if not data.get('address') or len(data.get('address', '').strip()) < 5:
        errors.append('Address is required (minimum 5 characters)')
    elif len(data.get('address', '').strip()) > 500:
        errors.append('Address must be less than 500 characters')

    # Validate service type
    valid_services = ['installation', 'repair', 'gas', 'amc', 'pcb', 'buy', 'rent', 'cleaning', 'servicing']
    if not data.get('serviceType'):
        errors.append('Service type is required')
    elif data.get('serviceType') not in valid_services:
        errors.append('Please select a valid service type')

    # Validate AC type (optional but must be valid if provided)
    if data.get('acType') and not validate_ac_type(data.get('acType', '')):
        errors.append('Invalid AC type. Valid options: Split, Window, Central, Tower')

    # Validate email (optional but must be valid if provided)
    if data.get('email'):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data.get('email', '')):
            errors.append('Please enter a valid email address')

    return errors


def validate_contact_message(data):
    """Validate contact message data - Enhanced"""
    errors = []

    # Validate name
    if not data.get('name') or len(data.get('name', '').strip()) < 2:
        errors.append('Name must be at least 2 characters')
    elif len(data.get('name', '').strip()) > 100:
        errors.append('Name must be less than 100 characters')

    # Validate phone
    if not data.get('phone'):
        errors.append('Phone number is required')
    elif not validate_phone(data.get('phone', '')):
        errors.append('Please enter a valid 10-digit mobile number')

    # Validate service type
    valid_services = ['installation', 'repair', 'gas', 'amc', 'pcb', 'buy', 'rent', 'cleaning', 'servicing']
    if not data.get('serviceType'):
        errors.append('Service type is required')
    elif data.get('serviceType') not in valid_services:
        errors.append('Please select a valid service type')

    # Validate email (optional but must be valid if provided)
    if data.get('email'):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data.get('email', '')):
            errors.append('Please enter a valid email address')

    return errors


@api_bp.route('/service-request', methods=['POST'])
@limiter.limit("10 per minute")
@require_api_key
def submit_service_request():
    """
    Submit a new service request
    Requires X-API-KEY header
    
    Expected JSON body:
    {
        "name": "John Doe",
        "phone": "9876543210",
        "address": "123 Main Street, Mumbai",
        "serviceType": "installation",
        "acType": "Split",
        "preferredDate": "2026-02-28",
        "timeSlot": "morning",
        "message": "Optional message"
    }
    """
    try:
        # Get JSON data
        data = request.get_json()

        if not data:
            logger.warning(f"Bad request from {request.remote_addr}: No JSON data")
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400

        # Validate input
        validation_errors = validate_service_request(data)
        if validation_errors:
            logger.warning(f"Validation failed from {request.remote_addr}: {validation_errors[0]}")
            return jsonify({
                "success": False,
                "message": validation_errors[0]
            }), 400

        # Create service request record (matching billing software schema)
        service_request = ServiceRequest(
            customer_name=data['name'].strip(),
            customer_phone=re.sub(r'\s', '', data['phone']),
            customer_email=data.get('email', '').strip() if data.get('email') else None,
            customer_address=data['address'].strip(),
            service_type=data['serviceType'],
            ac_type=data.get('acType', 'Not Specified'),
            preferred_date=data.get('preferredDate', None) if data.get('preferredDate') else None,
            time_slot=data.get('timeSlot', 'Not Specified'),
            message=data.get('message', '').strip() if data.get('message') else None,
            source='Website',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:500]
        )

        db.session.add(service_request)
        db.session.commit()

        logger.info(f"Service request created: ID={service_request.id}, Name={service_request.customer_name}")

        # Send WhatsApp confirmation message (non-blocking)
        try:
            whatsapp_result = send_whatsapp_service_confirmation(
                customer_name=service_request.customer_name,
                phone=service_request.customer_phone,
                service_type=service_request.service_type,
                ac_type=service_request.ac_type,
                request_id=service_request.id
            )
            if whatsapp_result.get('success'):
                logger.info(f"WhatsApp sent to {service_request.customer_phone}")
            else:
                logger.warning(f"WhatsApp failed: {whatsapp_result.get('message')}")
        except Exception as e:
            logger.warning(f"WhatsApp error (non-fatal): {str(e)}")
            # Don't fail the request if WhatsApp fails

        return jsonify({
            "success": True,
            "message": "Service request submitted successfully! Our team will contact you soon.",
            "data": {
                "requestId": service_request.id
            }
        }), 201

    except ValueError as ve:
        db.session.rollback()
        logger.error(f"Value error: {str(ve)}")
        return jsonify({
            "success": False,
            "message": "Invalid data provided"
        }), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error submitting service request: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Failed to submit request. Please try again."
        }), 500


@api_bp.route('/contact', methods=['POST'])
@limiter.limit("10 per minute")
@require_api_key
def submit_contact_message():
    """
    Submit a contact form message
    Requires X-API-KEY header
    
    Expected JSON body:
    {
        "name": "John Doe",
        "phone": "9876543210",
        "email": "john@example.com",
        "address": "Optional address",
        "serviceType": "installation",
        "acType": "Split",
        "message": "Optional message"
    }
    """
    try:
        # Get JSON data
        data = request.get_json()

        if not data:
            logger.warning(f"Bad request from {request.remote_addr}: No JSON data")
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400

        # Validate input
        validation_errors = validate_contact_message(data)
        if validation_errors:
            logger.warning(f"Validation failed from {request.remote_addr}: {validation_errors[0]}")
            return jsonify({
                "success": False,
                "message": validation_errors[0]
            }), 400

        # Create contact message record (matching billing software schema)
        contact_message = ContactMessage(
            name=data['name'].strip(),
            phone=re.sub(r'\s', '', data['phone']),
            email=data.get('email', '').strip() if data.get('email') else None,
            address=data.get('address', '').strip() if data.get('address') else None,
            service_type=data['serviceType'],
            ac_type=data.get('acType', 'Not Specified'),
            message=data.get('message', '').strip() if data.get('message') else None,
            source='Website',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:500]
        )

        db.session.add(contact_message)
        db.session.commit()

        logger.info(f"Contact message created: ID={contact_message.id}, Name={contact_message.name}")

        # Send WhatsApp confirmation message (non-blocking)
        try:
            whatsapp_result = send_whatsapp_contact_confirmation(
                customer_name=contact_message.name,
                phone=contact_message.phone,
                service_type=contact_message.service_type,
                message_id=contact_message.id
            )
            if whatsapp_result.get('success'):
                logger.info(f"WhatsApp sent to {contact_message.phone}")
            else:
                logger.warning(f"WhatsApp failed: {whatsapp_result.get('message')}")
        except Exception as e:
            logger.warning(f"WhatsApp error (non-fatal): {str(e)}")
            # Don't fail the request if WhatsApp fails

        return jsonify({
            "success": True,
            "message": "Message sent successfully! We will contact you soon.",
            "data": {
                "messageId": contact_message.id
            }
        }), 201

    except ValueError as ve:
        db.session.rollback()
        logger.error(f"Value error: {str(ve)}")
        return jsonify({
            "success": False,
            "message": "Invalid data provided"
        }), 400
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error submitting contact message: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Failed to send message. Please try again."
        }), 500


@api_bp.route('/service-request', methods=['GET'])
@limiter.limit("30 per hour")
def get_service_requests():
    """
    Get all service requests (for admin use)
    Optional query params: status, limit, offset
    """
    try:
        status = request.args.get('status')
        limit = min(int(request.args.get('limit', 50)), 100)
        offset = int(request.args.get('offset', 0))

        query = ServiceRequest.query

        if status:
            query = query.filter_by(request_status=status)

        requests = query.order_by(
            ServiceRequest.created_at.desc()
        ).offset(offset).limit(limit).all()

        return jsonify({
            "success": True,
            "data": [req.to_dict() for req in requests],
            "count": len(requests)
        }), 200

    except Exception as e:
        print(f"Error fetching service requests: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch service requests"
        }), 500


@api_bp.route('/contact', methods=['GET'])
@limiter.limit("30 per hour")
def get_contact_messages():
    """
    Get all contact messages (for admin use)
    Optional query params: status, limit, offset
    """
    try:
        status = request.args.get('status')
        limit = min(int(request.args.get('limit', 50)), 100)
        offset = int(request.args.get('offset', 0))

        query = ContactMessage.query

        if status:
            query = query.filter_by(status=status)

        messages = query.order_by(
            ContactMessage.created_at.desc()
        ).offset(offset).limit(limit).all()

        return jsonify({
            "success": True,
            "data": [msg.to_dict() for msg in messages],
            "count": len(messages)
        }), 200

    except Exception as e:
        print(f"Error fetching contact messages: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch contact messages"
        }), 500


# ========================================
# ADMIN DASHBOARD ROUTES
# ========================================

def require_admin(f):
    """Enhanced admin authentication with security checks"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if admin is logged in
        admin_id = session.get('admin_id')
        if not admin_id:
            log_security_event('UNAUTHORIZED_ACCESS', {'endpoint': request.endpoint})
            response = make_response(jsonify({
                "success": False,
                "message": "Unauthorized - Please login"
            }), 401)
            response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response

        # Validate session
        if not validate_session():
            logger.warning(f"Session validation failed for admin_id: {admin_id}")
            session.pop('admin_id', None)
            response = make_response(jsonify({
                "success": False,
                "message": "Session expired - Please login again"
            }), 401)
            response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response

        # Check if admin is active
        admin = Admin.query.get(admin_id)
        if not admin or not admin.is_active:
            session.pop('admin_id', None)
            log_security_event('INACTIVE_ADMIN_LOGIN', {'admin_id': admin_id})
            response = make_response(jsonify({
                "success": False,
                "message": "Account deactivated"
            }), 401)
            response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            return response

        # Execute the function and add security headers
        response = make_response(f(*args, **kwargs))
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-API-KEY')
        return response
    return decorated_function


@api_bp.route('/admin/login', methods=['POST'])
@limiter.limit("10 per minute")
def admin_login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            logger.error("No JSON data provided in login request")
            return jsonify({
                "success": False,
                "message": "No data provided"
            }), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')

        logger.info(f"Login attempt for username: {username}")

        if not username or not password:
            logger.error("Username or password missing")
            return jsonify({
                "success": False,
                "message": "Username and password required"
            }), 400

        admin = Admin.query.filter_by(username=username).first()
        
        if not admin:
            logger.warning(f"Login attempt with unknown username: {username}")
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            }), 401

        logger.info(f"Admin found, checking password for: {username}")
        
        if not admin.check_password(password):
            logger.warning(f"Failed login attempt for username: {username} - Password mismatch")
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            }), 401

        if not admin.is_active:
            logger.warning(f"Inactive admin trying to login: {username}")
            return jsonify({
                "success": False,
                "message": "Account is deactivated"
            }), 401

        # Update last login
        admin.last_login = datetime.utcnow()
        db.session.commit()
        logger.info(f"Updated last login for: {username}")

        # Set session
        session['admin_id'] = admin.id
        logger.info(f"Session set for admin_id: {admin.id}")

        logger.info(f"✅ Admin logged in successfully: {username}")

        response = make_response(jsonify({
            "success": True,
            "message": "Login successful",
            "data": {
                "admin": admin.to_dict()
            }
        }), 200)

        # Add CORS headers for credentials - allow both localhost and 127.0.0.1
        origin = request.headers.get('Origin', '*')
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-API-KEY')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        response.headers.add('Access-Control-Expose-Headers', 'Set-Cookie')

        return response

    except Exception as e:
        logger.error(f"❌ Admin login error: {str(e)}", exc_info=True)
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            "success": False,
            "message": f"Login failed: {str(e)}"
        }), 500


@api_bp.route('/admin/logout', methods=['POST'])
@require_admin
def admin_logout():
    """Admin logout endpoint"""
    session.pop('admin_id', None)
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    }), 200


@api_bp.route('/admin/me', methods=['GET'])
@require_admin
def get_current_admin():
    """Get current admin info"""
    admin = Admin.query.get(session['admin_id'])
    return jsonify({
        "success": True,
        "data": admin.to_dict()
    }), 200


@api_bp.route('/admin/stats', methods=['GET'])
@require_admin
def get_admin_stats():
    """Get dashboard statistics"""
    try:
        total_messages = ContactMessage.query.count()
        total_requests = ServiceRequest.query.count()
        pending_requests = ServiceRequest.query.filter_by(request_status='Pending').count()
        completed_requests = ServiceRequest.query.filter_by(request_status='Completed').count()
        unread_messages = ContactMessage.query.filter_by(status='unread').count()

        return jsonify({
            "success": True,
            "data": {
                "totalMessages": total_messages,
                "totalRequests": total_requests,
                "pendingRequests": pending_requests,
                "completedRequests": completed_requests,
                "unreadMessages": unread_messages
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to get statistics"
        }), 500


@api_bp.route('/admin/messages', methods=['GET'])
@require_admin
def get_all_messages():
    """Get all contact messages with filtering"""
    try:
        status = request.args.get('status', 'all')
        limit = min(int(request.args.get('limit', 100)), 200)
        offset = int(request.args.get('offset', 0))

        query = ContactMessage.query

        if status != 'all':
            query = query.filter_by(status=status)

        messages = query.order_by(
            ContactMessage.created_at.desc()
        ).offset(offset).limit(limit).all()

        return jsonify({
            "success": True,
            "data": [msg.to_dict() for msg in messages],
            "count": len(messages)
        }), 200

    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch messages"
        }), 500


@api_bp.route('/admin/messages/<int:id>', methods=['GET'])
@require_admin
def get_message(id):
    """Get single message details"""
    try:
        message = ContactMessage.query.get(id)
        if not message:
            return jsonify({
                "success": False,
                "message": "Message not found"
            }), 404

        return jsonify({
            "success": True,
            "data": message.to_dict()
        }), 200

    except Exception as e:
        logger.error(f"Error fetching message: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch message"
        }), 500


@api_bp.route('/admin/messages/<int:id>/status', methods=['PUT'])
@require_admin
def update_message_status(id):
    """Update message status"""
    try:
        data = request.get_json()
        message = ContactMessage.query.get(id)
        
        if not message:
            return jsonify({
                "success": False,
                "message": "Message not found"
            }), 404

        if 'status' in data:
            message.status = data['status']

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Status updated",
            "data": message.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating message status: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to update status"
        }), 500


@api_bp.route('/admin/requests', methods=['GET'])
@require_admin
def get_all_requests():
    """Get all service requests with filtering"""
    try:
        status = request.args.get('status', 'all')
        limit = min(int(request.args.get('limit', 100)), 200)
        offset = int(request.args.get('offset', 0))

        query = ServiceRequest.query

        if status != 'all':
            query = query.filter_by(request_status=status)

        requests = query.order_by(
            ServiceRequest.created_at.desc()
        ).offset(offset).limit(limit).all()

        return jsonify({
            "success": True,
            "data": [req.to_dict() for req in requests],
            "count": len(requests)
        }), 200

    except Exception as e:
        logger.error(f"Error fetching requests: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch requests"
        }), 500


@api_bp.route('/admin/requests/<int:id>', methods=['GET'])
@require_admin
def get_request(id):
    """Get single service request details"""
    try:
        service_request = ServiceRequest.query.get(id)
        if not service_request:
            return jsonify({
                "success": False,
                "message": "Request not found"
            }), 404

        return jsonify({
            "success": True,
            "data": service_request.to_dict()
        }), 200

    except Exception as e:
        logger.error(f"Error fetching request: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch request"
        }), 500


@api_bp.route('/admin/requests/<int:id>/status', methods=['PUT'])
@require_admin
def update_request_status(id):
    """Update service request status"""
    try:
        data = request.get_json()
        service_request = ServiceRequest.query.get(id)
        
        if not service_request:
            return jsonify({
                "success": False,
                "message": "Request not found"
            }), 404

        if 'status' in data:
            service_request.request_status = data['status']
        
        if 'notes' in data:
            # You can add a notes field to the model later
            pass

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Status updated",
            "data": service_request.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating request status: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to update status"
        }), 500


@api_bp.route('/admin/settings', methods=['GET'])
@require_admin
def get_settings():
    """Get all website settings"""
    try:
        settings = WebsiteSetting.query.all()
        settings_dict = {s.setting_key: s.setting_value for s in settings}

        return jsonify({
            "success": True,
            "data": settings_dict
        }), 200

    except Exception as e:
        logger.error(f"Error fetching settings: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch settings"
        }), 500


@api_bp.route('/admin/settings', methods=['POST'])
@require_admin
def update_settings():
    """Update website settings"""
    try:
        data = request.get_json()

        for key, value in data.items():
            setting = WebsiteSetting.query.filter_by(setting_key=key).first()
            if setting:
                setting.setting_value = value
            else:
                setting = WebsiteSetting(
                    setting_key=key,
                    setting_value=value,
                    setting_type='text'
                )
                db.session.add(setting)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Settings updated successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating settings: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to update settings"
        }), 500


@api_bp.route('/admin/content', methods=['GET'])
@require_admin
def get_content():
    """Get website content settings"""
    try:
        settings = WebsiteSetting.query.all()
        settings_dict = {s.setting_key: s.setting_value for s in settings}

        return jsonify({
            "success": True,
            "data": settings_dict
        }), 200

    except Exception as e:
        logger.error(f"Error fetching content: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch content"
        }), 500


@api_bp.route('/admin/content', methods=['POST'])
@require_admin
def update_content():
    """Update website content"""
    try:
        data = request.get_json()

        content_fields = ['heroTitle', 'heroSubtitle', 'contactPhone', 'contactEmail', 'businessHours', 'address']

        for key in content_fields:
            if key in data:
                setting = WebsiteSetting.query.filter_by(setting_key=key).first()
                if setting:
                    setting.setting_value = data[key]
                else:
                    setting = WebsiteSetting(
                        setting_key=key,
                        setting_value=data[key],
                        setting_type='text'
                    )
                    db.session.add(setting)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Content updated successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating content: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to update content"
        }), 500


# ========================================
# PHOTO GALLERY ROUTES
# ========================================

@api_bp.route('/admin/gallery', methods=['GET'])
@require_admin
def get_gallery_images():
    """Get all gallery images with optional category filter"""
    try:
        category = request.args.get('category', 'all')
        limit = min(int(request.args.get('limit', 100)), 200)
        offset = int(request.args.get('offset', 0))

        query = GalleryImage.query.filter_by(is_active=True)

        if category != 'all':
            query = query.filter_by(category=category)

        images = query.order_by(
            GalleryImage.created_at.desc()
        ).offset(offset).limit(limit).all()

        return jsonify({
            "success": True,
            "data": [img.to_dict() for img in images],
            "count": len(images)
        }), 200

    except Exception as e:
        logger.error(f"Error fetching gallery images: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to fetch gallery images"
        }), 500


@api_bp.route('/admin/gallery', methods=['POST'])
@require_admin
def upload_gallery_image():
    """Upload image to gallery"""
    try:
        if 'image' not in request.files:
            return jsonify({
                "success": False,
                "message": "No image file provided"
            }), 400

        file = request.files['image']
        category = request.form.get('category', 'gallery')
        alt_text = request.form.get('alt_text', '')

        if file.filename == '':
            return jsonify({
                "success": False,
                "message": "No file selected"
            }), 400

        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        filename = file.filename.lower()
        ext = filename.rsplit('.', 1)[1] if '.' in filename else ''

        if ext not in allowed_extensions:
            return jsonify({
                "success": False,
                "message": f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
            }), 400

        # Create uploads directory if it doesn't exist
        import os
        from werkzeug.utils import secure_filename
        from datetime import datetime

        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'gallery')
        os.makedirs(uploads_dir, exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{secure_filename(file.filename)}"
        file_path = os.path.join(uploads_dir, unique_filename)

        # Get file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning

        # Save file
        file.save(file_path)

        # Create URL path (relative to frontend)
        image_url = f"/uploads/gallery/{unique_filename}"

        # Create database record
        gallery_image = GalleryImage(
            image_path=file_path,
            image_url=image_url,
            category=category,
            alt_text=alt_text,
            file_size=file_size,
            mime_type=file.content_type
        )

        db.session.add(gallery_image)
        db.session.commit()

        logger.info(f"Gallery image uploaded: ID={gallery_image.id}, Category={category}")

        return jsonify({
            "success": True,
            "message": "Image uploaded successfully",
            "data": gallery_image.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error uploading image: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": "Failed to upload image"
        }), 500


@api_bp.route('/admin/gallery/<int:id>', methods=['DELETE'])
@require_admin
def delete_gallery_image(id):
    """Delete image from gallery"""
    try:
        import os

        image = GalleryImage.query.get(id)
        if not image:
            return jsonify({
                "success": False,
                "message": "Image not found"
            }), 404

        # Delete file from filesystem
        if os.path.exists(image.image_path):
            os.remove(image.image_path)

        # Mark as inactive (soft delete)
        image.is_active = False
        db.session.commit()

        logger.info(f"Gallery image deleted: ID={id}")

        return jsonify({
            "success": True,
            "message": "Image deleted successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting image: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to delete image"
        }), 500
