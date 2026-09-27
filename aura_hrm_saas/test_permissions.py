import sqlite3
conn=sqlite3.connect('databases/users.db')
c=conn.cursor()
c.execute("SELECT id, username, role FROM users")
for r in c.fetchall():
    print(r)
conn.close()
