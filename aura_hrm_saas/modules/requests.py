from modules.database import get_db_connection
from datetime import datetime

def get_all_requests():
    """Get all requests"""
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    c.execute('''SELECT id, employee_id, employee_name, request_type, subject, description, 
                        start_date, end_date, status, submitted_date, reviewer_name, reviewer_remarks, reviewed_date
                 FROM requests ORDER BY submitted_date DESC''')
    requests = c.fetchall()
    conn.close()
    return requests

def get_pending_requests():
    """Get only pending requests"""
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    c.execute('''SELECT id, employee_id, employee_name, request_type, subject, description, 
                        start_date, end_date, status, submitted_date, reviewer_name, reviewer_remarks, reviewed_date
                 FROM requests WHERE status = 'pending' ORDER BY submitted_date ASC''')
    requests = c.fetchall()
    conn.close()
    return requests

def get_requests_by_employee(employee_id):
    """Get requests for a specific employee"""
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    c.execute('''SELECT id, employee_id, employee_name, request_type, subject, description, 
                        start_date, end_date, status, submitted_date, reviewer_name, reviewer_remarks, reviewed_date
                 FROM requests WHERE employee_id = ? ORDER BY submitted_date DESC''', (employee_id,))
    requests = c.fetchall()
    conn.close()
    return requests

def get_requests_by_status(status):
    """Get requests by status (pending, approved, rejected)"""
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    c.execute('''SELECT id, employee_id, employee_name, request_type, subject, description, 
                        start_date, end_date, status, submitted_date, reviewer_name, reviewer_remarks, reviewed_date
                 FROM requests WHERE status = ? ORDER BY submitted_date DESC''', (status,))
    requests = c.fetchall()
    conn.close()
    return requests

def get_all_requests_with_status():
    """Get all requests with any status (for reports)"""
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    c.execute('''SELECT id, employee_id, employee_name, request_type, subject, description, 
                        start_date, end_date, status, submitted_date, reviewer_name, reviewer_remarks, reviewed_date
                 FROM requests ORDER BY submitted_date DESC''')
    requests = c.fetchall()
    conn.close()
    return requests

def get_requests_stats():
    """Get statistics for requests"""
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM requests")
    total = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM requests WHERE status = 'pending'")
    pending = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM requests WHERE status = 'approved'")
    approved = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM requests WHERE status = 'rejected'")
    rejected = c.fetchone()[0]
    
    conn.close()
    
    return {
        'total': total,
        'pending': pending,
        'approved': approved,
        'rejected': rejected
    }

def add_request(employee_id, employee_name, request_type, subject, description, start_date, end_date):
    """Add a new request"""
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    c.execute('''INSERT INTO requests 
                 (employee_id, employee_name, request_type, subject, description, start_date, end_date, 
                  status, submitted_date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (employee_id, employee_name, request_type, subject, description, start_date, end_date, 
               'pending', datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()

def approve_request(request_id, reviewer_id, reviewer_name, remarks):
    """Approve a request"""
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    c.execute('''UPDATE requests 
                 SET status = 'approved', 
                     reviewer_id = ?, 
                     reviewer_name = ?, 
                     reviewer_remarks = ?, 
                     reviewed_date = ?
                 WHERE id = ?''',
              (reviewer_id, reviewer_name, remarks, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request_id))
    conn.commit()
    conn.close()

def reject_request(request_id, reviewer_id, reviewer_name, remarks):
    """Reject a request"""
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    c.execute('''UPDATE requests 
                 SET status = 'rejected', 
                     reviewer_id = ?, 
                     reviewer_name = ?, 
                     reviewer_remarks = ?, 
                     reviewed_date = ?
                 WHERE id = ?''',
              (reviewer_id, reviewer_name, remarks, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request_id))
    conn.commit()
    conn.close()

def delete_request(request_id):
    """Delete a request"""
    conn = get_db_connection('requests.db')
    c = conn.cursor()
    c.execute("DELETE FROM requests WHERE id = ?", (request_id,))
    conn.commit()
    conn.close()