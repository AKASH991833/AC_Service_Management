/**
 * Sections Loader Module
 * Dynamic HTML section loading with caching
 */

const SectionsLoader = (function() {
    'use strict';

    // Cache for loaded sections
    const cache = new Map();

    /**
     * Load a single section
     */
    async function loadSection(containerId, filePath) {
        // Check cache first
        if (cache.has(filePath)) {
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = cache.get(filePath);
                console.log(`SectionsLoader: Loaded "${filePath}" from cache`);
            }
            return;
        }

        try {
            // Add cache-busting to force fresh load
            const bustKey = '?v=20260328';
            const response = await fetch(filePath + bustKey);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const html = await response.text();

            // Cache the content
            cache.set(filePath, html);

            // Insert into container
            const container = document.getElementById(containerId);
            if (container) {
                container.innerHTML = html;
            }

            console.log(`SectionsLoader: Loaded "${filePath}"`);
        } catch (error) {
            console.error(`SectionsLoader: Error loading ${filePath}:`, error);
            const container = document.getElementById(containerId);
            if (container) {
                // Show fallback content instead of just error message
                const sectionName = filePath.replace('sections/', '').replace('.html', '');
                container.innerHTML = `
                    <div class="section-load-error" style="
                        text-align: center; 
                        padding: 40px; 
                        background: rgba(255,255,255,0.05); 
                        border-radius: 10px;
                        margin: 20px 0;
                    ">
                        <i class="fas fa-exclamation-triangle" style="
                            font-size: 3rem; 
                            color: #ff4757; 
                            margin-bottom: 15px;
                        "></i>
                        <h3 style="color: #fff; margin-bottom: 10px;">Content Loading...</h3>
                        <p style="color: rgba(255,255,255,0.7);">
                            ${sectionName.charAt(0).toUpperCase() + sectionName.slice(1)} section is being prepared.
                        </p>
                        <p style="color: rgba(255,255,255,0.5); font-size: 0.9rem; margin-top: 10px;">
                            Please refresh the page if this message persists.
                        </p>
                    </div>
                `;
            }
        }
    }

    /**
     * Load multiple sections in parallel
     */
    async function loadSections(sections) {
        const promises = sections.map(section =>
            loadSection(section.containerId, section.filePath)
        );
        await Promise.all(promises);
        console.log('SectionsLoader: All sections loaded');
    }

    /**
     * Preload sections (cache them)
     */
    async function preloadSections(sectionPaths) {
        const promises = sectionPaths.map(path => fetch(path)
            .then(response => response.text())
            .then(html => {
                cache.set(path, html);
                console.log(`SectionsLoader: Preloaded "${path}"`);
            })
            .catch(error => console.error(`SectionsLoader: Failed to preload "${path}":`, error))
        );
        await Promise.all(promises);
    }

    /**
     * Clear cache for a specific section
     */
    function clearCache(filePath) {
        if (filePath) {
            cache.delete(filePath);
        } else {
            cache.clear();
        }
        console.log('SectionsLoader: Cache cleared');
    }

    /**
     * Get cache statistics
     */
    function getCacheStats() {
        return {
            size: cache.size,
            keys: Array.from(cache.keys())
        };
    }

    /**
     * Refresh a loaded section
     */
    async function refreshSection(containerId, filePath) {
        // Clear from cache
        cache.delete(filePath);
        // Reload
        await loadSection(containerId, filePath);
        console.log(`SectionsLoader: Refreshed "${filePath}"`);
    }

    // Public API
    return {
        loadSection,
        loadSections,
        preloadSections,
        clearCache,
        getCacheStats,
        refreshSection
    };
})();
