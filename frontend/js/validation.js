/**
 * Form Validation Module - ENHANCED
 * Real-time validation with visual feedback
 */

const Validation = (function() {
    'use strict';

    // Validation state tracking
    const fieldStates = {};

    /**
     * Validate phone number (Indian format)
     */
    function isValidPhone(phone) {
        const phoneRegex = /^[6-9]\d{9}$/;
        return phoneRegex.test(phone.replace(/\s/g, ''));
    }

    /**
     * Validate email
     */
    function isValidEmail(email) {
        if (!email || email.trim().length === 0) return true; // Optional field
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Validate required field
     */
    function isRequired(value) {
        return value && value.trim().length > 0;
    }

    /**
     * Validate minimum length
     */
    function minLength(value, length) {
        return value && value.length >= length;
    }

    /**
     * Validate maximum length
     */
    function maxLength(value, length) {
        return value && value.length <= length;
    }

    /**
     * Show field success state
     */
    function showFieldSuccess(field) {
        const inputWrapper = field.closest('.input-wrapper');
        if (inputWrapper) {
            inputWrapper.classList.add('is-valid');
            inputWrapper.classList.remove('is-invalid');
            
            // Update validation icon
            const validationIcon = inputWrapper.querySelector('.validation-icon');
            if (validationIcon) {
                validationIcon.innerHTML = '<i class="fas fa-check"></i>';
                validationIcon.classList.add('valid');
            }
        }
        
        // Clear any error messages
        const errorDiv = field.closest('.form-group')?.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.textContent = '';
            errorDiv.style.display = 'none';
        }
        
        fieldStates[field.name] = { valid: true, touched: true };
    }

    /**
     * Show field error
     */
    function showFieldError(field, message) {
        const inputWrapper = field.closest('.input-wrapper');
        if (inputWrapper) {
            inputWrapper.classList.add('is-invalid');
            inputWrapper.classList.remove('is-valid');
            
            // Update validation icon
            const validationIcon = inputWrapper.querySelector('.validation-icon');
            if (validationIcon) {
                validationIcon.innerHTML = '<i class="fas fa-exclamation"></i>';
                validationIcon.classList.add('invalid');
            }
        }
        
        // Show error message
        const errorDiv = field.closest('.form-group')?.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
        
        fieldStates[field.name] = { valid: false, touched: true };
    }

    /**
     * Clear field validation state
     */
    function clearFieldValidation(field) {
        const inputWrapper = field.closest('.input-wrapper');
        if (inputWrapper) {
            inputWrapper.classList.remove('is-valid', 'is-invalid');
            
            // Reset validation icon
            const validationIcon = inputWrapper.querySelector('.validation-icon');
            if (validationIcon) {
                validationIcon.innerHTML = '';
                validationIcon.classList.remove('valid', 'invalid');
            }
        }
        
        const errorDiv = field.closest('.form-group')?.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.textContent = '';
            errorDiv.style.display = 'none';
        }
        
        fieldStates[field.name] = { valid: false, touched: false };
    }

    /**
     * Clear all form validation
     */
    function clearFormValidation(form) {
        form.querySelectorAll('.form-control').forEach(field => {
            clearFieldValidation(field);
        });
        Object.keys(fieldStates).forEach(key => delete fieldStates[key]);
    }

    /**
     * Validate single field with visual feedback
     */
    function validateField(field) {
        const value = field.value.trim();
        const name = field.name;
        
        // Name validation
        if (name === 'name') {
            if (!isRequired(value)) {
                showFieldError(field, 'Name is required');
                return false;
            } else if (!minLength(value, 2)) {
                showFieldError(field, 'Name must be at least 2 characters');
                return false;
            } else if (!maxLength(value, 50)) {
                showFieldError(field, 'Name must be less than 50 characters');
                return false;
            }
            showFieldSuccess(field);
            return true;
        }
        
        // Phone validation
        if (name === 'phone') {
            if (!isRequired(value)) {
                showFieldError(field, 'Mobile number is required');
                return false;
            } else if (!isValidPhone(value)) {
                showFieldError(field, 'Enter a valid 10-digit Indian mobile number (starting with 6-9)');
                return false;
            }
            showFieldSuccess(field);
            return true;
        }
        
        // Email validation (optional)
        if (name === 'email') {
            if (value && !isValidEmail(value)) {
                showFieldError(field, 'Please enter a valid email address');
                return false;
            }
            if (value) {
                showFieldSuccess(field);
            } else {
                clearFieldValidation(field);
            }
            return true;
        }
        
        // Service type validation
        if (name === 'serviceType') {
            if (!isRequired(value)) {
                showFieldError(field, 'Please select a service type');
                return false;
            }
            showFieldSuccess(field);
            return true;
        }
        
        // Message validation (optional)
        if (name === 'message') {
            if (value && !maxLength(value, 500)) {
                showFieldError(field, 'Message must be less than 500 characters');
                return false;
            }
            return true;
        }
        
        return true;
    }

    /**
     * Validate entire form
     */
    function validateForm(form) {
        let isValid = true;
        let firstInvalidField = null;
        
        const fields = form.querySelectorAll('.form-control[required]');
        fields.forEach(field => {
            if (!validateField(field)) {
                isValid = false;
                if (!firstInvalidField) {
                    firstInvalidField = field;
                }
            }
        });
        
        // Focus on first invalid field
        if (firstInvalidField) {
            firstInvalidField.focus();
        }
        
        return isValid;
    }

    /**
     * Check if form is ready to submit
     */
    function isFormValid(form) {
        const requiredFields = form.querySelectorAll('.form-control[required]');
        let allValid = true;
        
        requiredFields.forEach(field => {
            if (!validateField(field)) {
                allValid = false;
            }
        });
        
        return allValid;
    }

    /**
     * Setup real-time validation listeners
     */
    function setupRealTimeValidation(formId) {
        const form = document.getElementById(formId);
        if (!form) return;
        
        // Validate on blur
        form.querySelectorAll('.form-control').forEach(field => {
            field.addEventListener('blur', () => {
                fieldStates[field.name] = fieldStates[field.name] || { valid: false, touched: true };
                validateField(field);
            });
            
            // Validate on input (after first touch)
            field.addEventListener('input', () => {
                if (fieldStates[field.name]?.touched) {
                    validateField(field);
                }
            });
            
            // Validate select on change
            if (field.tagName === 'SELECT') {
                field.addEventListener('change', () => {
                    validateField(field);
                });
            }
        });
        
        // Character counter for textarea
        const messageField = form.querySelector('textarea[name="message"]');
        const charCount = document.getElementById('charCount');
        if (messageField && charCount) {
            messageField.addEventListener('input', () => {
                charCount.textContent = messageField.value.length;
                if (messageField.value.length > 450) {
                    charCount.style.color = '#ff4444';
                } else if (messageField.value.length > 300) {
                    charCount.style.color = '#ffa500';
                } else {
                    charCount.style.color = '#00f5ff';
                }
            });
        }
    }

    /**
     * Validate contact form data
     */
    function validateContactForm(formData) {
        const errors = [];

        // Validate name
        if (!isRequired(formData.name)) {
            errors.push('Name is required');
        } else if (!minLength(formData.name, 2)) {
            errors.push('Name must be at least 2 characters');
        }

        // Validate phone
        if (!isRequired(formData.phone)) {
            errors.push('Phone number is required');
        } else if (!isValidPhone(formData.phone)) {
            errors.push('Please enter a valid 10-digit mobile number');
        }

        // Validate service type
        if (!isRequired(formData.serviceType)) {
            errors.push('Please select a service type');
        }

        // Validate email (optional)
        if (formData.email && !isValidEmail(formData.email)) {
            errors.push('Please enter a valid email address');
        }

        // Validate message length
        if (formData.message && !maxLength(formData.message, 500)) {
            errors.push('Message must be less than 500 characters');
        }

        return errors;
    }

    /**
     * Validate service request form
     */
    function validateServiceRequest(formData) {
        const errors = [];

        // Validate name
        if (!isRequired(formData.name)) {
            errors.push('Name is required');
        } else if (!minLength(formData.name, 2)) {
            errors.push('Name must be at least 2 characters');
        }

        // Validate phone
        if (!isRequired(formData.phone)) {
            errors.push('Phone number is required');
        } else if (!isValidPhone(formData.phone)) {
            errors.push('Please enter a valid 10-digit mobile number');
        }

        // Validate address
        if (!isRequired(formData.address)) {
            errors.push('Address is required');
        }

        // Validate service type
        if (!isRequired(formData.serviceType)) {
            errors.push('Please select a service type');
        }

        return errors;
    }

    /**
     * Sanitize form data
     */
    function sanitizeFormData(formData) {
        const sanitized = {};
        for (const [key, value] of Object.entries(formData)) {
            sanitized[key] = sanitizeInput(value);
        }
        return sanitized;
    }

    /**
     * Get field validation state
     */
    function getFieldState(fieldName) {
        return fieldStates[fieldName] || { valid: false, touched: false };
    }

    /**
     * Get all field states
     */
    function getAllFieldStates() {
        return { ...fieldStates };
    }

    // ========================================
    // SECURITY FUNCTIONS
    // ========================================

    /**
     * CSRF Token Management
     */
    let csrfToken = null;

    /**
     * Get or generate CSRF token
     */
    function getCsrfToken() {
        if (csrfToken) {
            return csrfToken;
        }
        
        // Try to get from cookie
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrf_token') {
                csrfToken = value;
                return value;
            }
        }
        
        // Generate new token if not found
        csrfToken = generateCsrfToken();
        return csrfToken;
    }

    /**
     * Generate a random CSRF token
     */
    function generateCsrfToken() {
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Validate CSRF token (client-side check)
     */
    function validateCsrfToken(token) {
        return token && token.length === 64 && /^[0-9a-f]+$/.test(token);
    }

    /**
     * Enhanced input sanitization - prevents XSS
     */
    function sanitizeInput(input) {
        if (typeof input !== 'string') return input;
        
        // First pass: HTML entity encode
        const div = document.createElement('div');
        div.textContent = input;
        let sanitized = div.innerHTML;
        
        // Second pass: Remove potentially dangerous patterns
        const dangerousPatterns = [
            /<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi,
            /javascript:/gi,
            /on\w+\s*=/gi,
            /data:text\/html/gi,
            /vbscript:/gi
        ];
        
        for (const pattern of dangerousPatterns) {
            sanitized = sanitized.replace(pattern, '');
        }
        
        return sanitized;
    }

    /**
     * Sanitize HTML (allow limited tags)
     */
    function sanitizeHtml(input, allowedTags = []) {
        if (typeof input !== 'string') return input;
        
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = input;
        
        // Remove disallowed tags
        const allElements = tempDiv.querySelectorAll('*');
        allElements.forEach(el => {
            const tagName = el.tagName.toLowerCase();
            if (!allowedTags.includes(tagName)) {
                // Replace with text content
                const textNode = document.createTextNode(el.textContent);
                el.parentNode.replaceChild(textNode, el);
            } else {
                // Remove dangerous attributes
                const attributes = Array.from(el.attributes);
                attributes.forEach(attr => {
                    const name = attr.name.toLowerCase();
                    if (name.startsWith('on') || name === 'style') {
                        el.removeAttribute(attr.name);
                    }
                });
            }
        });
        
        return tempDiv.innerHTML;
    }

    /**
     * Validate file upload (type and size)
     */
    function validateFileUpload(file, options = {}) {
        const {
            maxSize = 5 * 1024 * 1024, // 5MB default
            allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        } = options;

        const errors = [];

        if (!file) {
            errors.push('No file selected');
            return errors;
        }

        // Check file size
        if (file.size > maxSize) {
            errors.push(`File size must be less than ${maxSize / 1024 / 1024}MB`);
        }

        // Check file type
        if (!allowedTypes.includes(file.type)) {
            errors.push(`File type not allowed. Allowed: ${allowedTypes.join(', ')}`);
        }

        return errors;
    }

    /**
     * Encode for safe HTML insertion
     */
    function encodeForHtml(text) {
        if (typeof text !== 'string') return text;
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Public API
    return {
        isValidPhone,
        isValidEmail,
        isRequired,
        minLength,
        maxLength,
        showFieldSuccess,
        showFieldError,
        clearFieldValidation,
        clearFormValidation,
        validateField,
        validateForm,
        isFormValid,
        setupRealTimeValidation,
        validateContactForm,
        validateServiceRequest,
        sanitizeInput,
        sanitizeFormData,
        getFieldState,
        getAllFieldStates,
        // Security functions
        getCsrfToken,
        generateCsrfToken,
        validateCsrfToken,
        sanitizeHtml,
        validateFileUpload,
        encodeForHtml
    };
})();
