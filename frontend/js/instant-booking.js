/**
 * Instant Booking Widget
 * Floating button with quick booking form
 * No login required
 */
(function() {
    'use strict';
    
    function createInstantBooking() {
        const widget = document.createElement('div');
        widget.className = 'instant-booking';
        widget.innerHTML = `
            <button class="instant-booking-btn" id="instantBookingBtn" aria-label="Book service instantly">
                <i class="fas fa-calendar-plus"></i>
            </button>
            <div class="instant-booking-popup" id="instantBookingPopup">
                <h4><i class="fas fa-bolt me-2"></i>Quick Book</h4>
                <form id="instantBookingForm">
                    <input type="text" class="form-control" id="quickName" placeholder="Your Name *" required>
                    <input type="tel" class="form-control" id="quickPhone" placeholder="Phone Number *" required maxlength="10">
                    <select class="form-control" id="quickService" required>
                        <option value="">Select Service *</option>
                        <option value="installation">AC Installation</option>
                        <option value="repair">AC Repair</option>
                        <option value="gas">Gas Refill</option>
                        <option value="cleaning">Deep Cleaning</option>
                        <option value="amc">AMC Plan</option>
                    </select>
                    <textarea class="form-control" id="quickAddress" placeholder="Your Address *" rows="2" required></textarea>
                    <button type="submit" class="btn btn-primary-glow w-100">
                        <i class="fas fa-paper-plane me-2"></i>Submit Request
                    </button>
                    <div class="whatsapp-quick-replies mt-3">
                        <small class="text-muted d-block mb-2">Or chat directly:</small>
                        <a href="https://wa.me/919819104977?text=Hi, I need AC service" class="quick-reply-btn" target="_blank">
                            <i class="fab fa-whatsapp me-1"></i>WhatsApp
                        </a>
                    </div>
                </form>
            </div>
        `;
        
        document.body.appendChild(widget);
        
        const btn = document.getElementById('instantBookingBtn');
        const popup = document.getElementById('instantBookingPopup');
        const form = document.getElementById('instantBookingForm');
        
        // Toggle popup
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            popup.classList.toggle('show');
        });
        
        // Close on outside click
        document.addEventListener('click', (e) => {
            if (!widget.contains(e.target)) {
                popup.classList.remove('show');
            }
        });
        
        // Form submission
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                
                const name = document.getElementById('quickName').value.trim();
                const phone = document.getElementById('quickPhone').value.trim();
                const service = document.getElementById('quickService').value;
                const address = document.getElementById('quickAddress').value.trim();
                
                if (!name || !phone || !service || !address) {
                    alert('Please fill all required fields');
                    return;
                }
                
                if (!/^[6-9]\d{9}$/.test(phone)) {
                    alert('Please enter a valid 10-digit mobile number');
                    return;
                }
                
                // Submit to backend
                fetch('http://localhost:5000/api/service-request', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: name,
                        phone: phone,
                        serviceType: service,
                        address: address,
                        source: 'instant_booking'
                    })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        alert('✅ Service request submitted! We will contact you shortly.');
                        form.reset();
                        popup.classList.remove('show');
                    } else {
                        alert('❌ Error: ' + (data.message || 'Something went wrong'));
                    }
                })
                .catch(err => {
                    alert('❌ Error submitting request. Please call us at +91-9819104977');
                    console.error('Booking error:', err);
                });
            });
        }
        
        console.log('✅ Instant Booking Widget initialized');
    }
    
    // Initialize
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createInstantBooking);
    } else {
        createInstantBooking();
    }
})();
