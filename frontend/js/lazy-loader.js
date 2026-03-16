/**
 * Lazy Loading Module
 * Efficient image lazy loading with Intersection Observer
 */

const LazyLoader = (function() {
    'use strict';

    let observer = null;
    let loadedCount = 0;

    /**
     * Check if element is in viewport
     */
    function isInViewport(element, threshold = 0) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top <= (window.innerHeight || document.documentElement.clientHeight) + threshold &&
            rect.bottom >= -threshold
        );
    }

    /**
     * Load a single image
     */
    function loadImage(img) {
        const src = img.getAttribute('data-src');
        const srcset = img.getAttribute('data-srcset');

        if (!src) return;

        // Create new image to preload
        const newImg = new Image();

        newImg.onload = function() {
            if (srcset) {
                img.srcset = srcset;
            }
            img.src = src;
            img.classList.add('loaded', 'lazy-loaded');
            img.removeAttribute('data-src');
            if (srcset) img.removeAttribute('data-srcset');
            loadedCount++;
        };

        newImg.onerror = function() {
            // Don't show error in console for failed images
            // Just load them anyway (browser will handle)
            img.src = src;
            img.classList.add('loaded');
            img.removeAttribute('data-src');
            loadedCount++;
        };

        // Start loading
        newImg.src = src;
        if (srcset) newImg.srcset = srcset;
    }

    /**
     * Intersection Observer callback
     */
    function handleIntersection(entries, obs) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                loadImage(img);
                obs.unobserve(img);
            }
        });
    }

    /**
     * Initialize lazy loading with Intersection Observer
     */
    function init() {
        // Check for Intersection Observer support
        if ('IntersectionObserver' in window) {
            observer = new IntersectionObserver(handleIntersection, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            // Observe all images with data-src
            document.querySelectorAll('img[data-src]').forEach(img => {
                observer.observe(img);
            });

            console.log('LazyLoader: Initialized with Intersection Observer');
        } else {
            // Fallback for older browsers
            console.log('LazyLoader: Using fallback (no Intersection Observer)');
            loadAllImages();
        }
    }

    /**
     * Fallback: Load all images immediately
     */
    function loadAllImages() {
        document.querySelectorAll('img[data-src]').forEach(img => {
            loadImage(img);
        });
    }

    /**
     * Load images in a specific container
     */
    function loadContainer(container) {
        if (!container) return;

        const images = container.querySelectorAll('img[data-src]');
        images.forEach(img => loadImage(img));
    }

    /**
     * Refresh lazy loader (after dynamic content)
     */
    function refresh() {
        if (observer) {
            observer.disconnect();
            document.querySelectorAll('img[data-src]').forEach(img => {
                observer.observe(img);
            });
        } else {
            loadAllImages();
        }
    }

    /**
     * Get statistics
     */
    function getStats() {
        const total = document.querySelectorAll('img[data-src]').length;
        return {
            total: total,
            loaded: loadedCount,
            pending: total - loadedCount
        };
    }

    /**
     * Destroy observer
     */
    function destroy() {
        if (observer) {
            observer.disconnect();
            observer = null;
        }
    }

    // Public API
    return {
        init,
        refresh,
        loadContainer,
        loadAllImages,
        getStats,
        destroy
    };
})();

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', LazyLoader.init);
} else {
    LazyLoader.init();
}
