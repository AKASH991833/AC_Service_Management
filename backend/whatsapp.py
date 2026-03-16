"""
WhatsApp Auto-Message Service
Sends automatic WhatsApp messages to customers when they submit forms
Uses UltraMsg API (easy & affordable WhatsApp Business API)
"""

import requests
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WhatsAppService:
    """WhatsApp messaging service using UltraMsg API"""
    
    def __init__(self):
        self.enabled = os.getenv('WHATSAPP_ENABLED', 'false').lower() == 'true'
        self.instance_id = os.getenv('ULTRAMSG_INSTANCE_ID', '')
        self.token = os.getenv('ULTRAMSG_TOKEN', '')
        self.sender_number = os.getenv('WHATSAPP_SENDER_NUMBER', '919819104977')
        
        # UltraMsg API endpoints
        self.base_url = "https://api.ultramsg.com"
        
        if not self.enabled:
            logger.info("WhatsApp messaging is disabled (set WHATSAPP_ENABLED=true to enable)")
    
    def send_message(self, phone_number, message):
        """
        Send WhatsApp message to a phone number
        
        Args:
            phone_number: Recipient's phone number (with country code, e.g., 919876543210)
            message: Message text to send
            
        Returns:
            dict: {'success': True/False, 'message': 'Status message'}
        """
        if not self.enabled:
            logger.info(f"WhatsApp message not sent (disabled): {phone_number}")
            return {'success': False, 'message': 'WhatsApp messaging is disabled'}
        
        if not self.instance_id or not self.token:
            logger.error("WhatsApp credentials not configured")
            return {'success': False, 'message': 'WhatsApp credentials not configured'}
        
        # Clean phone number (remove spaces, +, -, etc.)
        clean_number = ''.join(filter(str.isdigit, phone_number))
        
        # Add India country code if not present
        if not clean_number.startswith('91') and len(clean_number) == 10:
            clean_number = '91' + clean_number
        
        try:
            # UltraMsg send message API
            url = f"{self.base_url}/{self.instance_id}/messages/chat"
            
            payload = {
                'token': self.token,
                'to': clean_number,
                'body': message
            }
            
            response = requests.post(url, data=payload, timeout=10)
            result = response.json()
            
            if result.get('sent') == 'true':
                logger.info(f"WhatsApp message sent successfully to {clean_number}")
                return {'success': True, 'message': 'Message sent successfully'}
            else:
                error_msg = result.get('error', 'Unknown error')
                logger.error(f"WhatsApp send failed: {error_msg}")
                return {'success': False, 'message': f'Failed: {error_msg}'}
                
        except requests.exceptions.Timeout:
            logger.error("WhatsApp API timeout")
            return {'success': False, 'message': 'Request timeout'}
        except requests.exceptions.RequestException as e:
            logger.error(f"WhatsApp API error: {str(e)}")
            return {'success': False, 'message': f'Network error: {str(e)}'}
        except Exception as e:
            logger.error(f"Unexpected error sending WhatsApp: {str(e)}")
            return {'success': False, 'message': f'Error: {str(e)}'}
    
    def send_service_request_confirmation(self, customer_name, phone, service_type, ac_type, request_id):
        """
        Send service request confirmation message
        
        Args:
            customer_name: Customer's name
            phone: Phone number
            service_type: Type of service requested
            ac_type: AC type
            request_id: Service request ID
        """
        message = self._get_service_request_template(
            customer_name, service_type, ac_type, request_id
        )
        return self.send_message(phone, message)
    
    def send_contact_confirmation(self, customer_name, phone, service_type, message_id):
        """
        Send contact form confirmation message
        
        Args:
            customer_name: Customer's name
            phone: Phone number
            service_type: Service type interested in
            message_id: Contact message ID
        """
        message = self._get_contact_template(
            customer_name, service_type, message_id
        )
        return self.send_message(phone, message)
    
    def _get_service_request_template(self, name, service_type, ac_type, request_id):
        """Professional service request confirmation template"""
        
        # Service type display names
        service_names = {
            'installation': 'Installation',
            'repair': 'Repair',
            'gas': 'Gas Refilling',
            'amc': 'AMC (Annual Maintenance)',
            'pcb': 'PCB Repair',
            'buy': 'New AC Purchase',
            'rent': 'AC Rental',
            'cleaning': 'Deep Cleaning',
            'servicing': 'Servicing'
        }
        
        service_display = service_names.get(service_type, service_type.title())
        
        message = f"""
✅ *Request Confirmed - Ansh Air Cool*

Dear {name},

Your service request has been received successfully!

📋 *Request Details:*
━━━━━━━━━━━━━━━━
🔹 Request ID: #{request_id}
🔹 Service: {service_display}
🔹 AC Type: {ac_type}
━━━━━━━━━━━━━━━━

👨‍🔧 *Next Steps:*
• Our team will review your request
• A technician will contact you within 2-4 hours
• Service appointment will be scheduled as per your preference

📞 *Need Immediate Help?*
Call us: +91 9819104977
WhatsApp: +91 9819104977

🌐 *Visit Us:* anshaircool.com

Thank you for choosing Ansh Air Cool!
⭐ Mumbai's Trusted AC Service Provider
"""
        return message.strip()
    
    def _get_contact_template(self, name, service_type, message_id):
        """Professional contact form confirmation template"""
        
        service_names = {
            'installation': 'Installation',
            'repair': 'Repair',
            'gas': 'Gas Refilling',
            'amc': 'AMC (Annual Maintenance)',
            'pcb': 'PCB Repair',
            'buy': 'New AC Purchase',
            'rent': 'AC Rental',
            'cleaning': 'Deep Cleaning',
            'servicing': 'Servicing'
        }
        
        service_display = service_names.get(service_type, service_type.title())
        
        message = f"""
✅ *Thank You - Ansh Air Cool*

Dear {name},

Thank you for contacting us!

📋 *Your Inquiry:*
━━━━━━━━━━━━━━━━
🔹 Service: {service_display}
🔹 Reference ID: #{message_id}
━━━━━━━━━━━━━━━━

📞 Our team will get back to you within 2-4 hours during business hours (9 AM - 8 PM).

*For Urgent Assistance:*
📱 Call: +91 9819104977
💬 WhatsApp: +91 9819104977

🌐 Website: anshaircool.com

Best Regards,
*Ansh Air Cool Team*
❄️ Cool Solutions, Happy Customers!
"""
        return message.strip()


# Create singleton instance
whatsapp_service = WhatsAppService()


def send_whatsapp_service_confirmation(customer_name, phone, service_type, ac_type, request_id):
    """
    Helper function to send service request confirmation
    
    Usage:
        send_whatsapp_service_confirmation("John", "9876543210", "installation", "Split", 123)
    """
    return whatsapp_service.send_service_request_confirmation(
        customer_name, phone, service_type, ac_type, request_id
    )


def send_whatsapp_contact_confirmation(customer_name, phone, service_type, message_id):
    """
    Helper function to send contact form confirmation
    
    Usage:
        send_whatsapp_contact_confirmation("John", "9876543210", "installation", 456)
    """
    return whatsapp_service.send_contact_confirmation(
        customer_name, phone, service_type, message_id
    )
