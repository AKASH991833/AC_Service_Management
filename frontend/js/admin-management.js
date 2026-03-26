/**
 * ANSH AIR COOL - ADMIN MANAGEMENT
 * Consolidated admin panel functionality with proper API configuration
 * 
 * This file combines:
 * - Authentication & Session Management
 * - Dashboard Stats
 * - Messages Management
 * - Service Requests Management
 * - Testimonials CRUD
 * - Services CRUD
 * - Products CRUD
 * - Content Management
 * - Gallery Management
 */

// ========================================
// API CONFIGURATION - Session-Based Auth
// ========================================
// SECURITY: Using session-based authentication (cookies)
// NO hardcoded API keys in frontend code
// ========================================
const ADMIN_API = {
    // Direct fallback to prevent undefined errors
    BASE_URL: (typeof API_CONFIG !== 'undefined' && API_CONFIG.BASE_URL) ||
              (typeof FRONTEND_SETTINGS !== 'undefined' && FRONTEND_SETTINGS.API_BASE_URL) ||
              'http://localhost:5000',

    // NO API_KEY - using session-based authentication
    // Admin authentication is handled via secure session cookies

    ENDPOINTS: {
        // Auth
        LOGIN: '/api/admin/login',
        LOGOUT: '/api/admin/logout',
        ME: '/api/admin/me',
        STATS: '/api/admin/stats',

        // Messages
        MESSAGES: '/api/admin/messages',
        MESSAGE_STATUS: '/api/admin/messages',

        // Service Requests
        REQUESTS: '/api/admin/requests',
        REQUEST_STATUS: '/api/admin/requests',

        // Content Sections - Using admin-full prefix
        HERO: '/api/admin-full/section/hero',
        SERVICES: '/api/admin-full/section/services',
        PRODUCTS: '/api/admin-full/section/products',
        TESTIMONIALS: '/api/admin-full/section/testimonials',
        FEATURES: '/api/admin-full/section/features',
        STATS: '/api/admin-full/section/stats',
        CONTACT: '/api/admin-full/section/contact',
        FOOTER: '/api/admin-full/section/footer',
        JUSTDIAL: '/api/admin-full/section/justdial',

        // Gallery
        GALLERY: '/api/admin-full/gallery',

        // Settings
        SETTINGS: '/api/admin-full/settings'
    }
};

// Debug mode
const ADMIN_DEBUG = true;

function adminDebugLog(...args) {
    if (ADMIN_DEBUG) {
        console.log('[ADMIN]', ...args);
    }
}

// State
let currentAdmin = null;
let allMessages = [];
let allRequests = [];

// ========================================
// UTILITY FUNCTIONS
// ========================================

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Truncate text
 */
function truncateText(text, length) {
    if (!text) return '';
    return text.length > length ? text.substring(0, length) + '...' : text;
}

/**
 * Format date
 */
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Show toast notification
 */
