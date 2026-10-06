"""
AuraToolKit 360 - Enterprise SaaS License & Subscription Manager
Handles cryptographic license verification, 14-day free trial tracking,
and machine-level licensing for on-premise desktop deployment.
"""

import os
import sys
import json
import time
import base64
import hmac
import hashlib
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASES_DIR = os.path.join(BASE_DIR, 'databases')
LICENSE_FILE = os.path.join(DATABASES_DIR, 'license_store.json')

# Master HMAC secret for signing and verifying tamper-proof licenses
MASTER_SECRET = b"AURA_TOOLKIT_360_ENTERPRISE_MASTER_KEY_2026_X92J_SECURE"
DEFAULT_TRIAL_DAYS = 14


def _ensure_db_dir():
    os.makedirs(DATABASES_DIR, exist_ok=True)


def _load_license_store():
    """Load raw store from disk or initialize default state."""
    _ensure_db_dir()
    if not os.path.exists(LICENSE_FILE):
        default_data = {
            "first_run_timestamp": int(time.time()),
            "first_run_date": datetime.now().strftime("%Y-%m-%d"),
            "trial_days": DEFAULT_TRIAL_DAYS,
            "activated_key": None,
            "license_payload": None,
            "last_clock_check": int(time.time())
        }
        _save_license_store(default_data)
        return default_data

    try:
        with open(LICENSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # If corrupted, preserve first run date if possible
        return {
            "first_run_timestamp": int(time.time()),
            "first_run_date": datetime.now().strftime("%Y-%m-%d"),
            "trial_days": DEFAULT_TRIAL_DAYS,
            "activated_key": None,
            "license_payload": None,
            "last_clock_check": int(time.time())
        }


def _save_license_store(data):
    """Save raw store atomically."""
    _ensure_db_dir()
    temp_file = LICENSE_FILE + ".tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    if os.path.exists(LICENSE_FILE):
        os.remove(LICENSE_FILE)
    os.rename(temp_file, LICENSE_FILE)


def generate_signature(payload_bytes: bytes) -> str:
    """Generate truncated HMAC-SHA256 signature (24 chars)"""
    sig = hmac.new(MASTER_SECRET, payload_bytes, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sig).decode("ascii").rstrip("=")[:24]


def pack_license_key(payload: dict) -> str:
    """
    Packs payload dict into a formatted license string:
    AURA-<PLAN>-<ENCODED_DATA>.<SIGNATURE>
    """
    canonical_json = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')
    data_b64 = base64.urlsafe_b64encode(canonical_json).decode('ascii').rstrip("=")
    sig = generate_signature(canonical_json)
    plan_code = payload.get("plan", "PRO").upper()
    return f"AURA-{plan_code}-{data_b64}.{sig}"


def unpack_and_verify_key(key_str: str):
    """
    Unpacks and verifies license key signature.
    Returns (True, payload_dict) or (False, error_message).
    """
    if not key_str or not isinstance(key_str, str):
        return False, "Invalid key format."

    clean_key = key_str.strip()
    if not clean_key.startswith("AURA-"):
        return False, "Key must start with AURA- prefix."

    parts = clean_key.split("-", 2)
    if len(parts) < 3:
        return False, "Malformed license key structure."

    body_and_sig = parts[2]
    if "." not in body_and_sig:
        return False, "Missing signature in license key."

    data_b64, sig = body_and_sig.split(".", 1)

    # Pad base64 string
    padding = len(data_b64) % 4
    if padding:
        data_b64 += "=" * (4 - padding)

    try:
        raw_json_bytes = base64.urlsafe_b64decode(data_b64.encode('ascii'))
        expected_sig = generate_signature(raw_json_bytes)
        if not hmac.compare_digest(sig, expected_sig):
            return False, "Invalid signature: License key is forged or corrupted."

        payload = json.loads(raw_json_bytes.decode('utf-8'))
        return True, payload
    except Exception as e:
        return False, f"License parsing error: {str(e)}"


def activate_license(key_str: str):
    """
    Validates and activates a new license key on this machine.
    Returns (True, message) or (False, error_message).
    """
    is_valid_sig, result = unpack_and_verify_key(key_str)
    if not is_valid_sig:
        return False, result

    payload = result
    expiry_str = payload.get("expires_at")
    
    if expiry_str != "lifetime":
        try:
            expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
            if datetime.now() > expiry_date:
                return False, f"This license key expired on {expiry_str}."
        except ValueError:
            return False, "Invalid expiration date format in license."

    store = _load_license_store()
    store["activated_key"] = key_str.strip()
    store["license_payload"] = payload
    store["last_clock_check"] = int(time.time())
    _save_license_store(store)

    company = payload.get("company", "Company")
    plan = payload.get("plan", "PRO").upper()
    return True, f"Successfully activated {plan} license for {company}!"


def remove_license():
    """Reset to trial or unlicensed mode."""
    store = _load_license_store()
    store["activated_key"] = None
    store["license_payload"] = None
    _save_license_store(store)
    return True


def get_license_info():
    """
    Evaluates current system license state.
    Returns structured dict with status, validity, and details.
    """
    store = _load_license_store()
    now_ts = int(time.time())
    today = datetime.now()

    # Clock rollback detection (allow 10 min drift)
    last_check = store.get("last_clock_check", now_ts)
    if now_ts < (last_check - 600):
        return {
            "is_valid": False,
            "status": "clock_tampered",
            "message": "System clock rollback detected. Please correct your system date.",
            "plan": "LOCKED",
            "company": "System Clock Error",
            "days_remaining": 0,
            "expiry_date": "N/A"
        }

    # Update clock check
    store["last_clock_check"] = now_ts

    # 1. Check if an activated license exists
    activated_key = store.get("activated_key")
    payload = store.get("license_payload")

    if activated_key and payload:
        is_valid_sig, check_payload = unpack_and_verify_key(activated_key)
        if not is_valid_sig:
            return {
                "is_valid": False,
                "status": "invalid_key",
                "message": "License key validation failed.",
                "plan": "INVALID",
                "company": "Tampered",
                "days_remaining": 0,
                "expiry_date": "N/A"
            }

        expiry_str = payload.get("expires_at", "2026-01-01")
        company = payload.get("company", "Licensed Client")
        plan = payload.get("plan", "PRO").upper()
        max_employees = payload.get("max_employees", "Unlimited")

        if expiry_str == "lifetime":
            return {
                "is_valid": True,
                "status": "active_lifetime",
                "message": f"Active Lifetime {plan} License",
                "plan": plan,
                "company": company,
                "days_remaining": 99999,
                "expiry_date": "Lifetime",
                "max_employees": max_employees,
                "is_trial": False
            }

        try:
            expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
            remaining_days = (expiry_date - today).days + 1
            if remaining_days > 0:
                return {
                    "is_valid": True,
                    "status": "active",
                    "message": f"Active {plan} License ({remaining_days} days remaining)",
                    "plan": plan,
                    "company": company,
                    "days_remaining": remaining_days,
                    "expiry_date": expiry_str,
                    "max_employees": max_employees,
                    "is_trial": False
                }
            else:
                return {
                    "is_valid": False,
                    "status": "expired",
                    "message": f"Subscription expired on {expiry_str}. Please renew your plan.",
                    "plan": plan,
                    "company": company,
                    "days_remaining": 0,
                    "expiry_date": expiry_str,
                    "max_employees": max_employees,
                    "is_trial": False
                }
        except ValueError:
            pass

    # 2. Check 14-Day Free Trial
    first_run_ts = store.get("first_run_timestamp", now_ts)
    trial_days = store.get("trial_days", DEFAULT_TRIAL_DAYS)
    first_run_dt = datetime.fromtimestamp(first_run_ts)
    trial_expiry_dt = first_run_dt + timedelta(days=trial_days)
    remaining_trial_days = (trial_expiry_dt - today).days + 1

    if remaining_trial_days > 0:
        return {
            "is_valid": True,
            "status": "trial",
            "message": f"Enterprise 14-Day Free Trial ({remaining_trial_days} days remaining)",
            "plan": "TRIAL",
            "company": "Evaluation Client",
            "days_remaining": remaining_trial_days,
            "expiry_date": trial_expiry_dt.strftime("%Y-%m-%d"),
            "max_employees": 50,
            "is_trial": True
        }
    else:
        return {
            "is_valid": False,
            "status": "trial_expired",
            "message": "Your 14-day free trial has expired. Enter an activation key to continue.",
            "plan": "TRIAL_EXPIRED",
            "company": "Evaluation Client",
            "days_remaining": 0,
            "expiry_date": trial_expiry_dt.strftime("%Y-%m-%d"),
            "max_employees": 0,
            "is_trial": True
        }


def is_license_valid():
    """Convenient boolean check for middleware guards."""
    info = get_license_info()
    return info.get("is_valid", False)
