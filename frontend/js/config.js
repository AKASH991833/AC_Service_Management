/**
 * API Configuration
 * 
 * ⚠️ SECURITY NOTICE:
 * - This configuration is visible in browser
 * - Backend validates all requests with API_KEY
 * - Session-based auth required for admin operations
 * - Rate limiting applied on backend
 */

const API_CONFIG = Object.freeze({
    // Base URL - loaded from settings.js with fallback
    BASE_URL: (typeof FRONTEND_SETTINGS !== 'undefined' && FRONTEND_SETTINGS.API_BASE_URL) || 
              'http://localhost:5000',

    // API Key - must match backend .env API_KEY
    // ⚠️ Changed from default - update backend .env file
    API_KEY: (typeof FRONTEND_SETTINGS !== 'undefined' && FRONTEND_SETTINGS.API_KEY) || 
             'ansh_aircool_website_key_2026',

    // API Endpoints (Public)
    ENDPOINTS: Object.freeze({
        SERVICE_REQUEST: '/api/service-request',
        CONTACT: '/api/contact'
    }),

    // Request Configuration
    TIMEOUT: 30000,        // 30 seconds
    RETRY_ATTEMPTS: 2,
    RETRY_DELAY: 1000
});