function showAdminToast(message, type = 'success') {
    // Remove existing toast
    const existingToast = document.querySelector('.admin-toast');
    if (existingToast) {
        existingToast.remove();
    }

    // Create toast element
    const toast = document.createElement('div');
    toast.className = `admin-toast admin-toast-${type}`;
    toast.innerHTML = `
        <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} me-2"></i>
        ${escapeHtml(message)}
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
        z-index: 99999;
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
 * Show loading state on button
 */
function setAdminButtonLoading(button, isLoading) {
    if (!button) return;
    
    if (isLoading) {
        button.disabled = true;
        button.dataset.originalHtml = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    } else {
        button.disabled = false;
        if (button.dataset.originalHtml) {
            button.innerHTML = button.dataset.originalHtml;
        }
    }
}

/**
 * Generic API request helper
 * SECURITY: Uses session-based authentication (cookies)
 * NO API_KEY required
 */
async function adminRequest(endpoint, options = {}) {
    const url = `${ADMIN_API.BASE_URL}${endpoint}`;

    adminDebugLog('📡 Request:', endpoint);
    adminDebugLog('📍 URL:', url);
    adminDebugLog('🔐 Auth: Session-based (cookies)');

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json'
            // NO API_KEY - using session-based authentication
        },
        credentials: 'include'  // Include cookies for session auth
    };

    const config = { ...defaultOptions, ...options };

    try {
        adminDebugLog('🚀 Fetching...');

        // First try with OPTIONS preflight for CORS
        if (options.method && options.method !== 'GET') {
            const optionsResponse = await fetch(url, {
                method: 'OPTIONS',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Request-Method': options.method
                }
            });

            if (!optionsResponse.ok) {
                adminDebugLog('⚠️ OPTIONS preflight failed:', optionsResponse.status);
            }
        }

        const response = await fetch(url, config);

        adminDebugLog('📥 Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            adminDebugLog('❌ Error response:', errorText);

            let error;
            try {
                error = JSON.parse(errorText);
            } catch {
                error = { message: errorText || `HTTP ${response.status}` };
            }

            // Handle session expiration (401)
            if (response.status === 401) {
                // Clear any cached admin data
                currentAdmin = null;
                throw new Error(`401 Unauthorized - ${error.message || 'Session expired'}`);
            }

            throw new Error(error.message || `HTTP ${response.status}`);
        }

        const data = await response.json();
        adminDebugLog('✅ Success:', data);
        return data;
    } catch (error) {
        adminDebugLog('❌ API Error:', error.message);
        adminDebugLog('Full error:', error);
        throw error;
    }
}

// ========================================
// INITIALIZATION
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    adminDebugLog('Admin Dashboard Initializing...');

    // Hide loading screen
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.classList.add('hidden');
        }, 1000);
    }

    // Initialize animations (same as website)
    initAdminAnimations();

    // Check if already logged in
    checkAuth();

    // Setup event listeners
    setupEventListeners();
});

/**
 * Initialize admin panel animations
 */
function initAdminAnimations() {
    adminDebugLog('Initializing admin animations...');
    
    // Initialize cursor trail
    initAdminCursorTrail();
    
    // Initialize particles
    initAdminParticles();
}

/**
 * Admin cursor trail effect
 */
function initAdminCursorTrail() {
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
    const particleCount = 12;

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
        particles.push({ element: particle, x: 0, y: 0 });
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
    adminDebugLog('Admin cursor trail initialized');
}

/**
 * Admin particles effect
 */
function initAdminParticles() {
    const container = document.getElementById('particles-container');
    if (!container) return;

    // Respect reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        container.style.display = 'none';
        return;
    }

    // Don't initialize on mobile or touch devices
    if (window.innerWidth < 768 || 'ontouchstart' in window) {
        container.style.display = 'none';
        return;
    }

    const particleCount = 15;

    for (let i = 0; i < particleCount; i++) {
        createAdminParticle(container);
    }

    adminDebugLog('Admin particles initialized');
}

/**
 * Create admin particle
 */
function createAdminParticle(container) {
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
        createAdminParticle(container);
    }, duration * 1000);
}

// ========================================
// AUTHENTICATION
// ========================================

async function checkAuth() {
    try {
        adminDebugLog('Checking admin authentication...');
        const response = await adminRequest(ADMIN_API.ENDPOINTS.ME, { method: 'GET' });

        currentAdmin = response.data;
        adminDebugLog('Admin authenticated:', currentAdmin?.username);
        showDashboard();
    } catch (error) {
        adminDebugLog('Not authenticated or error:', error.message);
        
        // Only show toast if we're already on dashboard (not on login page)
        // Don't show "Session expired" on login page itself
        const loginPage = document.getElementById('login-page');
        if (loginPage && !loginPage.classList.contains('d-none')) {
            // We're on login page, just stay here (no toast)
        } else {
            // We're on dashboard, show session expired message
            if (error.message && error.message.includes('401')) {
                showAdminToast('Session expired. Please login again.', 'error');
            }
        }
        
        showLoginPage();
    }
}

function showLoginError(message) {
    const loginError = document.getElementById('loginError');
    if (loginError) {
        loginError.classList.remove('d-none');
        loginError.querySelector('span').textContent = message;
        loginError.style.display = 'block';
    }
}

function showLoginPage() {
    const loginPage = document.getElementById('login-page');
    const dashboardPage = document.getElementById('dashboard-page');
    
    if (loginPage) loginPage.classList.remove('d-none');
    if (dashboardPage) dashboardPage.classList.add('d-none');
}

function showDashboard() {
    const loginPage = document.getElementById('login-page');
    const dashboardPage = document.getElementById('dashboard-page');
    
    if (loginPage) loginPage.classList.add('d-none');
    if (dashboardPage) dashboardPage.classList.remove('d-none');

    // Load initial data
    loadDashboardStats();
    loadRecentMessages();
    loadRecentRequests();

    // Set admin name
    if (currentAdmin) {
        const adminNameEl = document.getElementById('adminName');
        if (adminNameEl) {
            adminNameEl.textContent = currentAdmin.full_name || currentAdmin.username;
        }
    }
}

// ========================================
// EVENT LISTENERS
// ========================================

function setupEventListeners() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }

    // Sidebar navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const section = this.dataset.section;
            navigateToSection(section);
        });
    });

    // Sidebar toggle (mobile)
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }

    // View all buttons
    document.querySelectorAll('.btn-view-all').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            navigateToSection(this.dataset.section);
        });
    });

    // Filter selects
    const messagesFilter = document.getElementById('messagesFilter');
    if (messagesFilter) {
        messagesFilter.addEventListener('change', () => loadMessages(messagesFilter.value));
    }

    const requestsFilter = document.getElementById('requestsFilter');
    if (requestsFilter) {
        requestsFilter.addEventListener('change', () => loadRequests(requestsFilter.value));
    }

    const productsFilter = document.getElementById('productsFilter');
    if (productsFilter) {
        productsFilter.addEventListener('change', () => loadProducts());
    }

    // Refresh buttons
    const refreshMessages = document.getElementById('refreshMessages');
    if (refreshMessages) {
        refreshMessages.addEventListener('click', () => {
            const filter = document.getElementById('messagesFilter')?.value || 'all';
            loadMessages(filter);
        });
    }

    const refreshRequests = document.getElementById('refreshRequests');
    if (refreshRequests) {
        refreshRequests.addEventListener('click', () => {
            const filter = document.getElementById('requestsFilter')?.value || 'all';
            loadRequests(filter);
        });
    }

    // Content form
    const contentForm = document.getElementById('contentForm');
    if (contentForm) {
        contentForm.addEventListener('submit', handleContentSubmit);
    }

    // Settings form
    const settingsForm = document.getElementById('settingsForm');
    if (settingsForm) {
        settingsForm.addEventListener('submit', handleSettingsSubmit);
    }

    // Upload form
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleImageUpload);
    }

    // Update status button
    const updateStatusBtn = document.getElementById('updateStatusBtn');
    if (updateStatusBtn) {
        updateStatusBtn.addEventListener('click', handleStatusUpdate);
    }
}

// ========================================
// LOGIN HANDLER
// ========================================

async function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const loginError = document.getElementById('loginError');
    const submitBtn = e.target.querySelector('button[type="submit"]');

    adminDebugLog('Login attempt for username:', username);

    // Sanitize input
    const sanitizedUsername = escapeHtml(username.trim());
    
    setAdminButtonLoading(submitBtn, true);

    try {
        const response = await fetch(`${ADMIN_API.BASE_URL}${ADMIN_API.ENDPOINTS.LOGIN}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                // NO API_KEY - using session-based authentication
            },
            credentials: 'include',
            body: JSON.stringify({ username: sanitizedUsername, password })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            currentAdmin = result.data.admin;
            if (loginError) {
                loginError.classList.add('d-none');
                loginError.style.display = 'none';
            }
            adminDebugLog('✅ Login successful');
            showDashboard();
            showAdminToast('Login successful!', 'success');
        } else {
            if (loginError) {
                loginError.classList.remove('d-none');
                loginError.querySelector('span').textContent = result.message || 'Invalid credentials';
                loginError.style.display = 'block';
            }
        }
    } catch (error) {
        adminDebugLog('Login error:', error.message);
        
        let errorMessage = 'Unable to connect to server';
        if (error.name === 'TypeError') {
            errorMessage = 'Cannot connect to backend server. Please ensure backend is running on port 5000.';
        }

        if (loginError) {
            loginError.classList.remove('d-none');
            loginError.querySelector('span').textContent = errorMessage;
            loginError.style.display = 'block';
        }
    } finally {
        setAdminButtonLoading(submitBtn, false);
    }
}

async function handleLogout() {
    try {
        await adminRequest(ADMIN_API.ENDPOINTS.LOGOUT, { method: 'POST' });
    } catch (error) {
        adminDebugLog('Logout error:', error);
    }

    currentAdmin = null;
    showLoginPage();
    showAdminToast('Logged out successfully', 'success');
}

// ========================================
// NAVIGATION
// ========================================

