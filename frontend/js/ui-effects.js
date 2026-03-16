/**
 * UI Effects Module
 * Cursor trail, particles, and visual effects
 */

const UIEffects = (function() {
    'use strict';

    /**
     * Initialize cursor trail effect
     */
    function initCursorTrail() {
        const trail = document.getElementById('cursor-trail');
        if (!trail) return;

        // Respect reduced motion preference
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            trail.style.display = 'none';
            return;
        }

        // Don't initialize on mobile or touch devices
        if (window.innerWidth < 768 || 'ontouchstart' in window) {
            trail.style.display = 'none';
            return;
        }

        const particles = [];
        const particleCount = 12; // Reduced from 20 for better performance

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'cursor-particle';
            particle.style.cssText = `
                position: fixed;
                width: ${10 - i * 0.4}px;
                height: ${10 - i * 0.4}px;
                background: linear-gradient(135deg, rgba(255, 129, 255, 0.6), rgba(0, 245, 255, 0.6));
                border-radius: 50%;
                pointer-events: none;
                z-index: 9999;
                transition: transform 0.1s ease;
                box-shadow: 0 0 10px rgba(255, 129, 255, 0.5);
            `;
            trail.appendChild(particle);
            particles.push({
                element: particle,
                x: 0,
                y: 0
            });
        }

        let mouseX = 0, mouseY = 0;
        let currentX = 0, currentY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        });

        function animate() {
            currentX += (mouseX - currentX) * 0.3;
            currentY += (mouseY - currentY) * 0.3;

            particles.forEach((particle, index) => {
                const targetX = currentX - (currentX - mouseX) * (index / particleCount);
                const targetY = currentY - (currentY - mouseY) * (index / particleCount);

                particle.x += (targetX - particle.x) * 0.3;
                particle.y += (targetY - particle.y) * 0.3;

                particle.element.style.left = particle.x + 'px';
                particle.element.style.top = particle.y + 'px';
            });

            requestAnimationFrame(animate);
        }

        animate();
        console.log('UIEffects: Cursor trail initialized (reduced motion optimized)');
    }

    /**
     * Initialize floating particles
     */
    function initParticles() {
        const container = document.getElementById('particles-container');
        if (!container) return;

        // Respect reduced motion preference
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            container.style.display = 'none';
            return;
        }

        // Don't initialize on mobile or touch devices for better performance
        if (window.innerWidth < 768 || 'ontouchstart' in window) {
            container.style.display = 'none';
            return;
        }

        const particleCount = 15; // Reduced from 30 for better performance

        for (let i = 0; i < particleCount; i++) {
            createParticle(container);
        }

        console.log('UIEffects: Particles initialized (reduced motion optimized)');
    }

    /**
     * Create a single particle
     */
    function createParticle(container) {
        const particle = document.createElement('div');
        particle.className = 'particle';

        const size = Math.random() * 5 + 2;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.top = Math.random() * 100 + 'vh';
        particle.style.opacity = Math.random() * 0.5 + 0.2;

        const duration = Math.random() * 20 + 10;
        particle.style.animation = `float ${duration}s ease-in-out infinite`;
        particle.style.animationDelay = Math.random() * 5 + 's';

        container.appendChild(particle);

        // Remove and recreate particle after animation
        setTimeout(() => {
            particle.remove();
            createParticle(container);
        }, duration * 1000);
    }

    /**
     * Initialize loading screen
     */
    function initLoadingScreen() {
        const loadingScreen = document.getElementById('loading-screen');
        if (!loadingScreen) return;

        // Ensure loading screen is visible initially
        loadingScreen.classList.remove('hidden');

        console.log('UIEffects: Loading screen initialized');
    }

    /**
     * Parallax scroll effect
     */
    function initParallax() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        if (!parallaxElements.length) return;

        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;

            parallaxElements.forEach(element => {
                const speed = element.dataset.parallax || 0.5;
                const yPos = -(scrolled * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        });

        console.log('UIEffects: Parallax initialized');
    }

    /**
     * Button ripple effect
     */
    function initButtonRipple() {
        const buttons = document.querySelectorAll('.btn-primary-glow, .btn-outline-glow');

        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const rect = button.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                ripple.style.cssText = `
                    position: absolute;
                    left: ${x}px;
                    top: ${y}px;
                    width: 0;
                    height: 0;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.5);
                    transform: translate(-50%, -50%);
                    animation: ripple 0.6s ease-out;
                    pointer-events: none;
                `;

                button.style.position = 'relative';
                button.style.overflow = 'hidden';
                button.appendChild(ripple);

                setTimeout(() => ripple.remove(), 600);
            });
        });

        console.log('UIEffects: Button ripple initialized');
    }

    /**
     * Typing animation for text elements
     */
    function initTypingAnimation() {
        const typingElements = document.querySelectorAll('[data-typing]');
        if (!typingElements.length) return;

        typingElements.forEach(element => {
            const text = element.textContent;
            element.textContent = '';
            element.style.borderRight = '2px solid var(--cyan-glow)';

            let i = 0;
            function type() {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(type, 50);
                } else {
                    element.style.borderRight = 'none';
                }
            }

            // Start typing when element is in view
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        type();
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.5 });

            observer.observe(element);
        });

        console.log('UIEffects: Typing animation initialized');
    }

    /**
     * Destroy all effects (for cleanup)
     */
    function destroy() {
        const trail = document.getElementById('cursor-trail');
        const particles = document.getElementById('particles-container');
        if (trail) trail.innerHTML = '';
        if (particles) particles.innerHTML = '';
        console.log('UIEffects: Destroyed');
    }

    // Public API
    return {
        initCursorTrail,
        initParticles,
        initLoadingScreen,
        initParallax,
        initButtonRipple,
        initTypingAnimation,
        destroy
    };
})();

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        UIEffects.initLoadingScreen();
        UIEffects.initCursorTrail();
        UIEffects.initParticles();
    });
} else {
    UIEffects.initLoadingScreen();
    UIEffects.initCursorTrail();
    UIEffects.initParticles();
}
