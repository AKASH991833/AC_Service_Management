/**
 * Dynamic Content Loader
 * Loads website content from Admin Panel API
 * Makes all sections dynamic and editable from admin
 * 
 * NOTE: This uses admin endpoints which require authentication.
 * For production, create separate public API endpoints.
 */

const DynamicContent = (function() {
    'use strict';

    // API Configuration - with proper fallbacks
    const API_BASE = (typeof API_CONFIG !== 'undefined' && API_CONFIG.BASE_URL) || 
                     (typeof FRONTEND_SETTINGS !== 'undefined' && FRONTEND_SETTINGS.API_BASE_URL) || 
                     'http://localhost:5000';
    const API_KEY = (typeof API_CONFIG !== 'undefined' && API_CONFIG.API_KEY) || 
                    (typeof FRONTEND_SETTINGS !== 'undefined' && FRONTEND_SETTINGS.API_KEY) || 
                    'ansh_aircool_website_key_2026';

    /**
     * Safe API fetch with error handling
     */
    async function safeFetch(endpoint) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-KEY': API_KEY
                },
                credentials: 'include',
                signal: AbortSignal.timeout(5000) // 5 second timeout
            });

            if (response.ok) {
                return await response.json();
            }
            return null; // API unavailable or error
        } catch (error) {
            // Silent fail - use default content
            if (error.name !== 'AbortError') {
                console.log(`⚠️ API endpoint ${endpoint} unavailable, using default content`);
            }
            return null;
        }
    }

    /**
     * Load Hero Section from API
     */
    async function loadHeroSection() {
        try {
            const result = await safeFetch('/api/admin-full/section/hero');
            
            if (result && result.data) {
                const data = result.data || {};

                // Update Hero Section
                const heroTitle = document.querySelector('#hero-section h1');
                const heroSubtitle = document.querySelector('#hero-section .hero-subtitle');
                const ctaBtn = document.querySelector('#hero-section .hero-cta a.btn-primary-glow');

                if (heroTitle && data.title) heroTitle.textContent = data.title;
                if (heroSubtitle && data.subtitle) heroSubtitle.innerHTML = data.subtitle;
                if (ctaBtn && data.cta_text) ctaBtn.innerHTML = `<i class="fas fa-calendar-check me-2"></i>${data.cta_text}`;

                console.log('✅ Hero section loaded from API');
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Load Services from API
     */
    async function loadServices() {
        try {
            const result = await safeFetch('/api/admin-full/section/services');
            
            if (result && result.data && result.data.length > 0) {
                const services = result.data || [];

                if (services.length > 0) {
                    const servicesContainer = document.querySelector('#services-section .row.g-4');
                    if (servicesContainer) {
                        servicesContainer.innerHTML = services.map(service => {
                            const features = typeof service.features === 'string'
                                ? JSON.parse(service.features)
                                : (service.features || []);

                            return `
                                <div class="col-lg-4 col-md-6" data-aos="fade-up">
                                    <div class="service-card glass-card">
                                        <div class="service-icon">
                                            <i class="${service.icon_class || 'fas fa-tools'}"></i>
                                        </div>
                                        <h3 class="service-title">${service.service_name}</h3>
                                        <p class="service-description">${service.description || ''}</p>
                                        <div class="service-features">
                                            ${features.map(f => `<span class="feature-tag">${f}</span>`).join('')}
                                        </div>
                                        <div class="service-footer">
                                            <span class="service-price">${service.starting_price || '₹0'}</span>
                                            <button class="service-btn" data-service="${service.service_slug}">
                                                Book Now <i class="fas fa-arrow-right"></i>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            `;
                        }).join('');
                        console.log('✅ Services loaded from API');
                    }
                }
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Load Products from API
     */
    async function loadProducts() {
        try {
            const result = await safeFetch('/api/admin-full/section/products');
            
            if (result && result.data && result.data.length > 0) {
                const products = result.data || [];

                if (products.length > 0) {
                    // Separate buy and rent products
                    const buyProducts = products.filter(p => p.product_type === 'buy');
                    const rentProducts = products.filter(p => p.product_type === 'rent');

                    // Update Buy Products
                    const buyContainer = document.querySelector('#buy-products .row.g-4');
                    if (buyContainer && buyProducts.length > 0) {
                        buyContainer.innerHTML = buyProducts.map(product => createProductCard(product)).join('');
                    }

                    // Update Rent Products
                    const rentContainer = document.querySelector('#rent-products .row.g-4');
                    if (rentContainer && rentProducts.length > 0) {
                        rentContainer.innerHTML = rentProducts.map(product => createProductCard(product)).join('');
                    }

                    console.log('✅ Products loaded from API');
                }
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Create product card HTML
     */
    function createProductCard(product) {
        const features = typeof product.features === 'string' 
            ? JSON.parse(product.features) 
            : (product.features || []);

        return `
            <div class="col-lg-4 col-md-6" data-aos="zoom-in">
                <div class="product-card glass-card">
                    ${product.badge_text ? `<div class="product-badge">${product.badge_text}</div>` : ''}
                    <div class="product-image">
                        <img src="${product.product_image || 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=500'}" 
                             alt="${product.product_name}" class="lazy">
                    </div>
                    <div class="product-details">
                        <h3 class="product-name">${product.product_name}</h3>
                        <div class="product-specs">
                            <span><i class="fas fa-snowflake"></i> ${product.capacity || '1.5 Ton'}</span>
                            <span><i class="fas fa-star"></i> ${product.star_rating || '5'} Star</span>
                            <span><i class="fas fa-wind"></i> ${product.ac_type || 'Split'}</span>
                        </div>
                        <ul class="product-features">
                            ${features.slice(0, 3).map(f => `<li><i class="fas fa-check"></i> ${f}</li>`).join('')}
                        </ul>
                        <div class="product-footer">
                            <div class="product-price">${product.price || '₹0'}</div>
                            <button class="product-btn ${product.product_type}-btn" 
                                    data-product="${product.product_name}" 
                                    data-type="${product.product_type}">
                                ${product.product_type === 'buy' ? 'Buy Now' : 'Rent Now'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Load Testimonials from API
     */
    async function loadTestimonials() {
        try {
            const result = await safeFetch('/api/admin-full/section/testimonials');
            
            if (result && result.data && result.data.length > 0) {
                const testimonials = result.data || [];

                if (testimonials.length > 0) {
                    const testimonialsContainer = document.querySelector('#testimonials-section .testimonials-grid');
                    if (testimonialsContainer) {
                        testimonialsContainer.innerHTML = testimonials.map(t => `
                            <div class="testimonial-card glass-card" data-aos="fade-up">
                                <div class="testimonial-rating">${'⭐'.repeat(t.rating)}</div>
                                <p class="testimonial-text">"${t.review_text}"</p>
                                <div class="testimonial-author">
                                    <div class="author-info">
                                        <h4>${t.customer_name}</h4>
                                        <p>${t.customer_location || 'Happy Customer'}</p>
                                    </div>
                                </div>
                            </div>
                        `).join('');
                        console.log('✅ Testimonials loaded from API');
                    }
                }
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Load Features Section from API
     */
    async function loadFeatures() {
        try {
            const result = await safeFetch('/api/admin-full/section/features');
            
            if (result && result.data) {
                const data = result.data || {};

                // Update section title and subtitle
                const featuresTitle = document.querySelector('#features-section .section-title');
                const featuresSubtitle = document.querySelector('#features-section .section-subtitle');

                if (featuresTitle && data.title) featuresTitle.textContent = data.title;
                if (featuresSubtitle && data.subtitle) featuresSubtitle.textContent = data.subtitle;

                // Update features list if available
                if (data.features_list) {
                    const features = typeof data.features_list === 'string'
                        ? JSON.parse(data.features_list)
                        : [];

                    const featuresContainer = document.querySelector('#features-section .features-grid');
                    if (featuresContainer && features.length > 0) {
                        featuresContainer.innerHTML = features.map(f => `
                            <div class="feature-item" data-aos="fade-up">
                                <div class="feature-icon">
                                    <i class="${f.icon || 'fas fa-check-circle'}"></i>
                                </div>
                                <h3>${f.title}</h3>
                                <p>${f.description || ''}</p>
                            </div>
                        `).join('');
                    }
                }

                console.log('✅ Features loaded from API');
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Load Stats from API
     */
    async function loadStats() {
        try {
            const result = await safeFetch('/api/admin-full/section/stats');
            
            if (result && result.data) {
                const data = result.data || {};

                // Update stats
                updateStat('customers_count', data.customers_count);
                updateStat('services_count', data.services_count);
                updateStat('experience_count', data.experience_count);
                updateStat('technicians_count', data.technicians_count);

                // Update labels
                updateStatLabel('customers_label', data.customers_label);
                updateStatLabel('services_label', data.services_label);
                updateStatLabel('experience_label', data.experience_label);
                updateStatLabel('technicians_label', data.technicians_label);

                console.log('✅ Stats loaded from API');
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Update stat number
     */
    function updateStat(elementId, value) {
        const element = document.querySelector(`[data-target*="${elementId.replace('_count', '')}"]`);
        if (element && value) {
            const number = value.replace(/[^0-9]/g, '');
            if (number) element.setAttribute('data-target', number);
        }
    }

    /**
     * Update stat label
     */
    function updateStatLabel(elementId, value) {
        // Stats labels are usually in the HTML, can be updated if needed
    }

    /**
     * Load Contact Info from API
     */
    async function loadContactInfo() {
        try {
            const result = await safeFetch('/api/admin-full/section/contact');
            
            if (result && result.data) {
                const data = result.data || {};

                // Update phone
                const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
                if (phoneLinks.length > 0 && data.phone) {
                    phoneLinks.forEach(link => {
                        link.href = `tel:${data.phone}`;
                        link.textContent = data.phone;
                    });
                }

                // Update email
                const emailLinks = document.querySelectorAll('a[href^="mailto:"]');
                if (emailLinks.length > 0 && data.email) {
                    emailLinks.forEach(link => {
                        link.href = `mailto:${data.email}`;
                        link.textContent = data.email;
                    });
                }

                // Update address
                const addressEl = document.querySelector('.contact-item .contact-details span');
                if (addressEl && data.address) {
                    addressEl.textContent = data.address;
                }

                console.log('✅ Contact info loaded from API');
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Load all content
     */
    async function loadAllContent() {
        console.log('🔄 Loading dynamic content from API...');

        // Load all sections in parallel with timeout
        try {
            await Promise.all([
                loadHeroSection(),
                loadServices(),
                loadProducts(),
                loadTestimonials(),
                loadFeatures(),
                loadStats(),
                loadContactInfo()
            ]);
            console.log('✅ All dynamic content loaded!');
        } catch (error) {
            console.log('⚠️ Some content failed to load from API, using defaults');
        }
    }

    // Public API
    return {
        loadAllContent,
        loadHeroSection,
        loadServices,
        loadProducts,
        loadTestimonials,
        loadFeatures,
        loadStats,
        loadContactInfo
    };
})();

// Auto-load content when DOM is ready with proper timing
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        // Wait for sections to load first, then dynamic content
        setTimeout(() => {
            DynamicContent.loadAllContent();
        }, 800);
    });
} else {
    setTimeout(() => {
        DynamicContent.loadAllContent();
    }, 800);
}
