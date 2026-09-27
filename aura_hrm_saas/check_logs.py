import sqlite3
conn = sqlite3.connect('databases/activity_logs.db')
c = conn.cursor()
c.execute("SELECT id, user, action, created_at FROM activity_logs ORDER BY id DESC LIMIT 10")
rows = c.fetchall()
print('latest logs:')
for r in rows:
    print(r)
conn.close()
