from modules.database import get_db_connection
from datetime import datetime

TEAMS = ['Webbuggs', 'Simpli Plugin', 'BuggByte Studios']

def get_teams():
    return TEAMS

def get_all_payroll():
    conn = get_db_connection('payroll.db')
    c = conn.cursor()
    c.execute('SELECT * FROM payroll ORDER BY id DESC')
    payroll = c.fetchall()
    conn.close()
    return payroll

def get_payroll_by_id(payroll_id):
    conn = get_db_connection('payroll.db')
    c = conn.cursor()
    c.execute('SELECT * FROM payroll WHERE id = ?', (payroll_id,))
    payroll = c.fetchone()
    conn.close()
    return payroll

def get_payroll_by_employee(employee_id):
    """Get payroll records for a specific employee"""
    conn = get_db_connection('payroll.db')
    c = conn.cursor()
    c.execute('SELECT * FROM payroll WHERE employee_id = ? ORDER BY year DESC, month DESC', (employee_id,))
    payroll = c.fetchall()
    conn.close()
    return payroll

def get_payroll_stats():
    conn = get_db_connection('payroll.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM payroll')
    total_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM payroll WHERE status = "Paid"')
    paid_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM payroll WHERE status = "Pending"')
    pending_count = c.fetchone()[0]

    c.execute('SELECT SUM(net_salary) FROM payroll')
    total_amount = c.fetchone()[0] or 0
    c.execute('SELECT SUM(net_salary) FROM payroll WHERE status = "Paid"')
    paid_amount = c.fetchone()[0] or 0
    c.execute('SELECT SUM(net_salary) FROM payroll WHERE status = "Pending"')
    pending_amount = c.fetchone()[0] or 0
    
    # Team wise stats
    c.execute('''SELECT team, COUNT(*) as count, SUM(net_salary) as total, 
                    SUM(CASE WHEN status = "Paid" THEN net_salary ELSE 0 END) as paid_amount
                 FROM payroll GROUP BY team''')
    team_stats = c.fetchall()
    conn.close()
    return {
        'total_count': total_count,
        'paid_count': paid_count,
        'pending_count': pending_count,
        'total_amount': total_amount,
        'paid_amount': paid_amount,
        'pending_amount': pending_amount,
        'team_stats': team_stats
    }

def calculate_gross_salary(basic, petrol, overtime, bonus):
    return basic + petrol + overtime + bonus

def calculate_net_salary(gross, tax, other_deductions, advance):
    return gross - (tax + other_deductions + advance)

def add_payroll(data):
    conn = get_db_connection('payroll.db')
    c = conn.cursor()
    c.execute('''INSERT INTO payroll (
        employee_id, team, employee_name, working_days,
        basic_salary, petrol_allowance, additional_earnings,
        gross_salary, income_tax, other_deductions, leaves,
        net_salary, bank_salary, cash_salary,
        remarks, bank_name, account_number, month, year, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (data['employee_id'], data['team'], data['employee_name'], data['working_days'],
         data['basic_salary'], data['petrol_allowance'], data['additional_earnings'],
         data['gross_salary'], data['income_tax'], data['other_deductions'], data['leaves'],
         data['net_salary'], data['bank_salary'], data['cash_salary'],
         data['remarks'], data['bank_name'], data['account_number'], 
         data['month'], data['year'], data['status']))
    conn.commit()
    conn.close()

def update_payroll(payroll_id, data):
    conn = get_db_connection('payroll.db')
    c = conn.cursor()
    c.execute('''UPDATE payroll SET 
        employee_id=?, team=?, employee_name=?, working_days=?,
        basic_salary=?, petrol_allowance=?, additional_earnings=?,
        gross_salary=?, income_tax=?, other_deductions=?, leaves=?,
        net_salary=?, bank_salary=?, cash_salary=?,
        remarks=?, bank_name=?, account_number=?, month=?, year=?, status=?
        WHERE id=?''',
        (data['employee_id'], data['team'], data['employee_name'], data['working_days'],
         data['basic_salary'], data['petrol_allowance'], data['additional_earnings'],
         data['gross_salary'], data['income_tax'], data['other_deductions'], data['leaves'],
         data['net_salary'], data['bank_salary'], data['cash_salary'],
         data['remarks'], data['bank_name'], data['account_number'],
         data['month'], data['year'], data['status'], payroll_id))
    conn.commit()
    conn.close()

def delete_payroll(payroll_id):
    conn = get_db_connection('payroll.db')
    c = conn.cursor()
    c.execute('DELETE FROM payroll WHERE id = ?', (payroll_id,))
    conn.commit()
    conn.close()

def process_payroll_record(payroll_id):
    conn = get_db_connection('payroll.db')
    c = conn.cursor()
    c.execute('UPDATE payroll SET status = "Paid", payment_date = ? WHERE id = ?', 
              (datetime.now().strftime('%Y-%m-%d'), payroll_id))
    conn.commit()
    conn.close()