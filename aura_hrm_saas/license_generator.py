"""
AuraToolKit 360 - Master License Key Generator
Author: Ali Raza Bhatti / AuraToolKit 360 Team
Use this tool to generate authentic, tamper-proof license activation keys
for SaaS clients purchasing an AuraHR Desktop / On-Premise subscription.
"""

import sys
import os
import argparse
import random
import string
from datetime import datetime, timedelta

# Ensure parent path is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from license_manager import pack_license_key, unpack_and_verify_key


def generate_random_serial(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_license_key(company: str, plan: str = "PRO", days: int = 365, max_employees: int = 100):
    """
    Generate a signed cryptographic license key string.
    days = 0 means lifetime license.
    max_employees = 0 means unlimited employees.
    """
    today = datetime.now()
    if days == 0:
        expiry_str = "lifetime"
        period_desc = "Lifetime Access"
    else:
        expiry_dt = today + timedelta(days=days)
        expiry_str = expiry_dt.strftime("%Y-%m-%d")
        period_desc = f"{days} Days (Valid until {expiry_str})"

    payload = {
        "company": company.strip(),
        "plan": plan.upper().strip(),
        "issued_at": today.strftime("%Y-%m-%d"),
        "expires_at": expiry_str,
        "max_employees": "Unlimited" if max_employees <= 0 else max_employees,
        "serial": generate_random_serial(),
        "features": ["employees", "attendance", "biometric_sync", "ats", "payroll", "increment_sheet", "inventory"]
    }

    key_str = pack_license_key(payload)
    
    # Self-verify to ensure 100% validity
    is_valid, check = unpack_and_verify_key(key_str)
    if not is_valid:
        raise ValueError(f"Self-verification failed: {check}")

    return key_str, payload, period_desc


def format_customer_message(key_str: str, payload: dict, period_desc: str) -> str:
    msg = f"""
==============================================================
*** AuraHR Enterprise -- Official License Key ***
==============================================================
Client / Company:  {payload['company']}
Subscription Plan: {payload['plan']} Edition
Validity Period:   {period_desc}
Max Employees:     {payload['max_employees']}
Issue Date:        {payload['issued_at']}
Serial Number:     {payload['serial']}
--------------------------------------------------------------
YOUR ACTIVATION KEY:
{key_str}
--------------------------------------------------------------
ACTIVATION INSTRUCTIONS:
1. Open AuraHR Desktop on your PC.
2. Go to the Activation screen (or click 'License' in top bar).
3. Paste the activation key above and click 'Activate Now'.
4. Enjoy unlimited full access to AuraHR Enterprise!

Official Support: https://auratoolkit360.com
==============================================================
"""
    return msg


def main():
    parser = argparse.ArgumentParser(description="Generate AuraHR Enterprise License Activation Keys")
    parser.add_argument("--company", "-c", type=str, help="Client or Company Name")
    parser.add_argument("--plan", "-p", type=str, default="PRO", choices=["STARTER", "PRO", "ENTERPRISE", "TRIAL"], help="Subscription plan tier")
    parser.add_argument("--days", "-d", type=int, default=365, help="Validity in days (0 for lifetime)")
    parser.add_argument("--employees", "-e", type=int, default=100, help="Max employee limit (0 for unlimited)")
    
    args = parser.parse_args()

    company = args.company
    if not company:
        print("\n" + "="*50)
        print("*** AuraHR Enterprise -- License Key Generator ***")
        print("="*50)
        company = input("Enter Company Name [e.g. WebBugs Tech]: ").strip()
        if not company:
            company = "Demo Client Inc"
        
        plan_input = input("Enter Plan (starter / pro / enterprise) [Default: pro]: ").strip().upper()
        plan = plan_input if plan_input in ["STARTER", "PRO", "ENTERPRISE", "TRIAL"] else "PRO"
        
        days_str = input("Validity in days (30 / 90 / 365 / 0 for lifetime) [Default: 365]: ").strip()
        days = int(days_str) if days_str.isdigit() else 365

        emp_str = input("Max Employees (50 / 200 / 0 for unlimited) [Default: 100]: ").strip()
        employees = int(emp_str) if emp_str.isdigit() else 100
    else:
        plan = args.plan
        days = args.days
        employees = args.employees

    key_str, payload, period_desc = create_license_key(company, plan, days, employees)
    message = format_customer_message(key_str, payload, period_desc)
    print(message)


if __name__ == "__main__":
    main()
