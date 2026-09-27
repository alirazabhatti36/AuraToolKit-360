from modules.database import get_db_connection
from datetime import datetime

def get_all_increments():
    """Get all increment records"""
    conn = get_db_connection('increment.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, employee_id, employee_name, team, current_salary, increment_percent, 
               new_salary, last_increment_date, next_increment_date, effective_date, 
               reason, status, approved_by, approved_date, remarks, created_at
        FROM increments 
        ORDER BY team, employee_name
    ''')
    increments = cursor.fetchall()
    conn.close()
    return increments

def get_increments_by_team(team):
    """Get increments for specific team"""
    conn = get_db_connection('increment.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, employee_id, employee_name, team, current_salary, increment_percent, 
               new_salary, last_increment_date, next_increment_date, effective_date, 
               reason, status, approved_by, approved_date, remarks, created_at
        FROM increments 
        WHERE team = ?
        ORDER BY employee_name
    ''', (team,))
    increments = cursor.fetchall()
    conn.close()
    return increments

def get_teams():
    """Get all unique teams"""
    conn = get_db_connection('increment.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT team FROM increments ORDER BY team")
    teams = [row[0] for row in cursor.fetchall()]
    conn.close()
    return teams

def get_increment_stats():
    """Get increment statistics"""
    conn = get_db_connection('increment.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM increments")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM increments WHERE status = 'pending'")
    pending = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM increments WHERE status = 'approved'")
    approved = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM increments WHERE status = 'rejected'")
    rejected = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM increments WHERE status = 'implemented'")
    implemented = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(new_salary - current_salary) FROM increments WHERE status = 'approved' OR status = 'implemented'")
    total_increase = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'total': total,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'implemented': implemented,
        'total_increase': total_increase
    }

def add_or_update_increment(employee_id, employee_name, team, current_salary, increment_percent, 
                            new_salary, last_increment_date, next_increment_date, effective_date, 
                            reason, remarks=''):
    """Add or update increment record"""
    conn = get_db_connection('increment.db')
    cursor = conn.cursor()
    
    # Check if already exists
    cursor.execute("SELECT id FROM increments WHERE employee_id = ?", (employee_id,))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('''
            UPDATE increments 
            SET increment_percent = ?, new_salary = ?, next_increment_date = ?, 
                effective_date = ?, reason = ?, remarks = ?, status = 'pending'
            WHERE employee_id = ?
        ''', (increment_percent, new_salary, next_increment_date, effective_date, reason, remarks, employee_id))
    else:
        cursor.execute('''
            INSERT INTO increments 
            (employee_id, employee_name, team, current_salary, increment_percent, new_salary,
             last_increment_date, next_increment_date, effective_date, reason, status, remarks, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (employee_id, employee_name, team, current_salary, increment_percent, new_salary,
              last_increment_date, next_increment_date, effective_date, reason, 'pending', remarks, 
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    
    conn.commit()
    conn.close()
    return True

def approve_increment(increment_id, approved_by, remarks=''):
    """Approve an increment"""
    conn = get_db_connection('increment.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE increments 
        SET status = 'approved', approved_by = ?, approved_date = ?, remarks = ?
        WHERE id = ?
    ''', (approved_by, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), remarks, increment_id))
    conn.commit()
    conn.close()

def reject_increment(increment_id, remarks=''):
    """Reject an increment"""
    conn = get_db_connection('increment.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE increments 
        SET status = 'rejected', remarks = ?
        WHERE id = ?
    ''', (remarks, increment_id))
    conn.commit()
    conn.close()

def implement_increment(increment_id):
    """Implement increment (update employee salary)"""
    conn = get_db_connection('increment.db')
    cursor = conn.cursor()
    
    # Get increment details
    cursor.execute("SELECT employee_id, new_salary FROM increments WHERE id = ?", (increment_id,))
    inc = cursor.fetchone()
    
    if inc:
        # Update employee salary in employees.db
        from modules.employees import update_employee_salary
        update_employee_salary(inc[0], inc[1])
        
        # Update increment status
        cursor.execute("UPDATE increments SET status = 'implemented' WHERE id = ?", (increment_id,))
        conn.commit()
    
    conn.close()

def bulk_update_increment(team, increment_percent, effective_date, reason):
    """Bulk update increments for all employees in a team"""
    conn = get_db_connection('increment.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE increments 
        SET increment_percent = ?, new_salary = current_salary * (1 + ?/100),
            effective_date = ?, reason = ?, status = 'pending'
        WHERE team = ? AND status NOT IN ('approved', 'implemented')
    ''', (increment_percent, increment_percent, effective_date, reason, team))
    
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected