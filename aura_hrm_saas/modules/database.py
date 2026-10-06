import sqlite3
import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'databases')

def get_db_connection(db_name):
    """Get database connection"""
    os.makedirs(DB_PATH, exist_ok=True)
    return sqlite3.connect(os.path.join(DB_PATH, db_name))

def ensure_company_id_column(conn, table_name):
    """Helper to ensure company_id column exists for multi-tenancy"""
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    if 'company_id' not in columns:
        try:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN company_id INTEGER DEFAULT 1")
            conn.commit()
        except Exception as e:
            print(f"Migration notice for {table_name}: {e}")

def init_all_dbs():
    """Initialize all databases for AuraToolKit 360 B2B Multi-Tenant Platform"""
    os.makedirs(DB_PATH, exist_ok=True)
    
    print("=" * 50)
    print("[OK] Initializing AuraToolKit 360 B2B Multi-Tenant Databases...")
    print("=" * 50)
    
    # Companies database (Central Tenant Registry)
    conn = get_db_connection('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        domain TEXT,
        email TEXT,
        phone TEXT,
        plan TEXT DEFAULT 'pro',
        max_employees INTEGER DEFAULT 100,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    # Default B2B Company
    c.execute('''INSERT OR IGNORE INTO companies (id, name, slug, domain, email, phone, plan, max_employees, status)
                 VALUES (1, 'AuraToolKit 360 Inc', 'auratoolkit-360', 'auratoolkit360.com', 'admin@auratoolkit360.com', '0300-0000000', 'enterprise', 500, 'active')''')
    conn.commit()
    conn.close()
    print("[OK] Companies registry ready!")

    # Candidates database
    conn = get_db_connection('candidates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        filename TEXT,
        location TEXT,
        received_date TEXT,
        score INTEGER,
        matched_keywords TEXT,
        status TEXT DEFAULT 'pending',
        job_title TEXT,
        applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    ensure_company_id_column(conn, 'candidates')
    conn.commit()
    conn.close()
    print("[OK] Candidates database ready!")
    
    # Employees database
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        name TEXT,
        email TEXT,
        phone TEXT,
        position TEXT,
        department TEXT,
        joining_date TEXT,
        salary TEXT,
        petrol_allowance TEXT DEFAULT '0',
        location TEXT,
        cv_filename TEXT,
        employee_type TEXT DEFAULT 'Probation',
        status TEXT DEFAULT 'active',
        cnic TEXT,
        bank_name TEXT,
        account_number TEXT,
        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    ensure_company_id_column(conn, 'employees')
    default_employees = [
        (1, 'Senior Developer', 'developer@auratoolkit360.com', '0311-0000000', 'Developer', 'Web Team', '2024-01-01', '50000', '5000', 'Karachi', '', 'Permanent', 'active', '12345-1234567-1', 'Bank A', '1234567890'),
        (2, 'Bilal Ahmed', 'bilal@auratoolkit360.com', '0311-0000001', 'Developer', 'App Team', '2024-01-01', '48000', '4500', 'Lahore', '', 'Permanent', 'active', '12345-1234567-2', 'Bank B', '0987654321')
    ]
    for emp in default_employees:
        c.execute('''INSERT OR IGNORE INTO employees (id, name, email, phone, position, department, joining_date, salary, petrol_allowance, location, cv_filename, employee_type, status, cnic, bank_name, account_number)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', emp)
    conn.commit()
    conn.close()
    print("[OK] Employees database ready!")

    # Attendance database
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        employee_id INTEGER,
        employee_name TEXT,
        team TEXT,
        date TEXT,
        check_in TEXT,
        check_out TEXT,
        status TEXT DEFAULT 'Present',
        late_minutes INTEGER DEFAULT 0,
        overtime_minutes INTEGER DEFAULT 0,
        working_hours REAL DEFAULT 0,
        remarks TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    ensure_company_id_column(conn, 'attendance')
    c.execute('''CREATE TABLE IF NOT EXISTS holidays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        date TEXT,
        name TEXT,
        year TEXT
    )''')
    ensure_company_id_column(conn, 'holidays')
    c.execute('''CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        employee_id INTEGER,
        employee_name TEXT,
        team TEXT,
        from_date TEXT,
        to_date TEXT,
        leave_type TEXT DEFAULT 'Leave',
        reason TEXT,
        status TEXT DEFAULT 'Pending',
        applied_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        approved_by TEXT,
        approved_on TIMESTAMP
    )''')
    ensure_company_id_column(conn, 'leave_requests')
    conn.commit()
    conn.close()
    print("[OK] Attendance database ready!")
    
    # Inventory database
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
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
    ensure_company_id_column(conn, 'assets')
    c.execute('''CREATE TABLE IF NOT EXISTS asset_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        category_name TEXT
    )''')
    ensure_company_id_column(conn, 'asset_categories')
    default_cats = ['Laptop', 'Desktop', 'Monitor', 'Mouse', 'Keyboard', 'Headphone', 
                    'Access Card', 'Dongle', 'WiFi Device', 'Chair', 'Table', 'Locker']
    for cat in default_cats:
        c.execute("SELECT COUNT(*) FROM asset_categories WHERE category_name = ?", (cat,))
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO asset_categories (company_id, category_name) VALUES (1, ?)", (cat,))
    conn.commit()
    conn.close()
    print("[OK] Inventory database ready!")
    
    # Payroll database
    conn = get_db_connection('payroll.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS payroll (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
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
    ensure_company_id_column(conn, 'payroll')
    conn.commit()
    conn.close()
    print("[OK] Payroll database ready!")
    
    # Weekend database
    conn = get_db_connection('weekend.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS weekend (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        employee_id INTEGER,
        employee_name TEXT,
        team TEXT,
        weekend_count INTEGER DEFAULT 0,
        month TEXT,
        year TEXT,
        amount DECIMAL DEFAULT 0,
        status TEXT DEFAULT 'Pending',
        added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    ensure_company_id_column(conn, 'weekend')
    conn.commit()
    conn.close()
    print("[OK] Weekend database ready!")
    
    # Activity Logs database
    conn = get_db_connection('activity_logs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS activity_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        user TEXT,
        action TEXT,
        details TEXT,
        ip_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    ensure_company_id_column(conn, 'activity_logs')
    conn.commit()
    conn.close()
    print("[OK] Activity Logs database ready!")
    
    # Users database (5 tenant roles + 1 super_admin role)
    conn = get_db_connection('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        employee_id INTEGER,
        role TEXT DEFAULT 'employee',
        department TEXT,
        is_active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    ensure_company_id_column(conn, 'users')
    
    # Insert default users (Super Admin + Tenant Users)
    default_users = [
        (1, 'superadmin', generate_password_hash('admin123'), 'Platform Super Admin', 'superadmin@auratoolkit360.com', 0, 'super_admin', 'Platform'),
        (1, 'admin', generate_password_hash('admin123'), 'System Administrator', 'admin@auratoolkit360.com', 0, 'admin', 'IT'),
        (1, 'hr_manager', generate_password_hash('hr123'), 'HR Manager', 'hr@auratoolkit360.com', 0, 'hr_manager', 'HR'),
        (1, 'accountant', generate_password_hash('acc123'), 'Accountant', 'accountant@auratoolkit360.com', 0, 'accountant', 'Finance'),
        (1, 'management', generate_password_hash('mgmt123'), 'Management User', 'management@auratoolkit360.com', 0, 'management', 'Management'),
        (1, 'employee1', generate_password_hash('emp123'), 'Senior Developer', 'developer@auratoolkit360.com', 1, 'employee', 'Web Team'),
        (1, 'employee2', generate_password_hash('emp123'), 'Bilal Ahmed', 'bilal@auratoolkit360.com', 2, 'employee', 'App Team')
    ]
    
    for user in default_users:
        c.execute("INSERT OR IGNORE INTO users (company_id, username, password, full_name, email, employee_id, role, department) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", user)
    
    # Create roles, permissions and role_permissions tables (if not present)
    c.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS role_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER,
            permission TEXT,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
    ''')
    c.execute("DELETE FROM role_permissions WHERE role_id IN (SELECT id FROM roles WHERE name IN ('super_admin','admin','hr_manager','accountant','management','employee'))")

    # Default roles
    default_roles = [
        ('super_admin', 'Super Administrator - Full Platform Access'),
        ('admin', 'Tenant Administrator - Full Access within Company'),
        ('hr_manager', 'HR Manager - Employee and ATS Management'),
        ('accountant', 'Accountant - Payroll and Finance'),
        ('management', 'Management - Reports and Approvals'),
        ('employee', 'Employee - Basic Access')
    ]
    for role_name, role_desc in default_roles:
        c.execute("INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)", (role_name, role_desc))

    # Get admin role id
    c.execute("SELECT id FROM roles WHERE name = 'admin'")
    admin_row = c.fetchone()
    admin_id = admin_row[0] if admin_row else None

    # Permissions list
    permissions = [
        'view_ats','edit_ats',
        'view_employees','edit_employees','delete_employees',
        'view_inventory','edit_inventory','delete_inventory',
        'view_payroll','edit_payroll','delete_payroll',
        'view_weekend','edit_weekend',
        'view_attendance','edit_attendance',
        'view_increment','edit_increment','approve_increment',
        'view_users','edit_users','delete_users',
        'view_logs','clear_logs',
        'approve_requests'
    ]
    for perm in permissions:
        c.execute("INSERT OR IGNORE INTO permissions (name, description) VALUES (?, ?)", (perm, perm.replace('_', ' ').title()))
        if admin_id:
            c.execute("INSERT OR IGNORE INTO role_permissions (role_id, permission) VALUES (?, ?)", (admin_id, perm))

    # Assign sensible defaults for other roles
    # HR Manager: broad edit rights across HR/ATS/payroll/inventory, but cannot delete users
    c.execute("SELECT id FROM roles WHERE name = 'hr_manager'")
    hr_row = c.fetchone()
    hr_id = hr_row[0] if hr_row else None
    hr_perms = [
        'view_ats','edit_ats',
        'view_employees','edit_employees','delete_employees',
        'view_inventory','edit_inventory','delete_inventory',
        'view_payroll','edit_payroll','delete_payroll',
        'view_weekend','edit_weekend',
        'view_attendance','edit_attendance',
        'view_increment','edit_increment','approve_increment',
        'view_users','edit_users',
        'view_logs','clear_logs',
        'approve_requests'
    ]
    if hr_id:
        for p in hr_perms:
            c.execute("INSERT OR IGNORE INTO role_permissions (role_id, permission) VALUES (?, ?)", (hr_id, p))

    # Accountant: payroll, attendance, weekend sheet access
    c.execute("SELECT id FROM roles WHERE name = 'accountant'")
    acc_row = c.fetchone()
    acc_id = acc_row[0] if acc_row else None
    acc_perms = ['view_payroll','edit_payroll','view_weekend','edit_weekend','view_attendance','edit_attendance','view_employees']
    if acc_id:
        for p in acc_perms:
            c.execute("INSERT OR IGNORE INTO role_permissions (role_id, permission) VALUES (?, ?)", (acc_id, p))

    # Management: view employees/inventory, can approve requests/increments, but no editing or ATS access
    c.execute("SELECT id FROM roles WHERE name = 'management'")
    mgmt_row = c.fetchone()
    mgmt_id = mgmt_row[0] if mgmt_row else None
    mgmt_perms = ['view_employees','view_inventory','approve_increment','approve_requests']
    if mgmt_id:
        for p in mgmt_perms:
            c.execute("INSERT OR IGNORE INTO role_permissions (role_id, permission) VALUES (?, ?)", (mgmt_id, p))

    # Employee: self-service minimal perms (none needed here since UI handles employee role specially)
    
    # Deduplicate role_permissions: create unique-versioned table and replace
    c.execute('''
        CREATE TABLE IF NOT EXISTS role_permissions_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER,
            permission TEXT,
            UNIQUE(role_id, permission)
        )
    ''')
    c.execute('INSERT OR IGNORE INTO role_permissions_new (role_id, permission) SELECT DISTINCT role_id, permission FROM role_permissions')
    c.execute('DROP TABLE role_permissions')
    c.execute('ALTER TABLE role_permissions_new RENAME TO role_permissions')

    conn.commit()
    conn.close()
    print("[OK] Users database ready with Super Admin and tenant roles!")
    
    # Requests database
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        employee_id INTEGER,
        employee_name TEXT,
        request_type TEXT,
        subject TEXT,
        description TEXT,
        start_date TEXT,
        end_date TEXT,
        status TEXT DEFAULT 'pending',
        reviewer_id INTEGER,
        reviewer_name TEXT,
        reviewer_remarks TEXT,
        reviewed_date TEXT,
        submitted_date TEXT
    )''')
    ensure_company_id_column(conn, 'requests')
    conn.commit()
    conn.close()
    print("[OK] Requests database ready!")

    # Increment database
    conn = get_db_connection('increment.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS increments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER DEFAULT 1,
        employee_id INTEGER,
        employee_name TEXT,
        team TEXT,
        current_salary DECIMAL DEFAULT 0,
        increment_percent DECIMAL DEFAULT 0,
        new_salary DECIMAL DEFAULT 0,
        last_increment_date TEXT,
        next_increment_date TEXT,
        effective_date TEXT,
        reason TEXT,
        status TEXT DEFAULT 'pending',
        approved_by TEXT,
        approved_date TEXT,
        remarks TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    ensure_company_id_column(conn, 'increments')
    conn.commit()
    conn.close()
    print("[OK] Increment database ready!")
    
    print("=" * 50)
    print("[OK] ALL DATABASES INITIALIZED SUCCESSFULLY!")
    print("=" * 50)