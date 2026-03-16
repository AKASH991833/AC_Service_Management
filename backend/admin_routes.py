"""
Comprehensive Admin Routes for Full Website Control
Allows admin to edit every section of the website
"""

from flask import Blueprint, request, jsonify, session, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import json
from functools import wraps
from datetime import datetime
from models import (
    db, Admin, WebsiteSetting, WebsiteContent, 
    Service, Product, Testimonial, GalleryImage,
    ContactMessage, ServiceRequest
)
from werkzeug.utils import secure_filename
from security import log_security_event, validate_session

logger = None
try:
    import logging
    logger = logging.getLogger(__name__)
except:
    pass

admin_bp = Blueprint('admin_full', __name__)

# Limiter for rate limiting
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")


def require_admin(f):
    """Admin authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin_id = session.get('admin_id')
        if not admin_id:
            return jsonify({
                "success": False,
                "message": "Unauthorized - Please login"
            }), 401

        if not validate_session():
            session.pop('admin_id', None)
            return jsonify({
                "success": False,
                "message": "Session expired - Please login again"
            }), 401

        admin = Admin.query.get(admin_id)
        if not admin or not admin.is_active:
            session.pop('admin_id', None)
            return jsonify({
                "success": False,
                "message": "Account is deactivated"
            }), 401

        response = make_response(f(*args, **kwargs))
        response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin', '*'))
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    return decorated_function


# ========================================
# HERO SECTION MANAGEMENT
# ========================================

@admin_bp.route('/section/hero', methods=['GET'])
@require_admin
def get_hero_section():
    """Get Hero section content"""
    try:
        content = WebsiteContent.query.filter_by(section_name='hero').all()
        data = {c.content_key: c.content_value for c in content}
        
        # Default values if not set
        defaults = {
            'title': 'Professional AC Service & Installation at Your Doorstep',
            'subtitle': 'Certified Technicians | Same Day Service | Trusted by 1000+ Customers',
            'cta_text': 'Book Now',
            'cta_phone': '+91 9819104977',
            'background_image': '',
            'show_video': 'false',
            'video_url': ''
        }
        
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        if logger: logger.error(f"Error getting hero section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/hero', methods=['PUT'])
@require_admin
def update_hero_section():
    """Update Hero section content"""
    try:
        data = request.get_json()
        
        fields = ['title', 'subtitle', 'cta_text', 'cta_phone', 
                  'background_image', 'show_video', 'video_url']
        
        for field in fields:
            if field in data:
                content = WebsiteContent.query.filter_by(
                    section_name='hero', content_key=field
                ).first()
                
                if content:
                    content.content_value = data[field]
                else:
                    content = WebsiteContent(
                        section_name='hero',
                        content_key=field,
                        content_value=data[field],
                        content_type='text'
                    )
                    db.session.add(content)
        
        db.session.commit()
        return jsonify({"success": True, "message": "Hero section updated"}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating hero section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# SERVICES SECTION MANAGEMENT
# ========================================

@admin_bp.route('/section/services', methods=['GET'])
@require_admin
def get_services_section():
    """Get all services"""
    try:
        services = Service.query.order_by(Service.display_order).all()
        return jsonify({"success": True, "data": [s.to_dict() for s in services]}), 200
    except Exception as e:
        if logger: logger.error(f"Error getting services: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/services', methods=['POST'])
@require_admin
def create_service():
    """Create new service"""
    try:
        data = request.get_json()
        
        features_json = json.dumps(data.get('features', [])) if isinstance(data.get('features'), list) else data.get('features', '[]')
        
        service = Service(
            service_name=data.get('service_name', ''),
            service_slug=data.get('service_slug', '').lower().replace(' ', '-'),
            starting_price=data.get('starting_price', '₹0'),
            price_numeric=data.get('price_numeric', 0),
            description=data.get('description', ''),
            duration=data.get('duration', ''),
            icon_class=data.get('icon_class', 'fas fa-tools'),
            features=features_json,
            is_active=data.get('is_active', True),
            is_featured=data.get('is_featured', False),
            display_order=data.get('display_order', 0),
            service_image=data.get('service_image', '')
        )
        
        db.session.add(service)
        db.session.commit()
        
        return jsonify({"success": True, "data": service.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error creating service: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/services/<int:id>', methods=['PUT'])
@require_admin
def update_service(id):
    """Update service"""
    try:
        service = Service.query.get(id)
        if not service:
            return jsonify({"success": False, "message": "Service not found"}), 404
        
        data = request.get_json()
        
        if 'service_name' in data:
            service.service_name = data['service_name']
        if 'service_slug' in data:
            service.service_slug = data['service_slug'].lower().replace(' ', '-')
        if 'starting_price' in data:
            service.starting_price = data['starting_price']
        if 'price_numeric' in data:
            service.price_numeric = data['price_numeric']
        if 'description' in data:
            service.description = data['description']
        if 'duration' in data:
            service.duration = data['duration']
        if 'icon_class' in data:
            service.icon_class = data['icon_class']
        if 'features' in data:
            service.features = json.dumps(data['features']) if isinstance(data['features'], list) else data['features']
        if 'is_active' in data:
            service.is_active = data['is_active']
        if 'is_featured' in data:
            service.is_featured = data['is_featured']
        if 'display_order' in data:
            service.display_order = data['display_order']
        if 'service_image' in data:
            service.service_image = data['service_image']
        
        db.session.commit()
        return jsonify({"success": True, "data": service.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating service: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/services/<int:id>', methods=['DELETE'])
@require_admin
def delete_service(id):
    """Delete service"""
    try:
        service = Service.query.get(id)
        if not service:
            return jsonify({"success": False, "message": "Service not found"}), 404
        
        db.session.delete(service)
        db.session.commit()
        return jsonify({"success": True, "message": "Service deleted"}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error deleting service: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# PRODUCTS SECTION MANAGEMENT
# ========================================

@admin_bp.route('/section/products', methods=['GET'])
@require_admin
def get_products_section():
    """Get all products"""
    try:
        product_type = request.args.get('type', 'all')
        query = Product.query
        
        if product_type != 'all':
            query = query.filter_by(product_type=product_type)
        
        products = query.order_by(Product.display_order).all()
        return jsonify({"success": True, "data": [p.to_dict() for p in products]}), 200
    except Exception as e:
        if logger: logger.error(f"Error getting products: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/products', methods=['POST'])
@require_admin
def create_product():
    """Create new product"""
    try:
        data = request.get_json()
        
        product = Product(
            product_type=data.get('product_type', 'buy'),
            product_name=data.get('product_name', ''),
            brand=data.get('brand', ''),
            capacity=data.get('capacity', ''),
            ac_type=data.get('ac_type', ''),
            star_rating=data.get('star_rating', 3),
            is_inverter=data.get('is_inverter', False),
            price=data.get('price', '₹0'),
            price_numeric=data.get('price_numeric', 0),
            description=data.get('description', ''),
            features=json.dumps(data.get('features', [])),
            product_image=data.get('product_image', ''),
            image_gallery=json.dumps(data.get('image_gallery', [])),
            is_available=data.get('is_available', True),
            stock_status=data.get('stock_status', 'In Stock'),
            rental_min_months=data.get('rental_min_months'),
            rental_deposit=data.get('rental_deposit', ''),
            rental_includes=json.dumps(data.get('rental_includes', [])),
            is_active=data.get('is_active', True),
            is_featured=data.get('is_featured', False),
            display_order=data.get('display_order', 0),
            badge_text=data.get('badge_text', '')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({"success": True, "data": product.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error creating product: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/products/<int:id>', methods=['PUT'])
@require_admin
def update_product(id):
    """Update product"""
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"success": False, "message": "Product not found"}), 404
        
        data = request.get_json()
        
        updatable_fields = [
            'product_type', 'product_name', 'brand', 'capacity', 'ac_type',
            'star_rating', 'is_inverter', 'price', 'price_numeric', 'description',
            'features', 'product_image', 'image_gallery', 'is_available',
            'stock_status', 'rental_min_months', 'rental_deposit', 'rental_includes',
            'is_active', 'is_featured', 'display_order', 'badge_text'
        ]
        
        for field in updatable_fields:
            if field in data:
                value = data[field]
                if field in ['features', 'image_gallery', 'rental_includes']:
                    value = json.dumps(value) if isinstance(value, list) else value
                setattr(product, field, value)
        
        db.session.commit()
        return jsonify({"success": True, "data": product.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating product: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/products/<int:id>', methods=['DELETE'])
@require_admin
def delete_product(id):
    """Delete product"""
    try:
        product = Product.query.get(id)
        if not product:
            return jsonify({"success": False, "message": "Product not found"}), 404
        
        db.session.delete(product)
        db.session.commit()
        return jsonify({"success": True, "message": "Product deleted"}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error deleting product: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# TESTIMONIALS SECTION MANAGEMENT
# ========================================

@admin_bp.route('/section/testimonials', methods=['GET'])
@require_admin
def get_testimonials():
    """Get all testimonials"""
    try:
        testimonials = Testimonial.query.order_by(Testimonial.display_order).all()
        return jsonify({"success": True, "data": [t.to_dict() for t in testimonials]}), 200
    except Exception as e:
        if logger: logger.error(f"Error getting testimonials: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/testimonials', methods=['POST'])
@require_admin
def create_testimonial():
    """Create new testimonial"""
    try:
        data = request.get_json()
        
        testimonial = Testimonial(
            customer_name=data.get('customer_name', ''),
            customer_location=data.get('customer_location', ''),
            review_text=data.get('review_text', ''),
            rating=data.get('rating', 5),
            customer_photo=data.get('customer_photo', ''),
            is_active=data.get('is_active', True),
            is_featured=data.get('is_featured', False),
            display_order=data.get('display_order', 0)
        )
        
        db.session.add(testimonial)
        db.session.commit()
        
        return jsonify({"success": True, "data": testimonial.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error creating testimonial: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/testimonials/<int:id>', methods=['PUT'])
@require_admin
def update_testimonial(id):
    """Update testimonial"""
    try:
        testimonial = Testimonial.query.get(id)
        if not testimonial:
            return jsonify({"success": False, "message": "Testimonial not found"}), 404
        
        data = request.get_json()
        
        updatable_fields = [
            'customer_name', 'customer_location', 'review_text', 'rating',
            'customer_photo', 'is_active', 'is_featured', 'display_order'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(testimonial, field, data[field])
        
        db.session.commit()
        return jsonify({"success": True, "data": testimonial.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating testimonial: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/testimonials/<int:id>', methods=['DELETE'])
@require_admin
def delete_testimonial(id):
    """Delete testimonial"""
    try:
        testimonial = Testimonial.query.get(id)
        if not testimonial:
            return jsonify({"success": False, "message": "Testimonial not found"}), 404
        
        db.session.delete(testimonial)
        db.session.commit()
        return jsonify({"success": True, "message": "Testimonial deleted"}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error deleting testimonial: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# CONTACT SECTION MANAGEMENT
# ========================================

@admin_bp.route('/section/contact', methods=['GET'])
@require_admin
def get_contact_section():
    """Get Contact section content"""
    try:
        content = WebsiteContent.query.filter_by(section_name='contact').all()
        data = {c.content_key: c.content_value for c in content}
        
        defaults = {
            'phone': '+91 9819104977',
            'email': 'anshaircool@gmail.com',
            'whatsapp': '+91 9819104977',
            'address': 'Mumbai, Maharashtra',
            'business_hours': 'Mon - Sat: 9 AM - 8 PM | Sunday: 10 AM - 6 PM',
            'google_maps_embed': '',
            'show_form': 'true'
        }
        
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        if logger: logger.error(f"Error getting contact section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/contact', methods=['PUT'])
@require_admin
def update_contact_section():
    """Update Contact section content"""
    try:
        data = request.get_json()
        
        fields = ['phone', 'email', 'whatsapp', 'address', 'business_hours', 
                  'google_maps_embed', 'show_form']
        
        for field in fields:
            if field in data:
                content = WebsiteContent.query.filter_by(
                    section_name='contact', content_key=field
                ).first()
                
                if content:
                    content.content_value = data[field]
                else:
                    content = WebsiteContent(
                        section_name='contact',
                        content_key=field,
                        content_value=data[field],
                        content_type='text'
                    )
                    db.session.add(content)
        
        db.session.commit()
        return jsonify({"success": True, "message": "Contact section updated"}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating contact section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# FOOTER SECTION MANAGEMENT
# ========================================

@admin_bp.route('/section/footer', methods=['GET'])
@require_admin
def get_footer_section():
    """Get Footer section content"""
    try:
        content = WebsiteContent.query.filter_by(section_name='footer').all()
        data = {c.content_key: c.content_value for c in content}
        
        defaults = {
            'company_name': 'Ansh Air Cool',
            'tagline': 'Professional AC Services',
            'copyright_text': '© 2026 Ansh Air Cool. All rights reserved.',
            'social_facebook': '',
            'social_instagram': '',
            'social_twitter': '',
            'social_youtube': '',
            'quick_links': json.dumps([
                {'label': 'Home', 'url': '#home'},
                {'label': 'Services', 'url': '#services'},
                {'label': 'Products', 'url': '#products'},
                {'label': 'Contact', 'url': '#contact'}
            ])
        }
        
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        if logger: logger.error(f"Error getting footer section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/footer', methods=['PUT'])
@require_admin
def update_footer_section():
    """Update Footer section content"""
    try:
        data = request.get_json()
        
        fields = ['company_name', 'tagline', 'copyright_text',
                  'social_facebook', 'social_instagram', 'social_twitter', 
                  'social_youtube', 'quick_links']
        
        for field in fields:
            if field in data:
                content = WebsiteContent.query.filter_by(
                    section_name='footer', content_key=field
                ).first()
                
                if content:
                    content.content_value = data[field]
                else:
                    content = WebsiteContent(
                        section_name='footer',
                        content_key=field,
                        content_value=data[field],
                        content_type='text' if field != 'quick_links' else 'json'
                    )
                    db.session.add(content)
        
        db.session.commit()
        return jsonify({"success": True, "message": "Footer section updated"}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating footer section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# STATS SECTION MANAGEMENT
# ========================================

@admin_bp.route('/section/stats', methods=['GET'])
@require_admin
def get_stats_section():
    """Get Stats section content"""
    try:
        content = WebsiteContent.query.filter_by(section_name='stats').all()
        data = {c.content_key: c.content_value for c in content}
        
        defaults = {
            'customers_count': '1000+',
            'customers_label': 'Happy Customers',
            'services_count': '5000+',
            'services_label': 'Services Completed',
            'experience_count': '10+',
            'experience_label': 'Years Experience',
            'technicians_count': '50+',
            'technicians_label': 'Expert Technicians'
        }
        
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        if logger: logger.error(f"Error getting stats section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/stats', methods=['PUT'])
@require_admin
def update_stats_section():
    """Update Stats section content"""
    try:
        data = request.get_json()
        
        fields = ['customers_count', 'customers_label', 'services_count', 
                  'services_label', 'experience_count', 'experience_label',
                  'technicians_count', 'technicians_label']
        
        for field in fields:
            if field in data:
                content = WebsiteContent.query.filter_by(
                    section_name='stats', content_key=field
                ).first()
                
                if content:
                    content.content_value = data[field]
                else:
                    content = WebsiteContent(
                        section_name='stats',
                        content_key=field,
                        content_value=data[field],
                        content_type='text'
                    )
                    db.session.add(content)
        
        db.session.commit()
        return jsonify({"success": True, "message": "Stats section updated"}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating stats section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# FEATURES SECTION MANAGEMENT
# ========================================

@admin_bp.route('/section/features', methods=['GET'])
@require_admin
def get_features_section():
    """Get Features section content"""
    try:
        content = WebsiteContent.query.filter_by(section_name='features').all()
        data = {c.content_key: c.content_value for c in content}
        
        defaults = {
            'title': 'Why Choose Ansh Air Cool?',
            'subtitle': 'We provide the best AC services with experienced technicians',
            'features_list': json.dumps([
                {'icon': 'fas fa-certificate', 'title': 'Certified Technicians', 'description': 'All our technicians are certified and trained'},
                {'icon': 'fas fa-clock', 'title': 'Same Day Service', 'description': 'We provide quick and efficient same-day service'},
                {'icon': 'fas fa-shield-alt', 'title': 'Warranty Protection', 'description': 'All services come with warranty protection'},
                {'icon': 'fas fa-hand-holding-usd', 'title': 'Transparent Pricing', 'description': 'No hidden charges, upfront pricing'}
            ])
        }
        
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        if logger: logger.error(f"Error getting features section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/features', methods=['PUT'])
@require_admin
def update_features_section():
    """Update Features section content"""
    try:
        data = request.get_json()
        
        fields = ['title', 'subtitle', 'features_list']
        
        for field in fields:
            if field in data:
                content = WebsiteContent.query.filter_by(
                    section_name='features', content_key=field
                ).first()
                
                if content:
                    content.content_value = data[field]
                else:
                    content = WebsiteContent(
                        section_name='features',
                        content_key=field,
                        content_value=data[field],
                        content_type='json' if field == 'features_list' else 'text'
                    )
                    db.session.add(content)
        
        db.session.commit()
        return jsonify({"success": True, "message": "Features section updated"}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating features section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# JUSTDIAL TRUST SECTION
# ========================================

@admin_bp.route('/section/justdial', methods=['GET'])
@require_admin
def get_justdial_section():
    """Get JustDial section content"""
    try:
        content = WebsiteContent.query.filter_by(section_name='justdial').all()
        data = {c.content_key: c.content_value for c in content}
        
        defaults = {
            'show_badge': 'true',
            'badge_image': '',
            'rating': '4.8',
            'review_count': '500+',
            'verified_text': 'Verified by JustDial'
        }
        
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        if logger: logger.error(f"Error getting justdial section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/section/justdial', methods=['PUT'])
@require_admin
def update_justdial_section():
    """Update JustDial section content"""
    try:
        data = request.get_json()
        
        fields = ['show_badge', 'badge_image', 'rating', 'review_count', 'verified_text']
        
        for field in fields:
            if field in data:
                content = WebsiteContent.query.filter_by(
                    section_name='justdial', content_key=field
                ).first()
                
                if content:
                    content.content_value = data[field]
                else:
                    content = WebsiteContent(
                        section_name='justdial',
                        content_key=field,
                        content_value=data[field],
                        content_type='text'
                    )
                    db.session.add(content)
        
        db.session.commit()
        return jsonify({"success": True, "message": "JustDial section updated"}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating justdial section: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# GENERAL SETTINGS
# ========================================

@admin_bp.route('/settings/site', methods=['GET'])
@require_admin
def get_site_settings():
    """Get all site settings"""
    try:
        settings = WebsiteSetting.query.all()
        data = {s.setting_key: s.setting_value for s in settings}
        
        defaults = {
            'site_title': 'Ansh Air Cool - Premium AC Services',
            'site_description': 'Professional AC Installation, Repair & Maintenance Services',
            'site_keywords': 'AC service, AC repair, AC installation, HVAC, air conditioning',
            'favicon_url': '',
            'logo_url': '',
            'analytics_code': '',
            'facebook_pixel': '',
            'whatsapp_number': '+91 9819104977',
            'enable_whatsapp': 'true'
        }
        
        for key, value in defaults.items():
            if key not in data:
                data[key] = value
        
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        if logger: logger.error(f"Error getting site settings: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/settings/site', methods=['PUT'])
@require_admin
def update_site_settings():
    """Update site settings"""
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
        return jsonify({"success": True, "message": "Site settings updated"}), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating site settings: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# IMAGE UPLOAD HELPER
# ========================================

@admin_bp.route('/upload/image', methods=['POST'])
@require_admin
def upload_image():
    """Upload image helper"""
    try:
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "No image provided"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        ext = file.filename.rsplit('.', 1)[1].lower()
        
        if ext not in allowed_extensions:
            return jsonify({"success": False, "message": "Invalid file type"}), 400
        
        # Save file
        uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'website')
        os.makedirs(uploads_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{secure_filename(file.filename)}"
        filepath = os.path.join(uploads_dir, filename)
        file.save(filepath)
        
        image_url = f"/uploads/website/{filename}"
        
        return jsonify({
            "success": True,
            "message": "Image uploaded",
            "data": {"url": image_url, "filename": filename}
        }), 200
    except Exception as e:
        if logger: logger.error(f"Error uploading image: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


# ========================================
# ADMIN PROFILE & PASSWORD MANAGEMENT
# ========================================

@admin_bp.route('/profile', methods=['GET'])
@require_admin
def get_admin_profile():
    """Get current admin profile"""
    try:
        admin_id = session.get('admin_id')
        admin = Admin.query.get(admin_id)
        
        if not admin:
            return jsonify({"success": False, "message": "Admin not found"}), 404
        
        return jsonify({
            "success": True,
            "data": {
                "id": admin.id,
                "username": admin.username,
                "full_name": admin.full_name,
                "email": admin.email,
                "phone": admin.phone,
                "is_active": admin.is_active,
                "created_at": admin.created_at.isoformat() if admin.created_at else None,
                "last_login": admin.last_login.isoformat() if admin.last_login else None
            }
        }), 200
    except Exception as e:
        if logger: logger.error(f"Error getting admin profile: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/profile', methods=['PUT'])
@require_admin
def update_admin_profile():
    """Update admin profile (name, email, phone)"""
    try:
        admin_id = session.get('admin_id')
        admin = Admin.query.get(admin_id)
        
        if not admin:
            return jsonify({"success": False, "message": "Admin not found"}), 404
        
        data = request.get_json()
        
        if 'full_name' in data:
            admin.full_name = data['full_name'].strip()
        if 'email' in data:
            admin.email = data['email'].strip().lower()
        if 'phone' in data:
            admin.phone = data['phone'].strip()
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully",
            "data": {
                "username": admin.username,
                "full_name": admin.full_name,
                "email": admin.email,
                "phone": admin.phone
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error updating admin profile: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500


@admin_bp.route('/change-password', methods=['POST'])
@require_admin
def change_admin_password():
    """Change admin password"""
    try:
        admin_id = session.get('admin_id')
        admin = Admin.query.get(admin_id)
        
        if not admin:
            return jsonify({"success": False, "message": "Admin not found"}), 404
        
        data = request.get_json()
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validation
        if not current_password:
            return jsonify({"success": False, "message": "Current password is required"}), 400
        
        if not new_password:
            return jsonify({"success": False, "message": "New password is required"}), 400
        
        if len(new_password) < 6:
            return jsonify({"success": False, "message": "New password must be at least 6 characters"}), 400
        
        if new_password != confirm_password:
            return jsonify({"success": False, "message": "New passwords do not match"}), 400
        
        # Verify current password
        if not admin.check_password(current_password):
            log_security_event('FAILED_PASSWORD_CHANGE', {'admin_id': admin_id})
            return jsonify({"success": False, "message": "Current password is incorrect"}), 401
        
        # Set new password
        admin.set_password(new_password)
        db.session.commit()
        
        log_security_event('PASSWORD_CHANGED', {'admin_id': admin_id})
        
        return jsonify({
            "success": True,
            "message": "Password changed successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        if logger: logger.error(f"Error changing admin password: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500
