import sqlite3
from functools import wraps
from flask import session, flash, redirect, url_for
from modules.database import get_db_connection
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ============= DECORATORS FOR PERMISSIONS =============

def login_required(f):
    """Decorator to check if user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('⚠️ Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    """Decorator to check if user has specific permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not has_permission(session.get('user_id'), permission):
                flash('🔒 You do not have permission to access this page!', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def role_required(allowed_roles):
    """Decorator to check if user has specific role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('user_role', 'employee')
            if user_role == 'super_admin' or user_role in allowed_roles:
                return f(*args, **kwargs)
            flash('🔒 You do not have permission to access this page!', 'danger')
            return redirect(url_for('dashboard'))
        return decorated_function
    return decorator

def superadmin_required(f):
    """Decorator to check if user is Super Admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or session.get('user_role') != 'super_admin':
            flash('🔒 Super Admin platform privileges required!', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# ============= PERMISSION FUNCTIONS =============

def has_permission(user_id, permission_name):
    """Check if user has a specific permission"""
    if not user_id:
        return False
    
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    
    # Get user's role
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return False
    
    role = user[0]
    if role == 'super_admin':
        conn.close()
        return True
    
    # Check if role has permission
    cursor.execute('''
        SELECT COUNT(*) FROM role_permissions rp
        JOIN roles r ON r.id = rp.role_id
        WHERE r.name = ? AND rp.permission = ?
    ''', (role, permission_name))
    
    count = cursor.fetchone()[0]
    conn.close()
    
    return count > 0


def get_user_permissions(user_id):
    """Get all permissions for a user"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        conn.close()
        return []
    
    role = user[0]
    
    cursor.execute('''
        SELECT rp.permission FROM role_permissions rp
        JOIN roles r ON r.id = rp.role_id
        WHERE r.name = ?
    ''', (role,))
    
    permissions = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return permissions


def get_user_role(user_id):
    """Get user's role"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None


def get_current_employee_id():
    """Get employee_id from session"""
    return session.get('employee_id', 0)


def hash_password(password):
    """Hash password for secure storage"""
    return generate_password_hash(password)


def verify_password(stored_password, provided_password):
    """Verify a stored password hash or legacy plain-text password"""
    if not stored_password or not provided_password:
        return False

    hash_prefixes = ('pbkdf2:', 'scrypt:', 'argon2:', 'bcrypt:', 'sha1:', 'sha256:')
    if any(stored_password.startswith(prefix) for prefix in hash_prefixes):
        return check_password_hash(stored_password, provided_password)

    return stored_password == provided_password


# ============= USER AUTHENTICATION =============

def authenticate_user(username, password):
    """Authenticate user with username or email (case-insensitive) and password and fetch company details"""
    if not username or not password:
        return None
        
    username_clean = username.strip()
    password_clean = password.strip()
    
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, username, password, full_name, email, employee_id, role, department, is_active, company_id 
                      FROM users 
                      WHERE (LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?))''', 
                   (username_clean, username_clean))
    user = cursor.fetchone()
    
    if user and verify_password(user[2], password_clean) and user[8] == 1:
        company_id = user[9] if len(user) > 9 and user[9] else 1
        company_name = "AuraToolKit 360 Inc"
        if user[6] == 'super_admin':
            company_name = "Platform Super Admin"
        else:
            cursor.execute("SELECT name FROM companies WHERE id = ?", (company_id,))
            comp_row = cursor.fetchone()
            if comp_row:
                company_name = comp_row[0]
        conn.close()
        return (user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], company_id, company_name)
    
    conn.close()
    return None

# ============= B2B COMPANY MANAGEMENT =============

def get_all_companies():
    """Get all registered B2B client companies"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, slug, domain, email, phone, plan, max_employees, status, created_at FROM companies ORDER BY id DESC')
    companies = cursor.fetchall()
    conn.close()
    return companies

def get_company_by_id(company_id):
    """Get company by ID"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, slug, domain, email, phone, plan, max_employees, status, created_at FROM companies WHERE id = ?', (company_id,))
    company = cursor.fetchone()
    conn.close()
    return company

def add_company(name, slug, domain, email, phone, plan='pro', max_employees=100, admin_username='', admin_password=''):
    """Add a new B2B company and its tenant admin user"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO companies (name, slug, domain, email, phone, plan, max_employees, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
        ''', (name, slug, domain, email, phone, plan, max_employees))
        company_id = cursor.lastrowid

        # If admin account details provided, create company tenant admin
        if admin_username and admin_password:
            pass_hash = hash_password(admin_password)
            cursor.execute('''
                INSERT INTO users (company_id, username, password, full_name, email, employee_id, role, department, is_active)
                VALUES (?, ?, ?, ?, ?, 0, 'admin', 'Management', 1)
            ''', (company_id, admin_username, pass_hash, f"{name} Admin", email))

        conn.commit()
        conn.close()
        return company_id
    except Exception as e:
        print(f"Error adding company: {e}")
        conn.close()
        return None

