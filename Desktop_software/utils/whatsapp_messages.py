
"""

WhatsApp Message Templates
Pre-defined messages for customer communication
"""

WHATSAPP_MESSAGES = {
    # ===========================================
    # SERVICE REQUEST MESSAGES
    # ===========================================
    
    'service_confirm': """
✅ *Service Request Confirmed*

Namaste {name}!

Aapka service request humne receive kar liya hai.

🔧 Service: {service_type}
📍 Location: {location}

Hamara technician aapse jald contact karega.

Dhanyavaad! 🙏
*Ansh Air Cool*
📞 9918331262
    """,

    'technician_assigned': """
👨‍🔧 *Technician Assigned*

Namaste {name}!

Aapki service ke liye technician assign ho gaya hai.

👤 Technician: {technician_name}
📞 Phone: {technician_phone}
⏰ Time: {visit_time}

Koi bhi query ke liye call karein: 9918331262

*Ansh Air Cool*
    """,

    'work_completed': """
✅ *Service Completed*

Namaste {name}!

Aapki AC service successfully complete ho gayi hai.

💰 Total Amount: ₹{amount}
📅 Service Date: {date}

Agar koi problem ho toh humein batayein.

Dhanyavaad! 🙏
*Ansh Air Cool*
📞 9918331262
    """,

    # ===========================================
    # PAYMENT MESSAGES
    # ===========================================
    
    'payment_reminder': """
💳 *Payment Reminder*

Namaste {name},

Aapka payment abhi tak pending hai.

📄 Invoice: {invoice_number}
💰 Amount: ₹{amount}

Please payment clear karein:
UPI: anshaircool@paytm
Phone: 9918331262

Dhanyavaad! 🙏
*Ansh Air Cool*
    """,

    'payment_received': """
✅ *Payment Received*

Namaste {name}!

Aapka payment humne receive kar liya hai.

📄 Invoice: {invoice_number}
💰 Amount: ₹{amount}
📅 Date: {date}

Dhanyavaad! 🙏
*Ansh Air Cool*
📞 9918331262
    """,

    # ===========================================
    # THANK YOU / FEEDBACK MESSAGES
    # ===========================================
    
    'thank_you': """
🌟 *Thank You!*

Namaste {name},

Humara service use karne ke liye dhanyavaad!

Aapki feedback humare liye important hai.
Please rate our service: 1-5 ⭐

*Ansh Air Cool*
📞 9918331262
    """,

    'feedback_request': """
⭐ *We Value Your Feedback*

Namaste {name},

Kal hamari team ne aapki service ki thi.

Kripya batayein:
1. Service quality? (1-5 ⭐)
2. Technician behavior? (1-5 ⭐)
3. Koi suggestion?

*Ansh Air Cool*
📞 9918331262
    """,

    # ===========================================
    # AMC MESSAGES
    # ===========================================
    
    'amc_renewal': """
⚠️ *AMC Renewal Reminder*

Namaste {name},

Aapka AMC contract expire ho raha hai.

📅 Expiry Date: {expiry_date}
📞 Renewal ke liye call karein: 9918331262

*Ansh Air Cool*
    """,

    'amc_expiring_soon': """
🔔 *AMC Expiring in 7 Days*

Namaste {name},

Aapka AMC contract 7 din mein expire ho raha hai.

📅 Expiry: {expiry_date}
💰 Renewal Amount: ₹{amount}

Renew karwane ke liye call karein: 9918331262

*Ansh Air Cool*
    """,

    'amc_visit_scheduled': """
📅 *AMC Visit Scheduled*

Namaste {name},

Aapki AMC service visit schedule ho gayi hai.

📅 Date: {visit_date}
⏰ Time: {visit_time}
👨‍🔧 Technician: {technician_name}

*Ansh Air Cool*
📞 9918331262
    """,

    # ===========================================
    # ONLINE REQUEST MESSAGES (Website)
    # ===========================================
    
    'online_request_received': """
🌐 *New Service Request Received*

Customer: {name}
📞 Phone: {phone}
🔧 Service: {service_type}
📍 Address: {address}
💬 Message: {message}

Website se request aaya hai.
Contact karein: 9918331262

*Ansh Air Cool*
    """,

    'online_request_welcome': """
🙏 *Welcome to Ansh Air Cool!*

Namaste {name},

Aapka message humne receive kar liya hai.

🔧 Service: {service_type}

Hamara team member aapse 2 ghante mein contact karega.

Emergency? Call: 9918331262

*Ansh Air Cool*
    """,

    # ===========================================
    # APPOINTMENT MESSAGES
    # ===========================================
    
    'appointment_confirm': """
✅ *Appointment Confirmed*

Namaste {name},

Aapka appointment confirm ho gaya hai.

📅 Date: {appointment_date}
⏰ Time: {appointment_time}
🔧 Service: {service_type}
📍 Address: {address}

*Ansh Air Cool*
📞 9918331262
    """,

    'appointment_reminder': """
🔔 *Appointment Reminder*

Namaste {name},

Kal aapka appointment hai.

📅 Date: {appointment_date}
⏰ Time: {appointment_time}
🔧 Service: {service_type}

Koi cancellation? Call: 9918331262

*Ansh Air Cool*
    """,

    'appointment_reschedule': """
🔄 *Appointment Rescheduled*

Namaste {name},

Aapka appointment reschedule ho gaya hai.

📅 New Date: {appointment_date}
⏰ New Time: {appointment_time}

Confirm? Call: 9918331262

*Ansh Air Cool*
    """,

    # ===========================================
    # EMERGENCY MESSAGES
    # ===========================================
    
    'emergency_contact': """
🚨 *Emergency Service Request*

Customer: {name}
📞 Phone: {phone}
🔧 Issue: {message}
📍 Address: {address}

URGENT! Contact karein: 9918331262

*Ansh Air Cool*
    """,

    # ===========================================
    # GENERAL MESSAGES
    # ===========================================
    
    'greeting': """
🙏 *Namaste from Ansh Air Cool!*

Humara contact karne ke liye dhanyavaad.

Humari services:
✅ AC Installation
✅ AC Repair
✅ Gas Refill
✅ AMC Plans
✅ PCB Repair

Call karein: 9918331262

*Ansh Air Cool*
    """,

    'business_hours': """
🕐 *Business Hours*

Monday - Saturday: 9:00 AM - 8:00 PM
Sunday: 10:00 AM - 6:00 PM

Emergency: 24/7 Available

📞 9918331262
*Ansh Air Cool*
    """,

    'location': """
📍 *Our Location*

Ansh Air Cool
123 Cool Street, Mumbai
Maharashtra 400001

📞 9918331262

Google Maps: [Location link bhejein]

*Ansh Air Cool*
    """,

    # ===========================================
    # INVOICE SHARING MESSAGES
    # ===========================================

    'invoice_share': """
📄 *Invoice - {invoice_number}*

Namaste {customer_name}!

Aapka invoice taiyar hai.

💰 Total Amount: ₹{total_amount}
💵 Paid: ₹{paid_amount}
⚠️ Balance Due: ₹{balance_amount}

📅 Invoice Date: {invoice_date}

Payment ke liye sampark karein: 9918331262

Dhanyavaad! 🙏
*Ansh Air Cool*
📞 9918331262
    """,

    'payment_reminder': """
💳 *Payment Reminder*

Namaste {customer_name},

Aapke upar ₹{balance_amount} baki hai.

Invoice No: {invoice_number}
Date: {invoice_date}

Kripya payment clear karein.

📞 9918331262
*Ansh Air Cool*
    """,

    'invoice_paid': """
✅ *Payment Received*

Namaste {customer_name}!

Aapka payment successfully receive ho gaya hai.

🧾 Invoice: {invoice_number}
💰 Amount: ₹{total_amount}

Dhanyavaad! 🙏
*Ansh Air Cool*
📞 9918331262
    """,
}


def get_message_template(template_name):
    """Get a message template by name"""
    return WHATSAPP_MESSAGES.get(template_name, None)


def get_all_templates():
    """Get all available templates"""
    return WHATSAPP_MESSAGES.copy()


def format_message(template_name, **kwargs):
    """
    Format a message template with variables
    
    Usage:
        msg = format_message('service_confirm', name='Rahul', service_type='AC Repair', location='Mumbai')
    """
    template = get_message_template(template_name)
    if not template:
        return None
    
    try:
        return template.format(**kwargs)
    except KeyError as e:
        print(f"Missing variable in template: {e}")
        return template
