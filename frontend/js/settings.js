/**
 * Frontend Settings
 * 
 * ⚠️ SECURITY NOTICE:
 * - API_KEY is visible in browser - this is intentional for frontend apps
 * - In production, use a backend proxy to hide sensitive operations
 * - Change DEFAULT_API_KEY before deploying to production
 * - Backend validates API_KEY against environment variable
 */

const FRONTEND_SETTINGS = {
    // Backend API URL
    // Change this to your production URL when deploying
    API_BASE_URL: window.location.hostname === 'localhost' 
        ? 'http://localhost:5000' 
        : window.location.origin.replace(/:\d+$/, ':5000'),

    /**
     * ⚠️ PRODUCTION SECURITY:
     * This key is visible in browser source code.
     * Backend validates this key, but sensitive operations
     * should use session-based authentication.
     * 
     * For production:
     * 1. Change this key in backend .env file
     * 2. Use HTTPS only
     * 3. Implement rate limiting
     * 4. Add CSRF protection
     */
    API_KEY: 'ansh_aircool_website_key_2026',

    // Feature flags
    FEATURES: {
        ENABLE_WHATSAPP: true,
        ENABLE_ANALYTICS: false,
        ENABLE_CACHE: true
    },

    // UI Settings
    UI: {
        LOADING_DELAY: 1500,
        TOAST_DURATION: 5000,
        SCROLL_SMOOTH: true
    }
};

// Freeze to prevent modifications
Object.freeze(FRONTEND_SETTINGS);
Object.freeze(FRONTEND_SETTINGS.FEATURES);
Object.freeze(FRONTEND_SETTINGS.UI);
