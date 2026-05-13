/**
 * Dynamic Content Loader
 * Loads website content from backend API
 * Makes all sections dynamic and editable from admin
 *
 * SECURITY: Uses session-based authentication for admin content
 * Public content does not require authentication
 */

const DynamicContent = (function() {
    'use strict';

    /**
     * Escape HTML to prevent XSS
     */
    function escapeHtml(str) {
        if (typeof str !== 'string') return str;
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    /**
     * Resolve service image with sensible local fallbacks when DB image is missing
     */
    function resolveServiceImage(service) {
        if (service && service.service_image) {
            return service.service_image;
        }

        const slug = String(service?.service_slug || '').toLowerCase();
        const name = String(service?.service_name || '').toLowerCase();

        const fallbackMap = {
            'ac-installation': 'assets/images/ac-installation.jpg',
            'installation': 'assets/images/ac-installation.jpg',
            'ac-repair': 'assets/images/ac-repair.jpg',
            'repair': 'assets/images/ac-repair.jpg',
            'gas-refilling': 'assets/images/gas-refill.jpg',
            'gas-refill': 'assets/images/gas-refill.jpg',
            'gas': 'assets/images/gas-refill.jpg',
            'amc-service': 'assets/images/amc-service.jpg',
            'amc': 'assets/images/amc-service.jpg',
            'pcb-repair': 'assets/images/pcb-repair.jpg',
            'cleaning': 'assets/images/ac-cleaning.jpg',
            'deep-cleaning': 'assets/images/ac-cleaning.jpg'
        };

        for (const [key, path] of Object.entries(fallbackMap)) {
            if (slug.includes(key) || name.includes(key.replace(/-/g, ' '))) {
                return path;
            }
        }

        return 'assets/images/ac-repair.jpg';
    }

    // API Configuration - with proper fallbacks
    const API_BASE = (typeof API_CONFIG !== 'undefined' && API_CONFIG.BASE_URL) ||
                     (typeof FRONTEND_SETTINGS !== 'undefined' && FRONTEND_SETTINGS.API_BASE_URL) ||
                     'http://localhost:5000';
    
    // NO API_KEY - using session-based authentication

    /**
     * Safe API fetch with error handling
     * SECURITY: Session-based auth via cookies
     */
    async function safeFetch(endpoint) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json'
                    // NO API_KEY - using session-based authentication
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
                // API endpoint unavailable, using default content
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

            if (result && result.success && result.data) {
                const data = result.data || {};

                // Update Hero Section
                const heroTitle = document.querySelector('#hero-section .hero-title');
                const heroSubtitle = document.querySelector('#hero-section .hero-description');
                const primaryCta = document.querySelector('#hero-section .hero-cta a.btn-primary-glow');
                const phoneCta = document.querySelector('#hero-section .hero-cta a.btn-outline-glow');
                const whatsappCta = document.querySelector('#hero-section .hero-cta a.btn-whatsapp-hero');
                const backgroundImages = document.querySelectorAll('#hero-section .hero-main-bg, #hero-section .featured-img');

                if (heroTitle && data.title) {
                    heroTitle.textContent = data.title;
                }
                if (heroSubtitle && data.subtitle) {
                    heroSubtitle.textContent = data.subtitle;
                }
                if (primaryCta && data.cta_text) {
                    primaryCta.innerHTML = `<i class="fas fa-calendar-check me-2"></i>${escapeHtml(data.cta_text)}`;
                }
                if (phoneCta && data.cta_phone) {
                    phoneCta.href = `tel:${data.cta_phone}`;
                    phoneCta.innerHTML = `<i class="fas fa-phone-alt me-2"></i>${escapeHtml(data.cta_phone)}`;
                }
                if (whatsappCta && data.cta_phone) {
                    const whatsappNumber = String(data.cta_phone).replace(/[^\d]/g, '');
                    if (whatsappNumber) {
                        whatsappCta.href = `https://wa.me/${whatsappNumber}`;
                    }
                }
                if (data.background_image) {
                    backgroundImages.forEach(image => {
                        image.src = data.background_image;
                    });
                }

                // Hero section loaded from API
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

            if (result && result.success && result.data && result.data.length > 0) {
                let services = (result.data || []).filter(service =>
                    service && service.is_active !== false && !service.is_deleted
                );
                services.sort((a, b) => (a.display_order || 0) - (b.display_order || 0));

                const servicesContainer = document.querySelector('#services-container');
                if (servicesContainer) {
                    const maxMain = 3;
                    const cardsHtml = services.map((service, index) => {
                        const features = typeof service.features === 'string'
                            ? JSON.parse(service.features)
                            : (service.features || []);
                        const serviceImage = resolveServiceImage(service);
                        const isHidden = index >= maxMain;

                    return `
                        <div class="col-lg-4 col-md-6 service-item ${isHidden ? 'hidden-service' : 'main-service'}" ${isHidden ? 'style="display: none;"' : ''}>
                            <div class="glass-card service-card">
                                ${serviceImage ? `
                                <div class="service-image-wrapper">
                                    <img src="${escapeHtml(serviceImage)}" alt="${escapeHtml(service.service_name) || 'Service'}" class="img-fluid lazy" loading="lazy">
                                </div>
                                ` : `
                                <div class="icon-container">
                                    <i class="${escapeHtml(service.icon_class) || 'fas fa-tools'}"></i>
                                </div>
                                `}
                                <div class="service-content">
                                    <h3>${escapeHtml(service.service_name) || 'Service'}</h3>
                                    <p class="service-duration">${escapeHtml(service.duration) || ''}</p>
                                    <p class="service-short-desc">${escapeHtml(service.description) || ''}</p>
                                    <p class="service-price">
                                        <span class="price-label">From</span>
                                        <span class="price-amount">${escapeHtml(service.starting_price) || '₹0'}</span>
                                    </p>
                                    <ul class="service-features-list">
                                        ${features.map(f => `<li><i class="fas fa-check-circle"></i> ${escapeHtml(f)}</li>`).join('')}
                                    </ul>
                                    <button class="service-btn btn btn-primary-glow" data-service="${escapeHtml(service.service_slug) || ''}">
                                        Book Now <i class="fas fa-arrow-right"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                    }).join('');
                    servicesContainer.innerHTML = cardsHtml;
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

            if (result && result.success && result.data && result.data.length > 0) {
                const products = (result.data || []).filter(product =>
                    product && product.is_active !== false && product.is_available !== false
                );

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

                    // Products loaded from API
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
                    ${product.badge_text ? `<div class="product-badge">${escapeHtml(product.badge_text)}</div>` : ''}
                    <div class="product-image">
                        <img src="${escapeHtml(product.product_image) || 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?w=500'}"
                             alt="${escapeHtml(product.product_name) || 'Product'}" class="lazy">
                    </div>
                    <div class="product-details">
                        <h3 class="product-name">${escapeHtml(product.product_name) || 'Product'}</h3>
                        <div class="product-specs">
                            <span><i class="fas fa-snowflake"></i> ${escapeHtml(product.capacity) || '1.5 Ton'}</span>
                            <span><i class="fas fa-star"></i> ${product.star_rating || '5'} Star</span>
                            <span><i class="fas fa-wind"></i> ${escapeHtml(product.ac_type) || 'Split'}</span>
                        </div>
                        <ul class="product-features">
                            ${features.slice(0, 3).map(f => `<li><i class="fas fa-check"></i> ${escapeHtml(f)}</li>`).join('')}
                        </ul>
                        <div class="product-footer">
                            <div class="product-price">${escapeHtml(product.price) || '₹0'}</div>
                            <button class="product-btn ${product.product_type === 'buy' ? 'buy' : 'rent'}-btn"
                                    data-product="${escapeHtml(product.product_name) || ''}"
                                    data-type="${escapeHtml(product.product_type) || 'buy'}">
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

            if (result && result.success && result.data && result.data.length > 0) {
                const testimonials = (result.data || []).filter(testimonial =>
                    testimonial && testimonial.is_active !== false
                );

                if (testimonials.length > 0) {
                    const testimonialsContainer = document.querySelector('#testimonials-section .testimonials-grid');
                    if (testimonialsContainer) {
                        testimonialsContainer.innerHTML = testimonials.map(t => `
                            <div class="testimonial-card glass-card" data-aos="fade-up">
                                <div class="testimonial-rating">${'⭐'.repeat(t.rating || 5)}</div>
                                <p class="testimonial-text">"${escapeHtml(t.review_text) || ''}"</p>
                                <div class="testimonial-author">
                                    <div class="author-info">
                                        <h4>${escapeHtml(t.customer_name) || 'Customer'}</h4>
                                        <p>${escapeHtml(t.customer_location) || 'Happy Customer'}</p>
                                    </div>
                                </div>
                            </div>
                        `).join('');
                        // Testimonials loaded from API
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

            if (result && result.success && result.data) {
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
                                    <i class="${escapeHtml(f.icon) || 'fas fa-check-circle'}"></i>
                                </div>
                                <h3>${escapeHtml(f.title) || ''}</h3>
                                <p>${escapeHtml(f.description) || ''}</p>
                            </div>
                        `).join('');
                    }
                }

                // Features loaded from API
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

            if (result && result.success && result.data) {
                const data = result.data || {};
                const statMappings = [
                    { value: data.customers_count, label: data.customers_label },
                    { value: data.services_count, label: data.services_label },
                    { value: data.experience_count, label: data.experience_label },
                    { value: data.technicians_count, label: data.technicians_label }
                ];
                const statItems = document.querySelectorAll('#stats-section .stat-item');

                statItems.forEach((item, index) => {
                    const stat = statMappings[index];
                    if (!stat) return;

                    const numberEl = item.querySelector('.stat-number');
                    const labelEl = item.querySelector('.stat-label');

                    if (numberEl && stat.value) {
                        numberEl.textContent = stat.value;
                        const numericTarget = String(stat.value).replace(/[^0-9.]/g, '');
                        if (numericTarget) {
                            numberEl.setAttribute('data-target', numericTarget);
                        }
                    }

                    if (labelEl && stat.label) {
                        labelEl.textContent = stat.label;
                    }
                });

                // Stats loaded from API
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Load Contact Info from API
     */
    async function loadContactInfo() {
        try {
            const result = await safeFetch('/api/admin-full/section/contact');

            if (result && result.success && result.data) {
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

                // Update business hours
                const hoursItems = document.querySelectorAll('#contact-section .hours-item');
                if (hoursItems.length >= 2 && data.business_hours) {
                    const parts = String(data.business_hours).split('|').map(part => part.trim());
                    parts.forEach((part, index) => {
                        const timeEl = hoursItems[index]?.querySelector('.hours-time');
                        if (timeEl) {
                            timeEl.textContent = part;
                        }
                    });
                }

                // Update map
                const mapFrame = document.querySelector('#contact-section .map-container iframe');
                if (mapFrame && data.google_maps_embed) {
                    mapFrame.src = data.google_maps_embed;
                }

                // Contact info loaded from API
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Load JustDial section from API
     */
    async function loadJustdialSection() {
        try {
            const result = await safeFetch('/api/admin-full/section/justdial');

            if (result && result.success && result.data) {
                const data = result.data || {};
                const section = document.querySelector('#justdial-section #justdial');
                const statValues = document.querySelectorAll('#justdial-section .jd-stat-value');
                const verifiedBadges = document.querySelectorAll('#justdial-section .jd-verified');
                const badgeImage = document.querySelector('#justdial-section img');

                if (section) {
                    section.style.display = data.show_badge === 'false' ? 'none' : '';
                }
                if (statValues[0] && data.rating) {
                    statValues[0].innerHTML = `${escapeHtml(data.rating)}<small>/5</small>`;
                }
                if (statValues[1] && data.review_count) {
                    statValues[1].innerHTML = escapeHtml(data.review_count);
                }
                if (verifiedBadges.length > 0 && data.verified_text) {
                    verifiedBadges.forEach(badge => {
                        badge.innerHTML = `<i class="fas fa-check-circle"></i> ${escapeHtml(data.verified_text)}`;
                    });
                }
                if (badgeImage && data.badge_image) {
                    badgeImage.src = data.badge_image;
                }
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Load Footer section from API
     */
    async function loadFooterSection() {
        try {
            const result = await safeFetch('/api/admin-full/section/footer');

            if (result && result.success && result.data) {
                const data = result.data || {};
                const companyHeading = document.querySelector('#footer-section .footer-section h3');
                const companyDescription = document.querySelector('#footer-section .footer-section .description');
                const socialLinks = document.querySelectorAll('#footer-section .social-icons a');
                const quickLinksContainer = document.querySelector('#footer-section .footer-links');
                const copyrightText = document.querySelector('#footer-section .footer-copyright p');

                if (companyHeading && data.company_name) {
                    companyHeading.innerHTML = `<i class="fas fa-snowflake me-2"></i>${escapeHtml(data.company_name)}`;
                }
                if (companyDescription && data.tagline) {
                    companyDescription.textContent = data.tagline;
                }

                const socialValues = [
                    data.social_facebook,
                    data.social_instagram,
                    data.social_twitter,
                    data.social_youtube
                ];
                socialLinks.forEach((link, index) => {
                    if (socialValues[index]) {
                        link.href = socialValues[index];
                    }
                });

                if (quickLinksContainer && data.quick_links) {
                    try {
                        const links = typeof data.quick_links === 'string'
                            ? JSON.parse(data.quick_links)
                            : data.quick_links;
                        if (Array.isArray(links) && links.length > 0) {
                            quickLinksContainer.innerHTML = links.map(link =>
                                `<a href="${escapeHtml(link.url || '#')}">${escapeHtml(link.label || 'Link')}</a>`
                            ).join('');
                        }
                    } catch (error) {
                        // Ignore malformed quick links payload.
                    }
                }

                if (copyrightText && data.copyright_text) {
                    copyrightText.textContent = data.copyright_text;
                }
            }
        } catch (error) {
            // Silent fail - default content remains
        }
    }

    /**
     * Load all content
     */
    async function loadAllContent() {
        // Loading dynamic content from API

        // Load all sections in parallel with timeout
        try {
            await Promise.all([
                loadHeroSection(),
                loadServices(),
                loadProducts(),
                loadTestimonials(),
                loadFeatures(),
                loadStats(),
                loadContactInfo(),
                loadJustdialSection(),
                loadFooterSection()
            ]);
            // All dynamic content loaded
        } catch (error) {
            // Some content failed to load from API, using defaults
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
        loadContactInfo,
        loadJustdialSection,
        loadFooterSection
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
