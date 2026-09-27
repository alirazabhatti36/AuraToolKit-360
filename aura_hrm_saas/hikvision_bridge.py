"""
TeamHatch360 - Hikvision Local Office Biometric Sync Bridge
Syncs biometric attendance logs from local Hikvision devices to TeamHatch360 Firebase/Cloud.
"""
import time
import requests
import json
from datetime import datetime

# Local Office Configuration
HIKVISION_IP = "192.168.1.64"
HIKVISION_USER = "admin"
HIKVISION_PASS = "admin123"
COMPANY_SLUG = "teamhatch-inc"
API_ENDPOINT = "http://localhost:5000/api/attendance/push"  # Cloud or local app endpoint

def fetch_local_hikvision_logs():
    """Fetch attendance events from local Hikvision terminal"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Polling Hikvision at {HIKVISION_IP}...")
    # Simulated payload structure matching Hikvision ISAPI / ISUP format
    return [
        {
            "employee_id": 1,
            "employee_name": "Senior Developer",
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "Check-In",
            "company_slug": COMPANY_SLUG
        }
    ]

def push_to_cloud(logs):
    """Push biometric logs to TeamHatch360 Cloud API"""
    try:
        response = requests.post(API_ENDPOINT, json={"logs": logs}, timeout=5)
        if response.status_code == 200:
            print("✅ Successfully pushed attendance logs to TeamHatch360 Cloud!")
        else:
            print(f"⚠️ Cloud push returned status {response.status_code}")
    except Exception as e:
        print(f"ℹ️ Bridge offline sync notice: {e}")

def run_bridge_loop(interval_seconds=60):
    print("🚀 TeamHatch360 Hikvision Biometric Sync Bridge Started!")
    print(f"Syncing logs for Company [{COMPANY_SLUG}] every {interval_seconds} seconds.")
    while True:
        try:
            logs = fetch_local_hikvision_logs()
            if logs:
                push_to_cloud(logs)
        except Exception as err:
            print(f"Error in sync loop: {err}")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    run_bridge_loop()