function navigateToSection(section) {
    // Update nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.section === section) {
            item.classList.add('active');
        }
    });

    // Update content sections
    document.querySelectorAll('.content-section').forEach(sec => {
        sec.classList.remove('active');
    });

    const targetSection = document.getElementById(`${section}-section`);
    if (targetSection) {
        targetSection.classList.add('active');
    }

    // Update page title
    const titles = {
        'dashboard': 'Dashboard',
        'messages': 'Messages',
        'service-requests': 'Service Requests',
        'testimonials': 'Testimonials Management',
        'services': 'Services Management',
        'products': 'Products Management',
        'content': 'Content Management',
        'gallery': 'Photo Gallery',
        'admin-profile': 'Admin Profile & Security',
        'settings': 'Settings',
        'hero': 'Hero Section',
        'features': 'Features',
        'stats': 'Statistics',
        'contact': 'Contact Info',
        'footer': 'Footer',
        'justdial': 'JustDial Badge'
    };

    const pageTitle = document.getElementById('pageTitle');
    if (pageTitle) {
        pageTitle.textContent = titles[section] || 'Dashboard';
    }

    // Load section-specific data
    switch(section) {
        case 'messages':
            loadMessages();
            break;
        case 'service-requests':
            loadRequests();
            break;
        case 'testimonials':
            loadTestimonials();
            break;
        case 'services':
            loadServices();
            break;
        case 'products':
            loadProducts();
            break;
        case 'content':
        case 'hero':
        case 'features':
        case 'stats':
        case 'contact':
        case 'footer':
        case 'justdial':
            loadContentSettings(section);
            break;
        case 'gallery':
            loadGallery();
            break;
        case 'admin-profile':
            loadAdminProfile();
            break;
        case 'settings':
            loadSettings();
            break;
    }

    // Close sidebar on mobile
    if (window.innerWidth <= 992) {
        document.querySelector('.sidebar')?.classList.remove('active');
    }
}

function toggleSidebar() {
    document.querySelector('.sidebar')?.classList.toggle('active');
}

// ========================================
// DASHBOARD STATS
// ========================================

async function loadDashboardStats() {
    try {
        const result = await adminRequest(ADMIN_API.ENDPOINTS.STATS);
        const stats = result.data;

        const elTotalMessages = document.getElementById('totalMessages');
        const elTotalRequests = document.getElementById('totalRequests');
        const elPendingRequests = document.getElementById('pendingRequests');
        const elCompletedRequests = document.getElementById('completedRequests');
        const elMessagesBadge = document.getElementById('messagesBadge');
        const elRequestsBadge = document.getElementById('requestsBadge');

        if (elTotalMessages) elTotalMessages.textContent = stats.totalMessages || 0;
        if (elTotalRequests) elTotalRequests.textContent = stats.totalRequests || 0;
        if (elPendingRequests) elPendingRequests.textContent = stats.pendingRequests || 0;
        if (elCompletedRequests) elCompletedRequests.textContent = stats.completedRequests || 0;
        if (elMessagesBadge) elMessagesBadge.textContent = stats.unreadMessages || 0;
        if (elRequestsBadge) elRequestsBadge.textContent = stats.pendingRequests || 0;
    } catch (error) {
        adminDebugLog('Stats error:', error);
    }
}

async function loadRecentMessages() {
    try {
        const result = await adminRequest(`${ADMIN_API.ENDPOINTS.MESSAGES}?status=all&limit=5`);
        const messages = result.data || [];
        allMessages = messages;

        const tbody = document.getElementById('recentMessagesTable');
        if (!tbody) return;
        
        if (messages.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No messages yet</td></tr>';
            return;
        }

        tbody.innerHTML = messages.map(msg => `
            <tr>
                <td>${escapeHtml(msg.name)}</td>
                <td>${escapeHtml(msg.phone)}</td>
                <td>${escapeHtml(msg.service_type)}</td>
                <td>${formatDate(msg.created_at)}</td>
                <td><span class="status-badge status-${msg.status}">${msg.status}</span></td>
            </tr>
        `).join('');
    } catch (error) {
        adminDebugLog('Recent messages error:', error);
        const tbody = document.getElementById('recentMessagesTable');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">Error loading</td></tr>';
        }
    }
}

async function loadRecentRequests() {
    try {
        const result = await adminRequest(`${ADMIN_API.ENDPOINTS.REQUESTS}?status=all&limit=5`);
        const requests = result.data || [];
        allRequests = requests;

        const tbody = document.getElementById('recentRequestsTable');
        if (!tbody) return;
        
        if (requests.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No requests yet</td></tr>';
            return;
        }

        tbody.innerHTML = requests.map(req => `
            <tr>
                <td>${escapeHtml(req.customer_name || req.name)}</td>
                <td>${escapeHtml(req.customer_phone || req.phone)}</td>
                <td>${escapeHtml(req.service_type)}</td>
                <td>${formatDate(req.created_at)}</td>
                <td><span class="status-badge status-${(req.request_status || req.status || 'pending').toLowerCase().replace(' ', '')}">${req.request_status || req.status}</span></td>
            </tr>
        `).join('');
    } catch (error) {
        adminDebugLog('Recent requests error:', error);
        const tbody = document.getElementById('recentRequestsTable');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">Error loading</td></tr>';
        }
    }
}

// ========================================
// MESSAGES MANAGEMENT
// ========================================