def toggle_company_status(company_id):
    """Toggle company active / suspended status"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT status FROM companies WHERE id = ?', (company_id,))
    row = cursor.fetchone()
    if row:
        new_status = 'suspended' if row[0] == 'active' else 'active'
        cursor.execute('UPDATE companies SET status = ? WHERE id = ?', (new_status, company_id))
        conn.commit()
    conn.close()

def get_company_stats():
    """Get global platform SaaS statistics for Super Admin"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM companies')
    total_companies = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM companies WHERE status = 'active'")
    active_companies = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM users WHERE role != 'super_admin'")
    total_users = cursor.fetchone()[0]
    conn.close()

    # Employee count across employees.db
    emp_conn = get_db_connection('employees.db')
    emp_cursor = emp_conn.cursor()
    emp_cursor.execute('SELECT COUNT(*) FROM employees')
    total_employees = emp_cursor.fetchone()[0]
    emp_conn.close()

    return {
        'total_companies': total_companies,
        'active_companies': active_companies,
        'total_users': total_users,
        'total_employees': total_employees
    }


def get_user_by_username(username):
    """Get user by username"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password, full_name, email, employee_id, role, department, is_active FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password, full_name, email, employee_id, role, department, is_active FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


# ============= USER MANAGEMENT =============

def get_all_users():
    """Get all users"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, full_name, email, employee_id, role, department, is_active FROM users ORDER BY id')
    users = cursor.fetchall()
    conn.close()
    return users


