from modules.database import get_db_connection
from modules.employees import get_employee_by_id

def get_all_weekend():
    conn = get_db_connection('weekend.db')
    c = conn.cursor()
    c.execute('SELECT * FROM weekend ORDER BY id DESC')
    weekend = c.fetchall()
    conn.close()
    return weekend

def get_weekend_stats():
    conn = get_db_connection('weekend.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM weekend')
    total = c.fetchone()[0]
    c.execute('SELECT SUM(amount) FROM weekend')
    total_amount = c.fetchone()[0] or 0
    conn.close()
    return {'total': total, 'total_amount': total_amount}

def calculate_weekend_amount(employee_id, weekend_count):
    """Calculate weekend amount based on employee salary: (Salary / 30) * weekend_count"""
    employee = get_employee_by_id(employee_id)
    if employee:
        salary = float(employee[7]) if employee[7] else 0
        per_day = salary / 30
        return round(per_day * weekend_count, 2)
    return 0

def add_weekend_bulk(entries, month, year):
    """Add multiple weekend entries at once and update payroll"""
    conn = get_db_connection('weekend.db')
    c = conn.cursor()
    
    for entry in entries:
        # Calculate amount
        amount = calculate_weekend_amount(entry['employee_id'], entry['weekend_count'])
        
        # Check if weekend entry already exists for this employee/month/year
        c.execute('SELECT id FROM weekend WHERE employee_id = ? AND month = ? AND year = ?', 
                  (entry['employee_id'], month, year))
        existing = c.fetchone()
        
        if existing:
            # Update existing
            c.execute('UPDATE weekend SET weekend_count = ?, amount = ? WHERE id = ?',
                      (entry['weekend_count'], amount, existing[0]))
        else:
            # Insert new
            c.execute('''INSERT INTO weekend (employee_id, employee_name, team, weekend_count, month, year, amount)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (entry['employee_id'], entry['employee_name'], entry['team'], 
                       entry['weekend_count'], month, year, amount))
    conn.commit()
    conn.close()
    
    # Update payroll for each employee
    for entry in entries:
        update_or_create_payroll_with_weekend(entry['employee_id'], month, year)

def update_or_create_payroll_with_weekend(employee_id, month, year):
    """Update payroll additional earnings with weekend amount. Create payroll if not exists."""
    
    # Get employee details
    employee = get_employee_by_id(employee_id)
    if not employee:
        print(f"❌ Employee {employee_id} not found")
        return
    
    employee_name = employee[1]
    team = employee[5] or 'Not specified'
    basic_salary = float(employee[7]) if employee[7] else 0
    petrol_allowance = float(employee[8]) if employee[8] else 0
    
    # Get total weekend amount
    conn_weekend = get_db_connection('weekend.db')
    c_weekend = conn_weekend.cursor()
    c_weekend.execute('SELECT SUM(amount) FROM weekend WHERE employee_id = ? AND month = ? AND year = ?', 
                      (employee_id, month, year))
    total_weekend_amount = c_weekend.fetchone()[0] or 0
    conn_weekend.close()
    
    print(f"📊 Employee: {employee_name}, Basic: {basic_salary}, Petrol: {petrol_allowance}, Weekend: {total_weekend_amount}")
    
    conn_payroll = get_db_connection('payroll.db')
    c_payroll = conn_payroll.cursor()
    
    # Check if payroll exists
    c_payroll.execute('SELECT id FROM payroll WHERE employee_id = ? AND month = ? AND year = ?', 
                      (employee_id, month, year))
    existing = c_payroll.fetchone()
    
    gross = basic_salary + petrol_allowance + total_weekend_amount
    net = gross  # Assuming no tax/deductions for now
    
    if existing:
        # Update existing payroll
        payroll_id = existing[0]
        c_payroll.execute('UPDATE payroll SET additional_earnings = ?, gross_salary = ?, net_salary = ? WHERE id = ?', 
                          (total_weekend_amount, gross, net, payroll_id))
        print(f"✅ Payroll updated for {employee_name}: Additional Earnings = {total_weekend_amount}")
    else:
        # Create new payroll record
        c_payroll.execute('''INSERT INTO payroll (employee_id, team, employee_name, working_days, basic_salary, 
                          petrol_allowance, additional_earnings, gross_salary, net_salary, month, year, status)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (employee_id, team, employee_name, 30, basic_salary, petrol_allowance, 
                           total_weekend_amount, gross, net, month, year, 'Pending'))
        print(f"✅ New payroll created for {employee_name} with weekend amount {total_weekend_amount}")
    
    conn_payroll.commit()
    conn_payroll.close()

def delete_weekend(weekend_id):
    conn = get_db_connection('weekend.db')
    c = conn.cursor()
    c.execute('SELECT employee_id, month, year FROM weekend WHERE id = ?', (weekend_id,))
    weekend = c.fetchone()
    if weekend:
        employee_id, month, year = weekend
        c.execute('DELETE FROM weekend WHERE id = ?', (weekend_id,))
        conn.commit()
        conn.close()
        update_or_create_payroll_with_weekend(employee_id, month, year)
    else:
        conn.close()