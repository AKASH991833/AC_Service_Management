/**
 * ANSH AIR COOL - MAIN JAVASCRIPT
 * Main entry point - coordinates all modules
 */

// Initialize website when DOM is ready
document.addEventListener('DOMContentLoaded', async function() {
    console.log('🚀 Ansh Air Cool - Initializing...');
    
    try {
        // Step 1: Initialize UI effects
        if (typeof UIEffects !== 'undefined') {
            UIEffects.initLoadingScreen();
            UIEffects.initCursorTrail();
            UIEffects.initParticles();
        }

        // Step 2: Load all HTML sections
        if (typeof SectionsLoader !== 'undefined') {
            await Promise.all([
                SectionsLoader.loadSection('hero-section', 'sections/hero.html'),
                SectionsLoader.loadSection('justdial-section', 'sections/justdial.html'),
                SectionsLoader.loadSection('services-section', 'sections/services.html'),
                SectionsLoader.loadSection('products-section', 'sections/products.html'),
                SectionsLoader.loadSection('features-section', 'sections/features.html'),
                SectionsLoader.loadSection('stats-section', 'sections/stats.html'),
                SectionsLoader.loadSection('testimonials-section', 'sections/testimonials.html'),
                SectionsLoader.loadSection('contact-section', 'sections/contact.html'),
                SectionsLoader.loadSection('footer-section', 'sections/footer.html')
            ]);
        }

        // Step 3: Hide loading screen
        setTimeout(() => {
            const loadingScreen = document.getElementById('loading-screen');
            if (loadingScreen) {
                loadingScreen.classList.add('hidden');
            }
        }, FRONTEND_SETTINGS?.UI?.LOADING_DELAY || 1500);

        // Step 4: Initialize AOS animations
        if (typeof AOS !== 'undefined') {
            AOS.init({
                duration: 1200,
                once: false,
                offset: 120,
                delay: 0,
                easing: 'ease-out-cubic',
                mirror: true,
                anchorPlacement: 'top-bottom'
            });
        }

        // Step 5: Initialize lazy loading
        if (typeof LazyLoader !== 'undefined') {
            LazyLoader.refresh();
        }

        // Step 6: Initialize interactions
        if (typeof Interactions !== 'undefined') {
            Interactions.initSmoothScroll();
            Interactions.initNavbarScroll();
            Interactions.initStatsCounter();
            Interactions.initExpandableServices();
            Interactions.initScrollAnimations();
            Interactions.initScrollToTop();
            Interactions.initActiveNavHighlight();
        }

        // Step 7: Initialize form handlers
        initFormHandlers();

        // Step 8: Initialize product/service buttons (includes tabs)
        initProductAndServiceButtons();

        // Step 9: Initialize WhatsApp button scroll effect
        initWhatsAppScroll();

        console.log('✅ Website Ready!');
        
    } catch (error) {
        console.error('❌ Error:', error);
    }
});

/**
 * Initialize form handlers
 */
