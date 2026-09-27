from modules.database import get_db_connection
from datetime import datetime, date
import calendar

# ============= ATTENDANCE FUNCTIONS =============
def get_today_attendance():
    today = date.today().strftime('%Y-%m-%d')
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attendance WHERE date = ? ORDER BY check_in DESC', (today,))
    attendance = c.fetchall()
    conn.close()
    return attendance

def get_attendance_by_date(date_str):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM attendance WHERE date = ? ORDER BY check_in DESC', (date_str,))
    attendance = c.fetchall()
    conn.close()
    return attendance

def get_attendance_by_employee(employee_id, month, year):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM attendance 
                 WHERE employee_id = ? AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
                 ORDER BY date DESC''', (employee_id, month.zfill(2), year))
    attendance = c.fetchall()
    conn.close()
    return attendance

def get_monthly_attendance(month, year):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM attendance 
                 WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
                 ORDER BY date DESC''', (month.zfill(2), year))
    attendance = c.fetchall()
    conn.close()
    return attendance

def get_attendance_summary(month, year):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT 
                    COUNT(*) as total_days,
                    SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present,
                    SUM(CASE WHEN status = 'Late' THEN 1 ELSE 0 END) as late,
                    SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) as absent,
                    AVG(late_minutes) as avg_late,
                    SUM(working_hours) as total_hours
                 FROM attendance 
                 WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?''', 
                 (month.zfill(2), year))
    summary = c.fetchone()
    conn.close()
    return summary

def get_team_attendance_summary(month, year):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT 
                    team,
                    COUNT(DISTINCT employee_id) as total_employees,
                    COUNT(*) as total_days,
                    SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present,
                    SUM(CASE WHEN status = 'Late' THEN 1 ELSE 0 END) as late,
                    SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) as absent
                 FROM attendance 
                 WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?
                 GROUP BY team''', 
                 (month.zfill(2), year))
    summary = c.fetchall()
    conn.close()
    return summary

def check_in(employee_id, employee_name, team, check_in_time=None):
    if check_in_time is None:
        check_in_time = datetime.now().strftime('%H:%M:%S')
    
    today = date.today().strftime('%Y-%m-%d')
    
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    
    # Check if already checked in today
    c.execute('SELECT * FROM attendance WHERE employee_id = ? AND date = ?', (employee_id, today))
    existing = c.fetchone()
    
    if existing:
        conn.close()
        return False, "Already checked in today!"
    
    # Calculate late minutes (if after 9:30 AM)
    late_minutes = 0
    if check_in_time > '09:30:00':
        late_minutes = (datetime.strptime(check_in_time, '%H:%M:%S') - datetime.strptime('09:30:00', '%H:%M:%S')).seconds // 60
    
    status = 'Present' if late_minutes == 0 else 'Late'
    
    c.execute('''INSERT INTO attendance (employee_id, employee_name, team, date, check_in, late_minutes, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (employee_id, employee_name, team, today, check_in_time, late_minutes, status))
    conn.commit()
    conn.close()
    return True, f"✅ Checked in at {check_in_time}"

def check_out(employee_id, check_out_time=None):
    if check_out_time is None:
        check_out_time = datetime.now().strftime('%H:%M:%S')
    
    today = date.today().strftime('%Y-%m-%d')
    
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    
    # Get today's attendance record
    c.execute('SELECT * FROM attendance WHERE employee_id = ? AND date = ?', (employee_id, today))
    record = c.fetchone()
    
    if not record:
        conn.close()
        return False, "No check-in record found for today!"
    
    if record[6]:  # check_out already exists
        conn.close()
        return False, "Already checked out today!"
    
    # Calculate working hours
    check_in = record[5]
    check_in_dt = datetime.strptime(check_in, '%H:%M:%S')
    check_out_dt = datetime.strptime(check_out_time, '%H:%M:%S')
    working_hours = (check_out_dt - check_in_dt).seconds / 3600
    
    # Calculate overtime (after 6 PM)
    overtime_minutes = 0
    if check_out_time > '18:00:00':
        overtime_minutes = (datetime.strptime(check_out_time, '%H:%M:%S') - datetime.strptime('18:00:00', '%H:%M:%S')).seconds // 60
    
    c.execute('''UPDATE attendance 
                 SET check_out = ?, overtime_minutes = ?, working_hours = ?
                 WHERE employee_id = ? AND date = ?''',
              (check_out_time, overtime_minutes, working_hours, employee_id, today))
    conn.commit()
    conn.close()
    return True, f"✅ Checked out at {check_out_time} | Working Hours: {working_hours:.2f}"

def apply_leave(employee_id, employee_name, team, from_date, to_date, leave_type, reason):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('''INSERT INTO leave_requests (employee_id, employee_name, team, from_date, to_date, leave_type, reason, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (employee_id, employee_name, team, from_date, to_date, leave_type, reason, 'Pending'))
    conn.commit()
    conn.close()
    return True

def get_leave_requests(status=None):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    if status:
        c.execute('SELECT * FROM leave_requests WHERE status = ? ORDER BY applied_on DESC', (status,))
    else:
        c.execute('SELECT * FROM leave_requests ORDER BY applied_on DESC')
    leaves = c.fetchall()
    conn.close()
    return leaves

def get_leave_requests_by_employee(employee_id):
    """Get leave requests for a specific employee"""
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM leave_requests WHERE employee_id = ? ORDER BY applied_on DESC''', (employee_id,))
    leaves = c.fetchall()
    conn.close()
    return leaves

def update_leave_status(leave_id, status, approved_by=None):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    if approved_by:
        c.execute('UPDATE leave_requests SET status = ?, approved_by = ?, approved_on = ? WHERE id = ?', 
                  (status, approved_by, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), leave_id))
    else:
        c.execute('UPDATE leave_requests SET status = ? WHERE id = ?', (status, leave_id))
    conn.commit()
    conn.close()

def get_holidays(year):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM holidays WHERE year = ? ORDER BY date', (year,))
    holidays = c.fetchall()
    conn.close()
    return holidays

def add_holiday(date_str, name, year):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO holidays (date, name, year) VALUES (?, ?, ?)", (date_str, name, year))
    conn.commit()
    conn.close()

def delete_holiday(holiday_id):
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    c.execute('DELETE FROM holidays WHERE id = ?', (holiday_id,))
    conn.commit()
    conn.close()

def mark_absent(employee_id, employee_name, team, date_str):
    """Mark employee as absent for a specific date"""
    conn = get_db_connection('attendance.db')
    c = conn.cursor()
    
    # Check if already has attendance record
    c.execute('SELECT * FROM attendance WHERE employee_id = ? AND date = ?', (employee_id, date_str))
    existing = c.fetchone()
    
    if not existing:
        c.execute('''INSERT INTO attendance (employee_id, employee_name, team, date, status)
                     VALUES (?, ?, ?, ?, ?)''',
                  (employee_id, employee_name, team, date_str, 'Absent'))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False