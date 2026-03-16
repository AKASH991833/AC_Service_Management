/**
 * Interactions Module
 * Scroll, navbar, stats, and user interactions
 */

const Interactions = (function() {
    'use strict';

    /**
     * Smooth scroll for navigation links
     */
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;

                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    const offsetTop = target.offsetTop - 80;

                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });

                    // Close mobile menu if open
                    const navbarCollapse = document.querySelector('.navbar-collapse');
                    if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                        const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse) ||
                                          new bootstrap.Collapse(navbarCollapse);
                        bsCollapse.hide();
                    }
                }
            });
        });

        console.log('Interactions: Smooth scroll initialized');
    }

    /**
     * Navbar background change on scroll
     */
    function initNavbarScroll() {
        const navbar = document.querySelector('.navbar-custom');
        if (!navbar) return;

        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    if (window.scrollY > 50) {
                        navbar.classList.add('scrolled');
                        document.body.style.paddingTop = navbar.offsetHeight + 'px';
                    } else {
                        navbar.classList.remove('scrolled');
                        document.body.style.paddingTop = '0';
                    }
                    ticking = false;
                });
                ticking = true;
            }
        });

        console.log('Interactions: Navbar scroll initialized');
    }

    /**
     * Animated stats counter
     */
    function initStatsCounter() {
        const stats = document.querySelectorAll('.stat-number');
        if (!stats.length) {
            console.log('Interactions: No stats found');
            return;
        }

        const animateCount = (element) => {
            const target = parseFloat(element.getAttribute('data-target'));
            const duration = 2000;
            const increment = target / (duration / 16);
            let current = 0;
            
            // Get prefix/suffix if any
            const prefix = element.getAttribute('data-prefix') || '';
            const suffix = element.getAttribute('data-suffix') || '';

            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    element.textContent = prefix + target.toLocaleString() + suffix;
                    clearInterval(timer);
                } else {
                    if (target < 10) {
                        element.textContent = prefix + current.toFixed(1) + suffix;
                    } else {
                        element.textContent = prefix + Math.floor(current).toLocaleString() + suffix;
                    }
                }
            }, 16);
        };

        // Use Intersection Observer to start animation when visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    animateCount(entry.target);
                    entry.target.classList.add('counted');
                }
            });
        }, { threshold: 0.5 });

        stats.forEach(stat => observer.observe(stat));

        console.log('Interactions: Stats counter initialized (' + stats.length + ' stats)');
    }

    /**
     * Scroll to top button
     */
    function initScrollToTop() {
        const scrollBtn = document.createElement('div');
        scrollBtn.className = 'scroll-to-top';
        scrollBtn.innerHTML = '<i class="fas fa-chevron-up"></i>';
        scrollBtn.setAttribute('aria-label', 'Scroll to top');
        document.body.appendChild(scrollBtn);

        let ticking = false;

        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    if (window.scrollY > 500) {
                        scrollBtn.classList.add('visible');
                    } else {
                        scrollBtn.classList.remove('visible');
                    }
                    ticking = false;
                });
                ticking = true;
            }
        });

        scrollBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        console.log('Interactions: Scroll to top initialized');
    }

    /**
     * Expandable services functionality
     */
    function initExpandableServices() {
        const viewMoreBtn = document.getElementById('view-more-services');
        if (!viewMoreBtn) return;

        viewMoreBtn.addEventListener('click', function() {
            const hiddenServices = document.querySelectorAll('#services-container .hidden-service');
            const isExpanded = this.classList.contains('expanded');

            hiddenServices.forEach(service => {
                service.style.display = isExpanded ? 'none' : 'block';
                // Trigger AOS refresh
                if (typeof AOS !== 'undefined') {
                    AOS.refresh();
                }
            });

            this.classList.toggle('expanded');
            this.innerHTML = isExpanded ?
                '<i class="fas fa-plus me-2"></i>View All Services' :
                '<i class="fas fa-minus me-2"></i>Show Less';

            console.log('Interactions: Services expanded:', !isExpanded);
        });

        console.log('Interactions: Expandable services initialized');
    }

    /**
     * Expandable products functionality
     */
    function initExpandableProducts() {
        const viewMoreBtn = document.getElementById('view-more-products');
        if (!viewMoreBtn) return;

        viewMoreBtn.addEventListener('click', function() {
            const hiddenProducts = document.querySelectorAll('#products-container .hidden-product');
            const isExpanded = this.classList.contains('expanded');

            hiddenProducts.forEach(product => {
                product.style.display = isExpanded ? 'none' : 'block';
            });

            this.classList.toggle('expanded');
            this.innerHTML = isExpanded ?
                '<i class="fas fa-plus me-2"></i>View All Products' :
                '<i class="fas fa-minus me-2"></i>Show Less';
        });

        console.log('Interactions: Expandable products initialized');
    }

    /**
     * Scroll animations trigger
     */
    function initScrollAnimations() {
        const animatedElements = document.querySelectorAll('[data-scroll-animate]');
        if (!animatedElements.length) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, { threshold: 0.1, rootMargin: '50px' });

        animatedElements.forEach(el => observer.observe(el));

        console.log('Interactions: Scroll animations initialized');
    }

    /**
     * Active navigation link highlighter
     */
    function initActiveNavHighlight() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

        if (!sections.length || !navLinks.length) return;

        window.addEventListener('scroll', () => {
            let current = '';
            const scrollPos = window.scrollY + 100;

            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.offsetHeight;

                if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        });

        console.log('Interactions: Active nav highlight initialized');
    }

    // Public API
    return {
        initSmoothScroll,
        initNavbarScroll,
        initStatsCounter,
        initScrollToTop,
        initExpandableServices,
        initExpandableProducts,
        initScrollAnimations,
        initActiveNavHighlight
    };
})();