function initFormHandlers() {
    setTimeout(() => {
        const form = document.querySelector('#contactForm');
        if (!form) {
            console.warn('⚠️ Contact form not found');
            return;
        }

        console.log('📝 Setting up form validation...');
        
        // Setup validation
        if (typeof Validation !== 'undefined') {
            Validation.setupRealTimeValidation('contactForm');
        }

        // Form submit handler
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Validate form
            if (typeof Validation !== 'undefined' && !Validation.validateForm(form)) {
                if (typeof API !== 'undefined') {
                    API.showToast('Please fix the errors in the form', 'error');
                }
                return;
            }

            // Get form data
            const formData = {
                name: form.querySelector('[name="name"]')?.value?.trim() || '',
                phone: form.querySelector('[name="phone"]')?.value?.trim() || '',
                email: form.querySelector('[name="email"]')?.value?.trim() || '',
                address: form.querySelector('[name="address"]')?.value?.trim() || '',
                serviceType: form.querySelector('[name="serviceType"]')?.value?.trim() || '',
                message: form.querySelector('[name="message"]')?.value?.trim() || ''
            };

            // Sanitize data
            const sanitizedData = typeof Validation !== 'undefined' ? 
                Validation.sanitizeFormData(formData) : formData;

            // Get elements
            const submitButton = form.querySelector('button[type="submit"]');
            const loadingOverlay = document.getElementById('loadingOverlay');

            try {
                // Show loading
                if (loadingOverlay) loadingOverlay.style.display = 'flex';

                // Submit to API
                if (typeof API !== 'undefined') {
                    await API.submitContactForm(sanitizedData, submitButton);
                }

                // Reset form
                form.reset();
                if (typeof Validation !== 'undefined') {
                    Validation.clearFormValidation(form);
                }

                // Reset character counter
                const charCount = document.getElementById('charCount');
                if (charCount) charCount.textContent = '0';

                // Hide loading
                if (loadingOverlay) loadingOverlay.style.display = 'none';

                // Show success modal
                showSuccessModal(sanitizedData);

            } catch (error) {
                console.error('Form submission error:', error);
                
                // Hide loading
                if (loadingOverlay) loadingOverlay.style.display = 'none';

                // Show error
                if (typeof API !== 'undefined') {
                    if (error.message?.includes('timeout')) {
                        API.showToast('Request timed out. Check your internet.', 'error');
                    } else if (error.message?.includes('Unable to connect')) {
                        API.showToast('Cannot connect to server.', 'error');
                    } else {
                        API.showToast(error.message || 'Failed to submit.', 'error');
                    }
                }
            }
        });

        // WhatsApp direct button
        const whatsappBtn = document.getElementById('whatsappDirect');
        if (whatsappBtn) {
            whatsappBtn.addEventListener('click', function() {
                const name = form.querySelector('[name="name"]')?.value?.trim() || '';
                const phone = form.querySelector('[name="phone"]')?.value?.trim() || '';
                const serviceType = form.querySelector('[name="serviceType"]')?.value?.trim() || '';
                const message = form.querySelector('[name="message"]')?.value?.trim() || '';

                let whatsappMessage = `*New Service Inquiry* 🛠️\n\n`;
                whatsappMessage += `*Name:* ${name || 'Not provided'}\n`;
                whatsappMessage += `*Phone:* ${phone || 'Not provided'}\n`;
                if (serviceType) whatsappMessage += `*Service:* ${serviceType}\n`;
                if (message) whatsappMessage += `*Message:* ${message}\n`;
                whatsappMessage += `\n*Ansh Air Cool* ❄️`;

                const whatsappUrl = `https://wa.me/919819104977?text=${encodeURIComponent(whatsappMessage)}`;
                window.open(whatsappUrl, '_blank');
            });
            console.log('✅ WhatsApp button initialized');
        }

        // WhatsApp followup button
        const followupBtn = document.getElementById('whatsappFollowup');
        if (followupBtn) {
            followupBtn.addEventListener('click', function() {
                const refId = document.getElementById('referenceId')?.textContent || '#REF00000';
                const name = form.querySelector('[name="name"]')?.value?.trim() || 'Customer';

                let whatsappMessage = `*Follow-up on Service Request* 📋\n\n`;
                whatsappMessage += `Hi Ansh Air Cool Team,\n\n`;
                whatsappMessage += `I wanted to follow up on my service request.\n\n`;
                whatsappMessage += `*Reference ID:* ${refId}\n`;
                whatsappMessage += `*Name:* ${name}\n\n`;
                whatsappMessage += `Please confirm my booking. Thank you! 🙏`;

                const whatsappUrl = `https://wa.me/919819104977?text=${encodeURIComponent(whatsappMessage)}`;
                window.open(whatsappUrl, '_blank');
            });
            console.log('✅ WhatsApp followup button initialized');
        }

    }, 1000);
}

/**
 * Initialize product and service button handlers
 */
