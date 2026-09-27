import sqlite3
import os

DB_PATH = 'databases/'

def get_db_connection(db_name):
    """Get database connection"""
    os.makedirs(DB_PATH, exist_ok=True)
    return sqlite3.connect(os.path.join(DB_PATH, db_name))

def init_all_dbs():
    """Initialize all databases"""
    os.makedirs(DB_PATH, exist_ok=True)
    
    print("=" * 50)
    print("📀 Initializing All Databases...")
    print("=" * 50)
    
    # Candidates database
    conn = get_db_connection('candidates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        location TEXT,
        received_date TEXT,
        score INTEGER,
        matched_keywords TEXT,
        status TEXT DEFAULT 'pending',
        job_title TEXT,
        applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()
    print("✅ Candidates database ready!")
    
    # Employees database
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        position TEXT,
        department TEXT,
        joining_date TEXT,
        salary TEXT,
        location TEXT,
        cv_filename TEXT,
        employee_type TEXT DEFAULT 'Probation',
        status TEXT DEFAULT 'active',
        cnic TEXT,
        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()
    print("✅ Employees database ready!")
    
    # Inventory database
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_name TEXT,
        category TEXT,
        serial_number TEXT,
        brand_model TEXT,
        assigned_to INTEGER,
        assigned_date TEXT,
        status TEXT DEFAULT 'Available',
        purchase_date TEXT,
        warranty_until TEXT,
        cost TEXT,
        remarks TEXT,
        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS asset_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT
    )''')
    default_cats = ['Laptop', 'Desktop', 'Monitor', 'Mouse', 'Keyboard', 'Headphone', 
                    'Access Card', 'Dongle', 'WiFi Device', 'Chair', 'Table', 'Locker']
    for cat in default_cats:
        c.execute("INSERT OR IGNORE INTO asset_categories (category_name) VALUES (?)", (cat,))
    conn.commit()
    conn.close()
    print("✅ Inventory database ready!")
    
    # Payroll database
    conn = get_db_connection('payroll.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS payroll (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        team TEXT,
        employee_name TEXT,
        working_days INTEGER DEFAULT 30,
        basic_salary DECIMAL DEFAULT 0,
        petrol_allowance DECIMAL DEFAULT 0,
        additional_earnings DECIMAL DEFAULT 0,
        gross_salary DECIMAL DEFAULT 0,
        income_tax DECIMAL DEFAULT 0,
        other_deductions DECIMAL DEFAULT 0,
        leaves INTEGER DEFAULT 0,
        net_salary DECIMAL DEFAULT 0,
        bank_salary DECIMAL DEFAULT 0,
        cash_salary DECIMAL DEFAULT 0,
        remarks TEXT,
        bank_name TEXT,
        account_number TEXT,
        month TEXT,
        year TEXT,
        status TEXT DEFAULT 'Pending',
        payment_date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()
    print("✅ Payroll database ready!")
    
    print("=" * 50)
    print("🎉 ALL DATABASES INITIALIZED SUCCESSFULLY!")
    print("=" * 50)