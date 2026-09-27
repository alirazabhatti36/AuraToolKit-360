"""
TeamHatch360 - Automated Notifications Helper Module
Supports WhatsApp Link Generation & Email Alerts for Payslips, Approvals, and Onboarding
"""
import urllib.parse

def generate_whatsapp_payslip_link(employee_name, phone, month, net_salary):
    """Generate a quick WhatsApp click-to-send payslip message link"""
    if not phone:
        return ""
    
    clean_phone = ''.join(filter(str.isdigit, str(phone)))
    if clean_phone.startswith('0'):
        clean_phone = '92' + clean_phone[1:]
    
    message = f"Hello {employee_name},\n\nYour TeamHatch360 Payslip for {month} is ready.\n\nNet Salary: PKR {net_salary:,}\nStatus: Processed\n\nThank you!"
    encoded_message = urllib.parse.quote(message)
    
    return f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"

def generate_whatsapp_approval_link(phone, request_type, status):
    """Generate a quick WhatsApp alert link for request approval/rejection"""
    if not phone:
        return ""
    
    clean_phone = ''.join(filter(str.isdigit, str(phone)))
    if clean_phone.startswith('0'):
        clean_phone = '92' + clean_phone[1:]
        
    message = f"Hello,\n\nYour {request_type} request status has been updated to: {status}.\n\nTeamHatch360 HR System"
    encoded_message = urllib.parse.quote(message)
    
    return f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"