function initProductAndServiceButtons() {
    // Initialize product tab switching
    initProductTabs();
    
    // Service buttons
    document.addEventListener('click', function(e) {
        const serviceBtn = e.target.closest('.service-btn');
        if (serviceBtn) {
            const serviceType = serviceBtn.dataset.service;
            const contactSection = document.querySelector('#contact');
            const serviceSelect = document.querySelector('[name="serviceType"]');

            if (contactSection && serviceSelect && serviceType) {
                serviceSelect.value = serviceType;
                contactSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                // Highlight effect
                if (serviceSelect.parentElement) {
                    serviceSelect.parentElement.classList.add('highlight-field');
                    setTimeout(() => serviceSelect.parentElement.classList.remove('highlight-field'), 2000);
                }
            }
        }

        // Product buttons
        const productBtn = e.target.closest('.product-btn');
        if (productBtn) {
            const productName = productBtn.dataset.product;
            const productType = productBtn.dataset.type;
            const contactSection = document.querySelector('#contact');
            const messageField = document.querySelector('[name="message"]');
            const serviceSelect = document.querySelector('[name="serviceType"]');

            if (contactSection && messageField && productName && productType) {
                if (serviceSelect) {
                    serviceSelect.value = productType === 'buy' ? 'buy' : 'rent';
                }

                const action = productType === 'buy' ? 'purchase' : 'rent';
                messageField.value = `I am interested to ${action} ${productName}. Please contact me with more details.`;

                contactSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                
                // Highlight effect
                if (messageField.parentElement) {
                    messageField.parentElement.classList.add('highlight-field');
                    setTimeout(() => messageField.parentElement.classList.remove('highlight-field'), 2000);
                }
            }
        }
    });
}

/**
 * Initialize product tabs (Buy/Rent)
 */
function initProductTabs() {
    const tabButtons = document.querySelectorAll('.product-tabs .tab-btn');
    const tabContents = {
        buy: document.getElementById('buy-products'),
        rent: document.getElementById('rent-products')
    };

    tabButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.dataset.tab;

            // Remove active class from all buttons and contents
            tabButtons.forEach(b => b.classList.remove('active'));
            if (tabContents.buy) tabContents.buy.classList.remove('active');
            if (tabContents.rent) tabContents.rent.classList.remove('active');

            // Add active class to clicked button and corresponding content
            this.classList.add('active');
            if (tabContents[targetTab]) {
                tabContents[targetTab].classList.add('active');
                
                // Refresh lazy loader for newly visible images
                if (typeof LazyLoader !== 'undefined') {
                    setTimeout(() => LazyLoader.refresh(), 100);
                }
            }
        });
    });
}

/**
 * Show success modal
 */
function showSuccessModal(data) {
    const refId = '#REF' + Math.floor(10000 + Math.random() * 90000);
    const refElement = document.getElementById('referenceId');
    if (refElement) refElement.textContent = refId;

    const modalElement = document.getElementById('successModal');
    if (modalElement && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalElement, {
            backdrop: 'static',
            keyboard: false
        });
        modal.show();
    }
}

/**
 * Initialize WhatsApp button scroll effect
 * Button stays visible while scrolling
 */
function initWhatsAppScroll() {
    const whatsappBtn = document.querySelector('.whatsapp-float');
    if (!whatsappBtn) return;

    let lastScroll = 0;
    let ticking = false;

    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const currentScroll = window.pageYOffset;

                // WhatsApp button hamesha dikhega (always visible)
                // Bas thoda sa adjust hoga scroll direction ke hisaab se
                if (currentScroll > 100) {
                    // Scroll down - button visible rahega
                    whatsappBtn.style.opacity = '1';
                    whatsappBtn.style.visibility = 'visible';
                } else {
                    // Top pe thoda transparent
                    whatsappBtn.style.opacity = '0.8';
                    whatsappBtn.style.visibility = 'visible';
                }

                lastScroll = currentScroll;
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });

    console.log('✅ WhatsApp scroll effect initialized');
}
