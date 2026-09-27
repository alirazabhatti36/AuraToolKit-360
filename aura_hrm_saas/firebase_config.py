"""
AuraToolKit 360 Enterprise HR & ATS SaaS
Firebase Configuration, Firestore Multi-Tenant Manager & SDK Initialization
"""
import os
import json

# Client-Side Firebase SDK Configuration (for browser templates)
FIREBASE_CONFIG = {
    "apiKey": os.environ.get("FIREBASE_API_KEY", "AIzaSyAuraToolKit360PlaceholderApiKey"),
    "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN", "auratoolkit360.firebaseapp.com"),
    "projectId": os.environ.get("FIREBASE_PROJECT_ID", "auratoolkit360"),
    "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET", "auratoolkit360.appspot.com"),
    "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID", "123456789012"),
    "appId": os.environ.get("FIREBASE_APP_ID", "1:123456789012:web:abcdef1234567890")
}

_firestore_client = None
_firebase_initialized = False

def get_firebase_config():
    """Return Firebase client side config for Jinja2 templates"""
    return FIREBASE_CONFIG

def get_credentials_path():
    """Locate firebase service account json file"""
    custom_path = os.environ.get("FIREBASE_CREDENTIALS_PATH")
    if custom_path and os.path.exists(custom_path):
        return custom_path
    
    local_path = os.path.join(os.path.dirname(__file__), 'firebase_credentials.json')
    if os.path.exists(local_path):
        return local_path
    
    return None

def is_firebase_enabled():
    """Check if valid Firebase credentials file or env variable exists"""
    return get_credentials_path() is not None or 'FIREBASE_CREDENTIALS_JSON' in os.environ

def init_firebase_admin():
    """
    Initialize Firebase Admin SDK with graceful fallback.
    Returns Firestore client instance if enabled, otherwise None.
    """
    global _firestore_client, _firebase_initialized
    
    if _firestore_client is not None:
        return _firestore_client
        
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError:
        # firebase-admin not installed; fallback to SQLite
        return None

    if not is_firebase_enabled():
        return None

    try:
        if not firebase_admin._apps:
            cred_json_env = os.environ.get("FIREBASE_CREDENTIALS_JSON")
            if cred_json_env:
                cred_dict = json.loads(cred_json_env)
                cred = credentials.Certificate(cred_dict)
            else:
                cred_file = get_credentials_path()
                cred = credentials.Certificate(cred_file)
            firebase_admin.initialize_app(cred)
            
        _firestore_client = firestore.client()
        _firebase_initialized = True
        print("[FIREBASE] Cloud Firestore connected successfully for AuraToolKit 360!")
        return _firestore_client
    except Exception as e:
        print(f"[FIREBASE WARNING] Failed to initialize Firebase Admin SDK: {e}")
        return None

def get_tenant_collection(company_id, collection_name):
    """
    Helper to access multi-tenant isolated sub-collection in Firestore:
    companies/{company_id}/{collection_name}
    """
    db = init_firebase_admin()
    if db is None:
        return None
    return db.collection("companies").document(str(company_id)).collection(collection_name)