def add_user(username, password, full_name, email, employee_id, role, department):
    """Add new user"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    
    # Check if username exists
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False
    
    password_hash = hash_password(password)
    cursor.execute('''
        INSERT INTO users (username, password, full_name, email, employee_id, role, department, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    ''', (username, password_hash, full_name, email, employee_id, role, department))
    conn.commit()
    conn.close()
    return True


def update_user(user_id, full_name, email, role, department, is_active):
    """Update user details"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users 
        SET full_name = ?, email = ?, role = ?, department = ?, is_active = ?
        WHERE id = ?
    ''', (full_name, email, role, department, is_active, user_id))
    conn.commit()
    conn.close()


def delete_user(user_id):
    """Delete user"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()


def change_user_password(user_id, new_password):
    """Change user password"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    password_hash = hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (password_hash, user_id))
    conn.commit()
    conn.close()


# ============= ROLE AND PERMISSION MANAGEMENT =============

def init_permissions():
    """Initialize default roles and permissions"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    
    # Create roles table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT
        )
    ''')
    
    # Create permissions table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            description TEXT
        )
    ''')
    
    # Create role_permissions table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS role_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_id INTEGER,
            permission TEXT,
            FOREIGN KEY (role_id) REFERENCES roles(id)
        )
    ''')
    
    # Default roles
    default_roles = [
        ('admin', 'System Administrator - Full Access'),
        ('hr_manager', 'HR Manager - Employee and ATS Management'),
        ('accountant', 'Accountant - Payroll and Finance'),
        ('management', 'Management - Reports and Approvals'),
        ('employee', 'Employee - Basic Access')
    ]
    
    for role_name, role_desc in default_roles:
        cursor.execute("INSERT OR IGNORE INTO roles (name, description) VALUES (?, ?)", (role_name, role_desc))
    
    # Get admin role id
    cursor.execute("SELECT id FROM roles WHERE name = 'admin'")
    admin_id = cursor.fetchone()[0]
    
    # Permissions list
    permissions = [
        # ATS permissions
        ('view_ats', 'View ATS Dashboard'),
        ('edit_ats', 'Upload/Edit Resumes in ATS'),
        
        # Employee permissions
        ('view_employees', 'View Employee Records'),
        ('edit_employees', 'Add/Edit Employees'),
        ('delete_employees', 'Delete Employees'),
        
        # Inventory permissions
        ('view_inventory', 'View Inventory'),
        ('edit_inventory', 'Add/Edit Assets'),
        ('delete_inventory', 'Delete Assets'),
        
        # Payroll permissions
        ('view_payroll', 'View Payroll'),
        ('edit_payroll', 'Add/Edit Payroll'),
        ('delete_payroll', 'Delete Payroll'),
        
        # Weekend permissions
        ('view_weekend', 'View Weekend Sheet'),
        ('edit_weekend', 'Edit Weekend Sheet'),
        
        # Attendance permissions
        ('view_attendance', 'View Attendance'),
        ('edit_attendance', 'Mark/Edit Attendance'),
        
        # Increment permissions
        ('view_increment', 'View Increment Sheet'),
        ('edit_increment', 'Edit Increment Sheet'),
        ('approve_increment', 'Approve Increment'),
        
        # User permissions
        ('view_users', 'View Users'),
        ('edit_users', 'Add/Edit Users'),
        ('delete_users', 'Delete Users'),
        
        # Log permissions
        ('view_logs', 'View Activity Logs'),
        ('clear_logs', 'Clear Activity Logs')
    ]
    
    # Insert permissions
    for perm_name, perm_desc in permissions:
        cursor.execute("INSERT OR IGNORE INTO permissions (name, description) VALUES (?, ?)", (perm_name, perm_desc))
        cursor.execute("INSERT OR IGNORE INTO role_permissions (role_id, permission) VALUES (?, ?)", (admin_id, perm_name))
    
    conn.commit()
    conn.close()
    print("✅ Permissions initialized successfully")


def add_permission_to_role(role_name, permission_name):
    """Add a permission to a role"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM roles WHERE name = ?", (role_name,))
    role = cursor.fetchone()
    
    if role:
        cursor.execute("INSERT OR IGNORE INTO role_permissions (role_id, permission) VALUES (?, ?)", (role[0], permission_name))
        conn.commit()
    
    conn.close()


def remove_permission_from_role(role_name, permission_name):
    """Remove a permission from a role"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM roles WHERE name = ?", (role_name,))
    role = cursor.fetchone()
    
    if role:
        cursor.execute("DELETE FROM role_permissions WHERE role_id = ? AND permission = ?", (role[0], permission_name))
        conn.commit()
    
    conn.close()


def get_role_permissions(role_name):
    """Get all permissions for a role"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT rp.permission FROM role_permissions rp
        JOIN roles r ON r.id = rp.role_id
        WHERE r.name = ?
    ''', (role_name,))
    
    permissions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return permissions


# ============= DEFAULT ADMIN USER =============

def create_default_admin():
    """Create default admin user if not exists"""
    conn = get_db_connection('users.db')
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (username, password, full_name, email, employee_id, role, department, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('admin', 'admin123', 'System Administrator', 'admin@teamhatch360.com', 0, 'admin', 'Management', 1))
        conn.commit()
        print("✅ Default admin user created: username='admin', password='admin123'")
    
    conn.close()


# ============= RUN INITIALIZATION =============
if __name__ == '__main__':
    init_permissions()
    create_default_admin()