import sqlite3
conn=sqlite3.connect('databases/activity_logs.db')
c=conn.cursor()
c.execute("SELECT COUNT(*) FROM activity_logs WHERE created_at < datetime('now', '-30 days')")
print('count older than 30 days:', c.fetchone()[0])
c.execute("SELECT datetime('now','-30 days')")
print('datetime now -30:', c.fetchone()[0])
conn.close()
