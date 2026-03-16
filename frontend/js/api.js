/**
 * API Module
 * Centralized API calls with error handling, loading states, and security
 */

const API = (function() {
    'use strict';

    /**
     * Show loading state on button
     */
    function setLoading(button, isLoading) {
        if (!button) return;

        if (isLoading) {
            button.disabled = true;
            const originalText = button.innerHTML;
            button.dataset.originalText = originalText;
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        } else {
            button.disabled = false;
            if (button.dataset.originalText) {
                button.innerHTML = button.dataset.originalText;
            }
        }
    }

    /**
     * Show toast notification
     */
    function showToast(message, type = 'success') {
        // Remove existing toast if any
        const existingToast = document.querySelector('.api-toast');
        if (existingToast) {
            existingToast.remove();
        }

        // Create toast element
        const toast = document.createElement('div');
        toast.className = `api-toast api-toast-${type}`;
        toast.innerHTML = `
            <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} me-2"></i>
            ${message}
        `;

        // Add styles
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 9999;
            animation: slideIn 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        `;

        if (type === 'success') {
            toast.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
        } else {
            toast.style.background = 'linear-gradient(135deg, #dc3545, #c82333)';
        }

        document.body.appendChild(toast);

        // Auto remove after 5 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }

    /**
     * Handle API response
     */
    async function handleResponse(response) {
        if (!response.ok) {
            const error = await response.json().catch(() => ({
                message: 'An unexpected error occurred'
            }));
            throw new Error(error.message || `HTTP error! status: ${response.status}`);
        }
        return response.json();
    }

    /**
     * Get CSRF token from validation module or generate one
     */
    function getCsrfToken() {
        if (typeof Validation !== 'undefined' && Validation.getCsrfToken) {
            return Validation.getCsrfToken();
        }
        // Fallback: generate token
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Make API request with retry logic and security headers
     */
    async function request(endpoint, options = {}) {
        const url = `${API_CONFIG.BASE_URL}${endpoint}`;

        // Get CSRF token for state-changing requests
        const csrfToken = getCsrfToken();

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-API-KEY': API_CONFIG.API_KEY,
                'X-CSRF-Token': csrfToken
            },
            credentials: 'include',
            timeout: API_CONFIG.TIMEOUT
        };

        const config = { ...defaultOptions, ...options };

        // Merge headers
        config.headers = { ...defaultOptions.headers, ...(options.headers || {}) };

        // Add timeout handling
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), config.timeout);
        config.signal = controller.signal;

        try {
            const response = await fetch(url, config);
            clearTimeout(timeoutId);
            return await handleResponse(response);
        } catch (error) {
            clearTimeout(timeoutId);

            if (error.name === 'AbortError') {
                throw new Error('Request timeout. Please try again.');
            }

            if (error.message.includes('Failed to fetch')) {
                throw new Error('Unable to connect to server. Please check your connection.');
            }

            throw error;
        }
    }

    /**
     * Submit service request with enhanced validation
     */
    async function submitServiceRequest(data, button) {
        setLoading(button, true);

        try {
            // Sanitize data before sending
            const sanitizedData = (typeof Validation !== 'undefined' && Validation.sanitizeFormData)
                ? Validation.sanitizeFormData(data)
                : data;

            const response = await request(API_CONFIG.ENDPOINTS.SERVICE_REQUEST, {
                method: 'POST',
                body: JSON.stringify(sanitizedData)
            });

            showToast(response.message || 'Service request submitted successfully!', 'success');
            return response;
        } catch (error) {
            console.error('Service Request Error:', error);
            showToast(error.message || 'Failed to submit request. Please try again.', 'error');
            throw error;
        } finally {
            setLoading(button, false);
        }
    }

    /**
     * Submit contact form with enhanced validation
     */
    async function submitContactForm(data, button) {
        setLoading(button, true);

        try {
            // Sanitize data before sending
            const sanitizedData = (typeof Validation !== 'undefined' && Validation.sanitizeFormData)
                ? Validation.sanitizeFormData(data)
                : data;

            const response = await request(API_CONFIG.ENDPOINTS.CONTACT, {
                method: 'POST',
                body: JSON.stringify(sanitizedData)
            });

            showToast(response.message || 'Message sent successfully! We will contact you soon.', 'success');
            return response;
        } catch (error) {
            console.error('Contact Form Error:', error);
            showToast(error.message || 'Failed to send message. Please try again.', 'error');
            throw error;
        } finally {
            setLoading(button, false);
        }
    }

    // Public API
    return {
        submitServiceRequest,
        submitContactForm,
        showToast,
        request,
        setLoading
    };
})();

// Add CSS animations for toast
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
