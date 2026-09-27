from modules.database import get_db_connection
from flask import request
from datetime import datetime, timedelta

def log_activity(user, action, details=""):
    """Log user activity"""
    try:
        conn = get_db_connection('activity_logs.db')
        c = conn.cursor()
        
        # Get IP address
        ip_address = request.remote_addr if request else "Unknown"
        
        c.execute('''INSERT INTO activity_logs (user, action, details, ip_address, created_at)
                     VALUES (?, ?, ?, ?, ?)''',
                  (user, action, details, ip_address, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
        print(f"[LOG] {user} - {action}")
    except Exception as e:
        print(f"Error logging activity: {e}")

def get_all_logs(limit=200):
    """Get all activity logs"""
    conn = get_db_connection('activity_logs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM activity_logs ORDER BY id DESC LIMIT ?', (limit,))
    logs = c.fetchall()
    conn.close()
    return logs

def get_logs_by_user(user):
    """Get logs by specific user"""
    conn = get_db_connection('activity_logs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM activity_logs WHERE user = ? ORDER BY id DESC', (user,))
    logs = c.fetchall()
    conn.close()
    return logs

def get_logs_by_action(action):
    """Get logs by action type"""
    conn = get_db_connection('activity_logs.db')
    c = conn.cursor()
    c.execute('SELECT * FROM activity_logs WHERE action LIKE ? ORDER BY id DESC', (f'%{action}%',))
    logs = c.fetchall()
    conn.close()
    return logs

def get_logs_stats():
    """Get activity logs statistics"""
    conn = get_db_connection('activity_logs.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM activity_logs')
    total = c.fetchone()[0]
    c.execute('SELECT COUNT(DISTINCT user) FROM activity_logs')
    unique_users = c.fetchone()[0]
    c.execute('SELECT action, COUNT(*) as count FROM activity_logs GROUP BY action ORDER BY count DESC LIMIT 10')
    top_actions = c.fetchall()
    conn.close()
    return {'total': total, 'unique_users': unique_users, 'top_actions': top_actions}

def clear_old_logs(days=30):
    """Delete logs older than specified days"""
    conn = get_db_connection('activity_logs.db')
    c = conn.cursor()
    # Calculate cutoff datetime in Python to avoid SQLite datetime modifier quirks
    cutoff = datetime.now() - timedelta(days=days)
    cutoff_str = cutoff.strftime('%Y-%m-%d %H:%M:%S')
    c.execute('DELETE FROM activity_logs WHERE created_at < ?', (cutoff_str,))
    conn.commit()
    deleted = c.rowcount
    conn.close()
    return deleted