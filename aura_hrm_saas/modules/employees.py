from modules.database import get_db_connection
from flask import session

def get_current_company_id():
    """Helper to get active company_id from session or default to 1"""
    try:
        return session.get('company_id', 1)
    except Exception:
        return 1

def get_all_employees(company_id=None):
    if company_id is None:
        company_id = get_current_company_id()
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute('''SELECT id, name, email, phone, position, department, joining_date, 
                        salary, petrol_allowance, location, cv_filename, employee_type, 
                        status, cnic, bank_name, account_number, company_id 
                 FROM employees WHERE company_id = ? ORDER BY id ASC''', (company_id,))
    employees = c.fetchall()
    conn.close()
    return employees

def get_active_employees(company_id=None):
    if company_id is None:
        company_id = get_current_company_id()
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute('''SELECT id, name, email, phone, position, department, joining_date, 
                        salary, petrol_allowance, location, cv_filename, employee_type, 
                        status, cnic, bank_name, account_number, company_id 
                 FROM employees WHERE status = 'active' AND company_id = ? ORDER BY name''', (company_id,))
    employees = c.fetchall()
    conn.close()
    return employees

def get_employee_by_id(employee_id, company_id=None):
    if company_id is None:
        company_id = get_current_company_id()
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute('''SELECT id, name, email, phone, position, department, joining_date, 
                        salary, petrol_allowance, location, cv_filename, employee_type, 
                        status, cnic, bank_name, account_number, company_id 
                 FROM employees WHERE id = ? AND company_id = ?''', (employee_id, company_id))
    employee = c.fetchone()
    conn.close()
    return employee

def get_employee_details(employee_id, company_id=None):
    """Get complete employee details for auto-fill"""
    if company_id is None:
        company_id = get_current_company_id()
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute('''SELECT id, name, department, position, salary, petrol_allowance, 
                        bank_name, account_number, joining_date, employee_type, cnic, phone, email 
                 FROM employees WHERE id = ? AND company_id = ?''', (employee_id, company_id))
    employee = c.fetchone()
    conn.close()
    if employee:
        return {
            'id': employee[0],
            'name': employee[1],
            'team': employee[2],
            'position': employee[3],
            'salary': float(employee[4]) if employee[4] else 0,
            'petrol_allowance': float(employee[5]) if employee[5] else 0,
            'bank_name': employee[6] or '',
            'account_number': employee[7] or '',
            'joining_date': employee[8],
            'employee_type': employee[9],
            'cnic': employee[10],
            'phone': employee[11],
            'email': employee[12]
        }
    return None

def search_employees(search_term, company_id=None):
    """Search employees by name or team"""
    if company_id is None:
        company_id = get_current_company_id()
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute('''SELECT id, name, department, position, salary, petrol_allowance, bank_name, account_number 
                 FROM employees 
                 WHERE (name LIKE ? OR department LIKE ? OR position LIKE ?)
                 AND status = 'active' AND company_id = ?
                 LIMIT 15''', 
              (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', company_id))
    employees = c.fetchall()
    conn.close()
    return employees

def add_employee(name, email, phone, position, department, joining_date, salary, petrol_allowance, location, cv_filename, employee_type='Probation', cnic='', bank_name='', account_number='', company_id=None):
    if company_id is None:
        company_id = get_current_company_id()
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute('''INSERT INTO employees (company_id, name, email, phone, position, department, joining_date, 
                        salary, petrol_allowance, location, cv_filename, employee_type, status, cnic, bank_name, account_number)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (company_id, name, email, phone, position, department, joining_date, salary, petrol_allowance, location, cv_filename, employee_type, 'active', cnic, bank_name, account_number))
    conn.commit()
    conn.close()

def update_employee(employee_id, name, email, phone, position, department, joining_date, salary, petrol_allowance, location, employee_type, cnic='', bank_name='', account_number='', company_id=None):
    if company_id is None:
        company_id = get_current_company_id()
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute('''UPDATE employees SET name=?, email=?, phone=?, position=?, department=?, 
                        joining_date=?, salary=?, petrol_allowance=?, location=?, employee_type=?, 
                        cnic=?, bank_name=?, account_number=?
                 WHERE id=? AND company_id=?''',
              (name, email, phone, position, department, joining_date, salary, petrol_allowance, location, employee_type, cnic, bank_name, account_number, employee_id, company_id))
    conn.commit()
    conn.close()

def delete_employee(employee_id, company_id=None):
    if company_id is None:
        company_id = get_current_company_id()
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute('DELETE FROM employees WHERE id = ? AND company_id = ?', (employee_id, company_id))
    conn.commit()
    conn.close()

def update_employee_salary(employee_id, new_salary, company_id=None):
    """Update employee salary - used by increment module"""
    if company_id is None:
        company_id = get_current_company_id()
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute("UPDATE employees SET salary = ? WHERE id = ? AND company_id = ?", (new_salary, employee_id, company_id))
    conn.commit()
    conn.close()
    print(f"✅ Salary updated for employee ID {employee_id} to {new_salary}")

def get_employee_salary(employee_id, company_id=None):
    """Get employee current salary"""
    if company_id is None:
        company_id = get_current_company_id()
    conn = get_db_connection('employees.db')
    c = conn.cursor()
    c.execute("SELECT salary FROM employees WHERE id = ? AND company_id = ?", (employee_id, company_id))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0