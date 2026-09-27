import sqlite3
conn = sqlite3.connect('databases/users.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print('tables:', [r[0] for r in c.fetchall()])
# show sample rows from role_permissions
try:
    c.execute('SELECT * FROM role_permissions LIMIT 5')
    print('role_permissions rows:', c.fetchall())
except Exception as e:
    print('error querying role_permissions:', e)
conn.close()
