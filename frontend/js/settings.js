/**
 * Frontend Settings - Production Ready
 *
 * SECURITY NOTES:
 * - Public endpoints (service-request, contact) do NOT require API keys
 * - Admin endpoints use SESSION-BASED authentication (secure)
 * - Rate limiting protects against abuse
 * - All sensitive operations require admin login
 *
 * For production deployment:
 * 1. Use HTTPS
 * 2. Set proper CORS origins in backend
 * 3. Configure rate limiting
 * 4. Set secure SECRET_KEY in backend .env
 */

const FRONTEND_SETTINGS = Object.freeze({
    // Backend API URL - Auto-detects based on environment
    API_BASE_URL: window.location.hostname === 'localhost'
        ? 'http://localhost:5000'
        : window.location.origin.replace(/:\d+$/, ':5000'),

    // Feature flags
    FEATURES: {
        ENABLE_WHATSAPP: true,
        ENABLE_ANALYTICS: false,
        ENABLE_CACHE: true
    },

    // UI Settings
    UI: Object.freeze({
        LOADING_DELAY: 1500,
        TOAST_DURATION: 5000,
        SCROLL_SMOOTH: true
    }),

    // API Endpoints
    ENDPOINTS: Object.freeze({
        SERVICE_REQUEST: '/api/service-request',
        CONTACT: '/api/contact',
        ADMIN_LOGIN: '/api/admin/login',
        ADMIN_LOGOUT: '/api/admin/logout',
        ADMIN_STATS: '/api/admin/stats'
    })
});

/**
 * API Client Configuration
 * 
 * SECURITY IMPROVEMENT:
 * - Public endpoints: No authentication required
 * - Admin endpoints: Session-based authentication (cookies)
 * - NO hardcoded API keys in frontend code
 */
const API_CONFIG = Object.freeze({
    BASE_URL: FRONTEND_SETTINGS.API_BASE_URL,
    ENDPOINTS: FRONTEND_SETTINGS.ENDPOINTS,
    TIMEOUT: 30000,
    RETRY_ATTEMPTS: 2,
    RETRY_DELAY: 1000,
    HEADERS: {
        'Content-Type': 'application/json'
    },
    // Session-based auth - credentials included automatically
    CREDENTIALS: 'include'
});
