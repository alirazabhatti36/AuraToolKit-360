from modules.database import get_db_connection

def get_activity_log(limit=200):
    """Get all activity logs"""
    conn = get_db_connection('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM activity_log ORDER BY created_at DESC LIMIT ?''', (limit,))
    logs = c.fetchall()
    conn.close()
    return logs

def get_activity_by_user(user_id, limit=50):
    """Get activity logs by user"""
    conn = get_db_connection('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM activity_log WHERE user_id = ? ORDER BY created_at DESC LIMIT ?''', 
              (user_id, limit))
    logs = c.fetchall()
    conn.close()
    return logs

def get_activity_by_module(module, limit=50):
    """Get activity logs by module"""
    conn = get_db_connection('users.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM activity_log WHERE module = ? ORDER BY created_at DESC LIMIT ?''', 
              (module, limit))
    logs = c.fetchall()
    conn.close()
    return logs

def clear_old_logs(days=30):
    """Clear logs older than specified days"""
    from datetime import datetime, timedelta
    conn = get_db_connection('users.db')
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    c.execute('DELETE FROM activity_log WHERE created_at < ?', (cutoff,))
    conn.commit()
    conn.close()