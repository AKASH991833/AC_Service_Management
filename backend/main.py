"""
Ansh Air Cool - Backend API
Flask REST API for service requests and contact forms
Security Hardened Version
"""

from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from dotenv import load_dotenv
import os
import logging
from datetime import timedelta
from logging_config import setup_logging

# Load environment variables
load_dotenv()

# Setup logging first
loggers = setup_logging()
logger = loggers['app']
security_logger = loggers['security']
admin_logger = loggers['admin']

from models import db, ServiceRequest, ContactMessage
from routes import api_bp
from admin_routes import admin_bp
from security import init_security, add_security_headers


def create_app():
    """Application factory for Flask app"""
    app = Flask(__name__)

    # ========================================
    # SECURITY CONFIGURATION
    # ========================================

    # Secret key for sessions - MUST be set in environment
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    if not app.config['SECRET_KEY'] or 'CHANGE_THIS' in app.config['SECRET_KEY'] or 'change_this' in app.config['SECRET_KEY']:
        logger.error("❌ CRITICAL: SECRET_KEY not properly configured!")
        logger.error("Please set a secure SECRET_KEY in .env file")
        logger.error("Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\"")
        raise ValueError("SECRET_KEY must be set to a secure random value in production")

    # Session Security - Production Hardened
    app.config['SESSION_COOKIE_NAME'] = 'ansh_admin_session'
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV') == 'production'  # HTTPS only
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/ansh_aircool')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    app.config['JSON_SORT_KEYS'] = False

    # File Upload Security
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'gallery'), exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)

    # ========================================
    # CORS CONFIGURATION (Secure)
    # ========================================
    allowed_origins = [
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5000",
        "http://127.0.0.1:5000"
    ]

    # In production, only allow specific origins
    if os.getenv('FLASK_ENV') == 'production':
        allowed_origins = [os.getenv('FRONTEND_URL', 'https://yourdomain.com')]

    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-API-KEY", "X-CSRF-Token"],
            "supports_credentials": True,
            "expose_headers": ["Content-Type", "Authorization", "Set-Cookie"],
            "max_age": 3600
        }
    })

    # Rate limiting configuration (Increased for development)
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["1000 per day", "100 per hour"],  # Increased limits
        storage_uri="memory://",
        enabled=os.getenv('RATELIMIT_ENABLED', 'true').lower() == 'true'
    )

    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin-full')

    # Initialize security measures
    init_security(app)

    # Security Headers Middleware
    @app.after_request
    def add_security_headers(response):
        """Add comprehensive security headers to all responses"""
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # XSS Protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # HSTS (force HTTPS in production)
        if os.getenv('FLASK_ENV') == 'production':
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Content Security Policy (relaxed for development)
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https: blob:; "
            "connect-src 'self' http://localhost:5000 http://127.0.0.1:5000 http://localhost:5500 http://127.0.0.1:5500; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        response.headers['Content-Security-Policy'] = csp_policy
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Cache Control for admin endpoints (prevent sensitive data caching)
        if request.endpoint and 'admin' in request.endpoint:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        
        return response

    # Health check endpoint (no auth required)
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "message": "API is running"}), 200

    # Serve uploaded images
    @app.route('/uploads/gallery/<filename>')
    def serve_uploaded_image(filename):
        """Serve uploaded gallery images"""
        from flask import send_from_directory
        uploads_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'gallery')
        return send_from_directory(uploads_dir, filename)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f"404 - Endpoint not found: {request.path}")
        return jsonify({"success": False, "message": "Endpoint not found"}), 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        logger.warning(f"429 - Rate limit exceeded: {request.remote_addr}")
        return jsonify({"success": False, "message": "Rate limit exceeded. Please try again later."}), 429

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 - Internal error: {str(error)}")
        # Log full traceback for debugging
        import traceback
        logger.error(traceback.format_exc())
        # Return safe error to client
        return jsonify({"success": False, "message": "Internal server error"}), 500

    @app.errorhandler(400)
    def bad_request(error):
        logger.warning(f"400 - Bad request: {str(error)}")
        return jsonify({"success": False, "message": "Bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        logger.warning(f"401 - Unauthorized access attempt: {request.remote_addr}")
        return jsonify({"success": False, "message": "Unauthorized access"}), 401

    return app


if __name__ == '__main__':
    app = create_app()

    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("✅ Database tables created successfully!")

    # Run the application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Security warning for debug mode
    if debug:
        logger.warning("⚠️  WARNING: Debug mode is enabled! Disable in production!")
    
    # Log security configuration
    logger.info("=" * 50)
    logger.info("🔒 SECURITY CONFIGURATION")
    logger.info("=" * 50)
    logger.info(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    logger.info(f"Debug Mode: {debug}")
    logger.info(f"Rate Limiting: {os.getenv('RATELIMIT_ENABLED', 'true')}")
    logger.info(f"Security Headers: Enabled")
    logger.info(f"CORS Origins: localhost only")
    logger.info("=" * 50)
    
    logger.info(f"🚀 Starting Flask server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=debug, use_reloader=False)
