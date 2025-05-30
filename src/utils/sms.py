import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# In a production environment, these would be environment variables
# For demo purposes, we'll use placeholder values
TWILIO_ACCOUNT_SID = "AC_DEMO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "DEMO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "+15555555555"  # Demo Twilio number

def send_inventory_notification(to_phone, low_stock_items, out_of_stock_items, check_date):
    """
    Send SMS notification about inventory status
    
    Args:
        to_phone (str): Phone number to send the notification to
        low_stock_items (list): List of items that are low in stock
        out_of_stock_items (list): List of items that are out of stock
        check_date (datetime): Date and time of the inventory check
    
    Returns:
        dict: Result of the SMS sending operation
    """
    try:
        # Format the message
        message_parts = []
        message_parts.append(f"Restaurant Inventory Alert - {check_date.strftime('%m/%d/%Y %H:%M')}")
        
        if out_of_stock_items:
            message_parts.append("\nOUT OF STOCK:")
            for item in out_of_stock_items:
                message_parts.append(f"- {item.name}")
        
        if low_stock_items:
            message_parts.append("\nLOW STOCK:")
            for item in low_stock_items:
                message_parts.append(f"- {item.name}")
        
        if not low_stock_items and not out_of_stock_items:
            message_parts.append("\nAll inventory items are well stocked.")
        
        message_body = "\n".join(message_parts)
        
        # In a production environment, this would use actual Twilio credentials
        # For demo purposes, we'll simulate the SMS sending
        
        # Uncomment this code and add real credentials when deploying to production
        """
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        """
        
        # For demo, return success without actually sending SMS
        return {
            'success': True,
            'message': f"SMS would be sent to {to_phone} in production environment"
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': str(e)
        }