async function loadMessages(filter = 'all') {
    try {
        const result = await adminRequest(`${ADMIN_API.ENDPOINTS.MESSAGES}?status=${filter}&limit=100`);
        const messages = result.data || [];
        allMessages = messages;

        const tbody = document.getElementById('messagesTable');
        if (!tbody) return;
        
        if (messages.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center">No messages found</td></tr>';
            return;
        }

        tbody.innerHTML = messages.map(msg => `
            <tr>
                <td>#${msg.id}</td>
                <td>${escapeHtml(msg.name)}</td>
                <td>${escapeHtml(msg.phone)}</td>
                <td>${escapeHtml(msg.email || '-')}</td>
                <td>${escapeHtml(msg.service_type)}</td>
                <td>${truncateText(escapeHtml(msg.message || '-'), 30)}</td>
                <td>${formatDate(msg.created_at)}</td>
                <td><span class="status-badge status-${msg.status}">${msg.status}</span></td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn view" onclick="viewMessage(${msg.id})" title="View">
                            <i class="fas fa-eye"></i>
                        </button>
                        <a href="https://wa.me/91${msg.phone}" target="_blank" class="action-btn whatsapp" title="WhatsApp">
                            <i class="fab fa-whatsapp"></i>
                        </a>
                        <button class="action-btn edit" onclick="markMessageRead(${msg.id})" title="Mark Read">
                            <i class="fas fa-check"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        adminDebugLog('Messages error:', error);
        const tbody = document.getElementById('messagesTable');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center">Error loading messages</td></tr>';
        }
    }
}

function viewMessage(id) {
    const message = allMessages.find(m => m.id === id);
    if (!message) return;

    const els = {
        msgName: document.getElementById('msgName'),
        msgPhone: document.getElementById('msgPhone'),
        msgEmail: document.getElementById('msgEmail'),
        msgService: document.getElementById('msgService'),
        msgMessage: document.getElementById('msgMessage'),
        msgDate: document.getElementById('msgDate'),
        whatsappReply: document.getElementById('whatsappReply')
    };

    if (els.msgName) els.msgName.textContent = message.name;
    if (els.msgPhone) els.msgPhone.textContent = message.phone;
    if (els.msgEmail) els.msgEmail.textContent = message.email || '-';
    if (els.msgService) els.msgService.textContent = message.service_type;
    if (els.msgMessage) els.msgMessage.textContent = message.message || '-';
    if (els.msgDate) els.msgDate.textContent = formatDate(message.created_at);
    if (els.whatsappReply) els.whatsappReply.href = `https://wa.me/91${message.phone}`;

    const modalEl = document.getElementById('messageModal');
    if (modalEl && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }

    // Mark as read
    markMessageRead(id);
}

async function markMessageRead(id) {
    try {
        await adminRequest(`${ADMIN_API.ENDPOINTS.MESSAGE_STATUS}/${id}/status`, {
            method: 'PUT',
            body: JSON.stringify({ status: 'read' })
        });

        const filter = document.getElementById('messagesFilter')?.value || 'all';
        loadMessages(filter);
        loadDashboardStats();

        showAdminToast('Message marked as read', 'success');
    } catch (error) {
        adminDebugLog('Update error:', error);
        showAdminToast('Failed to update status', 'error');
    }
}

// ========================================
// SERVICE REQUESTS MANAGEMENT
// ========================================

async function loadRequests(filter = 'all') {
    try {
        const result = await adminRequest(`${ADMIN_API.ENDPOINTS.REQUESTS}?status=${filter}&limit=100`);
        const requests = result.data || [];
        allRequests = requests;

        const tbody = document.getElementById('requestsTable');
        if (!tbody) return;
        
        if (requests.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">No requests found</td></tr>';
            return;
        }

        tbody.innerHTML = requests.map(req => `
            <tr>
                <td>#${req.id}</td>
                <td>${escapeHtml(req.customer_name || req.name)}</td>
                <td>${escapeHtml(req.customer_phone || req.phone)}</td>
                <td>${escapeHtml(req.service_type)}</td>
                <td>${escapeHtml(req.ac_type)}</td>
                <td>${formatDate(req.created_at)}</td>
                <td><span class="status-badge status-${(req.request_status || req.status || 'pending').toLowerCase().replace(' ', '')}">${req.request_status || req.status}</span></td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn view" onclick="viewRequest(${req.id})" title="View">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="action-btn edit" onclick="editRequestStatus(${req.id})" title="Edit Status">
                            <i class="fas fa-edit"></i>
                        </button>
                        <a href="https://wa.me/91${req.customer_phone || req.phone}" target="_blank" class="action-btn whatsapp" title="WhatsApp">
                            <i class="fab fa-whatsapp"></i>
                        </a>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        adminDebugLog('Requests error:', error);
        const tbody = document.getElementById('requestsTable');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">Error loading requests</td></tr>';
        }
    }
}

function viewRequest(id) {
    const request = allRequests.find(r => r.id === id);
    if (!request) return;
    editRequestStatus(id);
}

function editRequestStatus(id) {
    const request = allRequests.find(r => r.id === id);
    if (!request) return;

    const els = {
        requestId: document.getElementById('requestId'),
        requestStatus: document.getElementById('requestStatus'),
        requestNotes: document.getElementById('requestNotes')
    };

    if (els.requestId) els.requestId.value = id;
    if (els.requestStatus) els.requestStatus.value = request.request_status || request.status || 'Pending';
    if (els.requestNotes) els.requestNotes.value = '';

    const modalEl = document.getElementById('statusModal');
    if (modalEl && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}

async function handleStatusUpdate() {
    const id = document.getElementById('requestId').value;
    const status = document.getElementById('requestStatus').value;
    const notes = document.getElementById('requestNotes').value;

    try {
        await adminRequest(`${ADMIN_API.ENDPOINTS.REQUEST_STATUS}/${id}/status`, {
            method: 'PUT',
            body: JSON.stringify({ status, notes })
        });

        const modal = bootstrap.Modal.getInstance(document.getElementById('statusModal'));
        if (modal) modal.hide();

        const filter = document.getElementById('requestsFilter')?.value || 'all';
        loadRequests(filter);
        loadDashboardStats();

        showAdminToast('Status updated successfully', 'success');
    } catch (error) {
        adminDebugLog('Update error:', error);
        showAdminToast('Failed to update status', 'error');
    }
}

// ========================================
// TESTIMONIALS MANAGEMENT
// ========================================

async function loadTestimonials() {
    try {
        const result = await adminRequest(ADMIN_API.ENDPOINTS.TESTIMONIALS);
        const testimonials = result.data || [];

        const tbody = document.getElementById('testimonialsTable');
        if (!tbody) return;
        
        if (testimonials.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No testimonials yet. Click "Add Testimonial" to create one.</td></tr>';
            return;
        }

        tbody.innerHTML = testimonials.map(t => `
            <tr>
                <td>${escapeHtml(t.customer_name)}</td>
                <td>${escapeHtml(t.customer_location || '-')}</td>
                <td>${'⭐'.repeat(t.rating)}</td>
                <td>${truncateText(escapeHtml(t.review_text), 50)}</td>
                <td>
                    <span class="status-badge ${t.is_active ? 'status-completed' : 'status-cancelled'}">
                        ${t.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn edit" onclick="editTestimonial(${t.id})" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="deleteTestimonial(${t.id})" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        adminDebugLog('Testimonials error:', error);
        const tbody = document.getElementById('testimonialsTable');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">Error loading testimonials</td></tr>';
        }
    }
}

function openAddTestimonialModal() {
    const els = {
        testimonialId: document.getElementById('testimonialId'),
        testimonialName: document.getElementById('testimonialName'),
        testimonialLocation: document.getElementById('testimonialLocation'),
        testimonialText: document.getElementById('testimonialText'),
        testimonialRating: document.getElementById('testimonialRating'),
        testimonialPhoto: document.getElementById('testimonialPhoto'),
        testimonialActive: document.getElementById('testimonialActive')
    };

    if (els.testimonialId) els.testimonialId.value = '';
    if (els.testimonialName) els.testimonialName.value = '';
    if (els.testimonialLocation) els.testimonialLocation.value = '';
    if (els.testimonialText) els.testimonialText.value = '';
    if (els.testimonialRating) els.testimonialRating.value = '5';
    if (els.testimonialPhoto) els.testimonialPhoto.value = '';
    if (els.testimonialActive) els.testimonialActive.checked = true;

    const modalTitle = document.querySelector('#testimonialModal .modal-title');
    if (modalTitle) modalTitle.textContent = 'Add Testimonial';

    const modalEl = document.getElementById('testimonialModal');
    if (modalEl && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}

async function editTestimonial(id) {
    try {
        const result = await adminRequest(`${ADMIN_API.ENDPOINTS.TESTIMONIALS}/${id}`);
        const t = result.data;

        const els = {
            testimonialId: document.getElementById('testimonialId'),
            testimonialName: document.getElementById('testimonialName'),
            testimonialLocation: document.getElementById('testimonialLocation'),
            testimonialText: document.getElementById('testimonialText'),
            testimonialRating: document.getElementById('testimonialRating'),
            testimonialPhoto: document.getElementById('testimonialPhoto'),
            testimonialActive: document.getElementById('testimonialActive')
        };

        if (els.testimonialId) els.testimonialId.value = t.id;
        if (els.testimonialName) els.testimonialName.value = t.customer_name;
        if (els.testimonialLocation) els.testimonialLocation.value = t.customer_location || '';
        if (els.testimonialText) els.testimonialText.value = t.review_text;
        if (els.testimonialRating) els.testimonialRating.value = t.rating;
        if (els.testimonialPhoto) els.testimonialPhoto.value = t.customer_photo || '';
        if (els.testimonialActive) els.testimonialActive.checked = t.is_active;

        const modalTitle = document.querySelector('#testimonialModal .modal-title');
        if (modalTitle) modalTitle.textContent = 'Edit Testimonial';

        const modalEl = document.getElementById('testimonialModal');
        if (modalEl && typeof bootstrap !== 'undefined') {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        }
    } catch (error) {
        adminDebugLog('Edit testimonial error:', error);
        showAdminToast('Failed to load testimonial', 'error');
    }
}

async function saveTestimonial() {
    const id = document.getElementById('testimonialId')?.value;
    const data = {
        customer_name: document.getElementById('testimonialName')?.value,
        customer_location: document.getElementById('testimonialLocation')?.value,
        review_text: document.getElementById('testimonialText')?.value,
        rating: parseInt(document.getElementById('testimonialRating')?.value),
        customer_photo: document.getElementById('testimonialPhoto')?.value,
        is_active: document.getElementById('testimonialActive')?.checked
    };

    if (!data.customer_name || !data.review_text) {
        showAdminToast('Please fill required fields', 'error');
        return;
    }

    try {
        const url = id ? `${ADMIN_API.ENDPOINTS.TESTIMONIALS}/${id}` : ADMIN_API.ENDPOINTS.TESTIMONIALS;
        const method = id ? 'PUT' : 'POST';

        await adminRequest(url, { method, body: JSON.stringify(data) });

        const modal = bootstrap.Modal.getInstance(document.getElementById('testimonialModal'));
        if (modal) modal.hide();
        
        loadTestimonials();
        showAdminToast(id ? 'Testimonial updated successfully' : 'Testimonial added successfully', 'success');
    } catch (error) {
        adminDebugLog('Save testimonial error:', error);
        showAdminToast('Failed to save testimonial', 'error');
    }
}

async function deleteTestimonial(id) {
    if (!confirm('Are you sure you want to delete this testimonial?')) return;

    try {
        await adminRequest(`${ADMIN_API.ENDPOINTS.TESTIMONIALS}/${id}`, { method: 'DELETE' });
        loadTestimonials();
        showAdminToast('Testimonial deleted successfully', 'success');
    } catch (error) {
        adminDebugLog('Delete testimonial error:', error);
        showAdminToast('Failed to delete testimonial', 'error');
    }
}

// ========================================
// SERVICES MANAGEMENT
// ========================================

async function loadServices() {
    try {
        const result = await adminRequest(ADMIN_API.ENDPOINTS.SERVICES);
        const services = result.data || [];

        const tbody = document.getElementById('servicesTable');
        if (!tbody) return;
        
        if (services.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No services yet. Click "Add Service" to create one.</td></tr>';
            return;
        }

        tbody.innerHTML = services.map(s => `
            <tr>
                <td>${escapeHtml(s.service_name)}</td>
                <td>${escapeHtml(s.starting_price)}</td>
                <td>${escapeHtml(s.duration || '-')}</td>
                <td>${s.features ? (typeof s.features === 'string' ? JSON.parse(s.features).length : s.features.length) : 0} features</td>
                <td>
                    <span class="status-badge ${s.is_active ? 'status-completed' : 'status-cancelled'}">
                        ${s.is_active ? 'Active' : 'Inactive'}
                    </span>
                </td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn edit" onclick="editService(${s.id})" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="deleteService(${s.id})" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        adminDebugLog('Services error:', error);
        const tbody = document.getElementById('servicesTable');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">Error loading services</td></tr>';
        }
    }
}

function openAddServiceModal() {
    const els = {
        serviceId: document.getElementById('serviceId'),
        serviceName: document.getElementById('serviceName'),
        serviceSlug: document.getElementById('serviceSlug'),
        servicePrice: document.getElementById('servicePrice'),
        serviceDuration: document.getElementById('serviceDuration'),
        serviceDescription: document.getElementById('serviceDescription'),
        serviceIcon: document.getElementById('serviceIcon'),
        serviceFeatures: document.getElementById('serviceFeatures'),
        serviceActive: document.getElementById('serviceActive')
    };

    Object.keys(els).forEach(key => {
        if (key === 'serviceActive' && els[key]) els[key].checked = true;
        else if (els[key]) els[key].value = '';
    });

    const modalTitle = document.querySelector('#serviceModal .modal-title');
    if (modalTitle) modalTitle.textContent = 'Add Service';

    const modalEl = document.getElementById('serviceModal');
    if (modalEl && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}

async function editService(id) {
    try {
        const result = await adminRequest(`${ADMIN_API.ENDPOINTS.SERVICES}/${id}`);
        const s = result.data;

        const els = {
            serviceId: document.getElementById('serviceId'),
            serviceName: document.getElementById('serviceName'),
            serviceSlug: document.getElementById('serviceSlug'),
            servicePrice: document.getElementById('servicePrice'),
            serviceDuration: document.getElementById('serviceDuration'),
            serviceDescription: document.getElementById('serviceDescription'),
            serviceIcon: document.getElementById('serviceIcon'),
            serviceFeatures: document.getElementById('serviceFeatures'),
            serviceActive: document.getElementById('serviceActive')
        };

        if (els.serviceId) els.serviceId.value = s.id;
        if (els.serviceName) els.serviceName.value = s.service_name;
        if (els.serviceSlug) els.serviceSlug.value = s.service_slug;
        if (els.servicePrice) els.servicePrice.value = s.starting_price;
        if (els.serviceDuration) els.serviceDuration.value = s.duration || '';
        if (els.serviceDescription) els.serviceDescription.value = s.description || '';
        if (els.serviceIcon) els.serviceIcon.value = s.icon_class || '';
        if (els.serviceFeatures) els.serviceFeatures.value = s.features ? (typeof s.features === 'string' ? JSON.parse(s.features).join(', ') : s.features.join(', ')) : '';
        if (els.serviceActive) els.serviceActive.checked = s.is_active;

        const modalTitle = document.querySelector('#serviceModal .modal-title');
        if (modalTitle) modalTitle.textContent = 'Edit Service';

        const modalEl = document.getElementById('serviceModal');
        if (modalEl && typeof bootstrap !== 'undefined') {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        }
    } catch (error) {
        adminDebugLog('Edit service error:', error);
        showAdminToast('Failed to load service', 'error');
    }
}

async function saveService() {
    const id = document.getElementById('serviceId')?.value;
    const featuresText = document.getElementById('serviceFeatures')?.value || '';

    const data = {
        service_name: document.getElementById('serviceName')?.value,
        service_slug: document.getElementById('serviceSlug')?.value,
        starting_price: document.getElementById('servicePrice')?.value,
        duration: document.getElementById('serviceDuration')?.value,
        description: document.getElementById('serviceDescription')?.value,
        icon_class: document.getElementById('serviceIcon')?.value,
        features: featuresText ? featuresText.split(',').map(f => f.trim()) : [],
        is_active: document.getElementById('serviceActive')?.checked
    };

    if (!data.service_name || !data.service_slug || !data.starting_price) {
        showAdminToast('Please fill required fields', 'error');
        return;
    }

    try {
        const url = id ? `${ADMIN_API.ENDPOINTS.SERVICES}/${id}` : ADMIN_API.ENDPOINTS.SERVICES;
        const method = id ? 'PUT' : 'POST';

        await adminRequest(url, { method, body: JSON.stringify(data) });

        const modal = bootstrap.Modal.getInstance(document.getElementById('serviceModal'));
        if (modal) modal.hide();
        
        loadServices();
        showAdminToast(id ? 'Service updated successfully' : 'Service added successfully', 'success');
    } catch (error) {
        adminDebugLog('Save service error:', error);
        showAdminToast('Failed to save service', 'error');
    }
}

async function deleteService(id) {
    if (!confirm('Are you sure you want to delete this service?')) return;

    try {
        await adminRequest(`${ADMIN_API.ENDPOINTS.SERVICES}/${id}`, { method: 'DELETE' });
        loadServices();
        showAdminToast('Service deleted successfully', 'success');
    } catch (error) {
        adminDebugLog('Delete service error:', error);
        showAdminToast('Failed to delete service', 'error');
    }
}

// ========================================
// PRODUCTS MANAGEMENT
// ========================================

async function loadProducts() {
    const filter = document.getElementById('productsFilter')?.value || 'all';

    try {
        const url = filter === 'all' 
            ? ADMIN_API.ENDPOINTS.PRODUCTS 
            : `${ADMIN_API.ENDPOINTS.PRODUCTS}?type=${filter}`;

        const result = await adminRequest(url);
        const products = result.data || [];

        const tbody = document.getElementById('productsTable');
        if (!tbody) return;
        
        if (products.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No products yet. Click "Add Product" to create one.</td></tr>';
            return;
        }

        tbody.innerHTML = products.map(p => `
            <tr>
                <td>
                    <span class="status-badge ${p.product_type === 'buy' ? 'status-primary' : 'status-info'}">
                        ${p.product_type === 'buy' ? 'Sale' : 'Rent'}
                    </span>
                </td>
                <td>${escapeHtml(p.product_name)}</td>
                <td>${escapeHtml(p.capacity || '-')}</td>
                <td>${escapeHtml(p.price)}</td>
                <td>
                    <span class="status-badge ${p.is_available || p.is_active ? 'status-completed' : 'status-cancelled'}">
                        ${p.stock_status || (p.is_available ? 'In Stock' : 'Out of Stock')}
                    </span>
                </td>
                <td>
                    <div class="action-btns">
                        <button class="action-btn edit" onclick="editProduct(${p.id})" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" onclick="deleteProduct(${p.id})" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        adminDebugLog('Products error:', error);
        const tbody = document.getElementById('productsTable');
        if (tbody) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">Error loading products</td></tr>';
        }
    }
}

function openAddProductModal() {
    const els = {
        productId: document.getElementById('productId'),
        productType: document.getElementById('productType'),
        productName: document.getElementById('productName'),
        productCapacity: document.getElementById('productCapacity'),
        productACType: document.getElementById('productACType'),
        productStar: document.getElementById('productStar'),
        productPrice: document.getElementById('productPrice'),
        productBrand: document.getElementById('productBrand'),
        productDescription: document.getElementById('productDescription'),
        productFeatures: document.getElementById('productFeatures'),
        productActive: document.getElementById('productActive')
    };

    if (els.productId) els.productId.value = '';
    if (els.productType) els.productType.value = 'buy';
    if (els.productName) els.productName.value = '';
    if (els.productCapacity) els.productCapacity.value = '1.5 Ton';
    if (els.productACType) els.productACType.value = 'Split';
    if (els.productStar) els.productStar.value = '5';
    if (els.productPrice) els.productPrice.value = '';
    if (els.productBrand) els.productBrand.value = '';
    if (els.productDescription) els.productDescription.value = '';
    if (els.productFeatures) els.productFeatures.value = '';
    if (els.productActive) els.productActive.checked = true;

    const modalTitle = document.querySelector('#productModal .modal-title');
    if (modalTitle) modalTitle.textContent = 'Add AC Product';

    const modalEl = document.getElementById('productModal');
    if (modalEl && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}

async function editProduct(id) {
    try {
        const result = await adminRequest(`${ADMIN_API.ENDPOINTS.PRODUCTS}/${id}`);
        const p = result.data;

        const els = {
            productId: document.getElementById('productId'),
            productType: document.getElementById('productType'),
            productName: document.getElementById('productName'),
            productCapacity: document.getElementById('productCapacity'),
            productACType: document.getElementById('productACType'),
            productStar: document.getElementById('productStar'),
            productPrice: document.getElementById('productPrice'),
            productBrand: document.getElementById('productBrand'),
            productDescription: document.getElementById('productDescription'),
            productFeatures: document.getElementById('productFeatures'),
            productActive: document.getElementById('productActive')
        };

        if (els.productId) els.productId.value = p.id;
        if (els.productType) els.productType.value = p.product_type;
        if (els.productName) els.productName.value = p.product_name;
        if (els.productCapacity) els.productCapacity.value = p.capacity || '1.5 Ton';
        if (els.productACType) els.productACType.value = p.ac_type || 'Split';
        if (els.productStar) els.productStar.value = p.star_rating || '5';
        if (els.productPrice) els.productPrice.value = p.price;
        if (els.productBrand) els.productBrand.value = p.brand || '';
        if (els.productDescription) els.productDescription.value = p.description || '';
        if (els.productFeatures) els.productFeatures.value = p.features ? (typeof p.features === 'string' ? JSON.parse(p.features).join(', ') : p.features.join(', ')) : '';
        if (els.productActive) els.productActive.checked = p.is_active;

        const modalTitle = document.querySelector('#productModal .modal-title');
        if (modalTitle) modalTitle.textContent = 'Edit AC Product';

        const modalEl = document.getElementById('productModal');
        if (modalEl && typeof bootstrap !== 'undefined') {
            const modal = new bootstrap.Modal(modalEl);
            modal.show();
        }
    } catch (error) {
        adminDebugLog('Edit product error:', error);
        showAdminToast('Failed to load product', 'error');
    }
}

async function saveProduct() {
    const id = document.getElementById('productId')?.value;
    const featuresText = document.getElementById('productFeatures')?.value || '';

    const data = {
        product_type: document.getElementById('productType')?.value,
        product_name: document.getElementById('productName')?.value,
        capacity: document.getElementById('productCapacity')?.value,
        ac_type: document.getElementById('productACType')?.value,
        star_rating: parseInt(document.getElementById('productStar')?.value),
        price: document.getElementById('productPrice')?.value,
        brand: document.getElementById('productBrand')?.value,
        description: document.getElementById('productDescription')?.value,
        features: featuresText ? featuresText.split(',').map(f => f.trim()) : [],
        is_active: document.getElementById('productActive')?.checked
    };

    if (!data.product_name || !data.price) {
        showAdminToast('Please fill required fields', 'error');
        return;
    }

    try {
        const url = id ? `${ADMIN_API.ENDPOINTS.PRODUCTS}/${id}` : ADMIN_API.ENDPOINTS.PRODUCTS;
        const method = id ? 'PUT' : 'POST';

        await adminRequest(url, { method, body: JSON.stringify(data) });

        const modal = bootstrap.Modal.getInstance(document.getElementById('productModal'));
        if (modal) modal.hide();
        
        loadProducts();
        showAdminToast(id ? 'Product updated successfully' : 'Product added successfully', 'success');
    } catch (error) {
        adminDebugLog('Save product error:', error);
        showAdminToast('Failed to save product', 'error');
    }
}

async function deleteProduct(id) {
    if (!confirm('Are you sure you want to delete this product?')) return;

    try {
        await adminRequest(`${ADMIN_API.ENDPOINTS.PRODUCTS}/${id}`, { method: 'DELETE' });
        loadProducts();
        showAdminToast('Product deleted successfully', 'success');
    } catch (error) {
        adminDebugLog('Delete product error:', error);
        showAdminToast('Failed to delete product', 'error');
    }
}

// ========================================
// CONTENT SETTINGS MANAGEMENT
// ========================================

async function loadContentSettings(section = 'content') {
    try {
        // Load hero section as default
        const result = await adminRequest(ADMIN_API.ENDPOINTS.HERO);
        const content = result.data || {};

        // Map to form fields based on section
        if (section === 'hero' || section === 'content') {
            const els = {
                heroTitle: document.getElementById('heroTitle'),
                heroSubtitle: document.getElementById('heroSubtitle'),
                contactPhone: document.getElementById('contactPhone'),
                contactEmail: document.getElementById('contactEmail'),
                businessHours: document.getElementById('businessHours'),
                address: document.getElementById('address')
            };

            if (els.heroTitle) els.heroTitle.value = content.title || els.heroTitle.value || '';
            if (els.heroSubtitle) els.heroSubtitle.value = content.subtitle || els.heroSubtitle.value || '';
            if (els.contactPhone) els.contactPhone.value = content.cta_phone || els.contactPhone.value || '';
            if (els.contactEmail) els.contactEmail.value = content.contact_email || els.contactEmail.value || '';
            if (els.businessHours) els.businessHours.value = content.business_hours || els.businessHours.value || '';
            if (els.address) els.address.value = content.address || els.address.value || '';
        }
    } catch (error) {
        adminDebugLog('Load content error:', error);
    }
}

async function handleContentSubmit(e) {
    e.preventDefault();

    const data = {
        title: document.getElementById('heroTitle')?.value,
        subtitle: document.getElementById('heroSubtitle')?.value,
        cta_phone: document.getElementById('contactPhone')?.value,
        contact_email: document.getElementById('contactEmail')?.value,
        business_hours: document.getElementById('businessHours')?.value,
        address: document.getElementById('address')?.value
    };

    try {
        await adminRequest(ADMIN_API.ENDPOINTS.HERO, {
            method: 'PUT',
            body: JSON.stringify(data)
        });

        showAdminToast('Content saved successfully', 'success');
    } catch (error) {
        adminDebugLog('Save content error:', error);
        showAdminToast('Failed to save content', 'error');
    }
}

// ========================================
// GALLERY MANAGEMENT
// ========================================

async function loadGallery() {
    try {
        const result = await adminRequest(`${ADMIN_API.ENDPOINTS.GALLERY}?category=all`);
        const images = result.data || [];

        const grid = document.getElementById('galleryGrid');
        if (!grid) return;
        
        if (images.length === 0) {
            grid.innerHTML = '<div class="text-center text-muted py-5">No images uploaded yet</div>';
            return;
        }

        grid.innerHTML = images.map(img => `
            <div class="gallery-item">
                <img src="${img.image_url || img.url}" alt="${escapeHtml(img.caption || 'Gallery image')}">
                <div class="gallery-item-actions">
                    <button class="btn btn-sm btn-danger" onclick="deleteGalleryImage(${img.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        adminDebugLog('Gallery error:', error);
        const grid = document.getElementById('galleryGrid');
        if (grid) {
            grid.innerHTML = '<div class="text-center text-muted py-5">Error loading gallery</div>';
        }
    }
}

async function handleImageUpload(e) {
    e.preventDefault();
    
    const imageInput = document.getElementById('imageInput');
    const categorySelect = document.getElementById('imageCategory');
    
    if (!imageInput || !imageInput.files || imageInput.files.length === 0) {
        showAdminToast('Please select images to upload', 'error');
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < imageInput.files.length; i++) {
        formData.append('images', imageInput.files[i]);
    }
    formData.append('category', categorySelect?.value || 'gallery');

    try {
        const response = await fetch(`${ADMIN_API.BASE_URL}${ADMIN_API.ENDPOINTS.GALLERY}`, {
            method: 'POST',
            headers: {
                // NO API_KEY - using session-based authentication
                // Content-Type will be set automatically by browser for FormData
            },
            credentials: 'include',
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showAdminToast('Images uploaded successfully', 'success');
            loadGallery();
            imageInput.value = '';
        } else {
            showAdminToast(result.message || 'Failed to upload images', 'error');
        }
    } catch (error) {
        adminDebugLog('Upload error:', error);
        showAdminToast('Failed to upload images', 'error');
    }
}

async function deleteGalleryImage(id) {
    if (!confirm('Are you sure you want to delete this image?')) return;

    try {
        await adminRequest(`${ADMIN_API.ENDPOINTS.GALLERY}/${id}`, { method: 'DELETE' });
        loadGallery();
        showAdminToast('Image deleted successfully', 'success');
    } catch (error) {
        adminDebugLog('Delete image error:', error);
        showAdminToast('Failed to delete image', 'error');
    }
}

// ========================================
// SETTINGS MANAGEMENT
// ========================================

async function loadSettings() {
    try {
        const result = await adminRequest(ADMIN_API.ENDPOINTS.SETTINGS);
        const settings = result.data || {};

        // Load settings into form fields
        const form = document.getElementById('settingsForm');
        if (form) {
            // Populate form with settings
            Object.keys(settings).forEach(key => {
                const field = form.querySelector(`[name="${key}"]`);
                if (field) {
                    field.value = settings[key];
                }
            });
        }
    } catch (error) {
        adminDebugLog('Load settings error:', error);
    }
}

async function handleSettingsSubmit(e) {
    e.preventDefault();

    const form = document.getElementById('settingsForm');
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
        await adminRequest(ADMIN_API.ENDPOINTS.SETTINGS, {
            method: 'PUT',
            body: JSON.stringify(data)
        });

        showAdminToast('Settings saved successfully', 'success');
    } catch (error) {
        adminDebugLog('Save settings error:', error);
        showAdminToast('Failed to save settings', 'error');
    }
}

// Export functions for global access
window.navigateToSection = navigateToSection;
window.openAddTestimonialModal = openAddTestimonialModal;
window.editTestimonial = editTestimonial;
window.saveTestimonial = saveTestimonial;
window.deleteTestimonial = deleteTestimonial;
window.openAddServiceModal = openAddServiceModal;
window.editService = editService;
window.saveService = saveService;
window.deleteService = deleteService;
window.openAddProductModal = openAddProductModal;
window.editProduct = editProduct;
window.saveProduct = saveProduct;
window.deleteProduct = deleteProduct;
window.viewMessage = viewMessage;
window.markMessageRead = markMessageRead;
window.viewRequest = viewRequest;
window.editRequestStatus = editRequestStatus;
window.deleteGalleryImage = deleteGalleryImage;

// ========================================
// ADMIN PROFILE & PASSWORD MANAGEMENT
// ========================================

/**
 * Load admin profile settings
 */
async function loadAdminProfile() {
    try {
        const result = await adminRequest('/api/admin/profile');
        const profile = result.data || {};
        
        // Fill profile fields
        const els = {
            profileUsername: document.getElementById('profileUsername'),
            profileFullName: document.getElementById('profileFullName'),
            profileEmail: document.getElementById('profileEmail'),
            profilePhone: document.getElementById('profilePhone')
        };
        
        if (els.profileUsername) els.profileUsername.value = profile.username || '';
        if (els.profileFullName) els.profileFullName.value = profile.full_name || '';
        if (els.profileEmail) els.profileEmail.value = profile.email || '';
        if (els.profilePhone) els.profilePhone.value = profile.phone || '';
        
        // Display last login
        const lastLoginEl = document.getElementById('profileLastLogin');
        if (lastLoginEl && profile.last_login) {
            lastLoginEl.textContent = formatDate(profile.last_login);
        }
    } catch (error) {
        adminDebugLog('Load profile error:', error);
        showAdminToast('Failed to load profile', 'error');
    }
}

/**
 * Update admin profile
 */
async function updateAdminProfile() {
    const data = {
        full_name: document.getElementById('profileFullName')?.value,
        email: document.getElementById('profileEmail')?.value,
        phone: document.getElementById('profilePhone')?.value
    };

    // Validation
    if (!data.full_name || !data.email) {
        showAdminToast('Please fill required fields', 'error');
        return;
    }

    try {
        await adminRequest('/api/admin/profile', {
            method: 'PUT',
            body: JSON.stringify(data)
        });

        showAdminToast('Profile updated successfully', 'success');
        
        // Update displayed name
        const adminNameEl = document.getElementById('adminName');
        if (adminNameEl && data.full_name) {
            adminNameEl.textContent = data.full_name;
        }
    } catch (error) {
        adminDebugLog('Update profile error:', error);
        showAdminToast(error.message || 'Failed to update profile', 'error');
    }
}

/**
 * Open change password modal
 */
function openChangePasswordModal() {
    // Clear form
    const els = {
        currentPassword: document.getElementById('currentPassword'),
        newPassword: document.getElementById('newPassword'),
        confirmPassword: document.getElementById('confirmPassword')
    };
    
    Object.values(els).forEach(el => { if (el) el.value = ''; });
    
    // Show modal
    const modalEl = document.getElementById('changePasswordModal');
    if (modalEl && typeof bootstrap !== 'undefined') {
        const modal = new bootstrap.Modal(modalEl);
        modal.show();
    }
}

/**
 * Change admin password
 */
async function changeAdminPassword() {
    const data = {
        current_password: document.getElementById('currentPassword')?.value,
        new_password: document.getElementById('newPassword')?.value,
        confirm_password: document.getElementById('confirmPassword')?.value
    };

    // Validation
    if (!data.current_password || !data.new_password) {
        showAdminToast('Please fill all password fields', 'error');
        return;
    }

    if (data.new_password.length < 6) {
        showAdminToast('New password must be at least 6 characters', 'error');
        return;
    }

    if (data.new_password !== data.confirm_password) {
        showAdminToast('New passwords do not match', 'error');
        return;
    }

    try {
        const result = await adminRequest('/api/admin/change-password', {
            method: 'POST',
            body: JSON.stringify(data)
        });

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('changePasswordModal'));
        if (modal) modal.hide();

        showAdminToast(result.message || 'Password changed successfully', 'success');

        // Clear form
        const els = {
            currentPassword: document.getElementById('currentPassword'),
            newPassword: document.getElementById('newPassword'),
            confirmPassword: document.getElementById('confirmPassword')
        };
        Object.values(els).forEach(el => { if (el) el.value = ''; });

    } catch (error) {
        adminDebugLog('Change password error:', error);
        const errorMsg = error.message || 'Failed to change password';
        showAdminToast(errorMsg, 'error');
    }
}

// Export new functions
window.loadAdminProfile = loadAdminProfile;
window.updateAdminProfile = updateAdminProfile;
window.openChangePasswordModal = openChangePasswordModal;
window.changeAdminPassword = changeAdminPassword;
