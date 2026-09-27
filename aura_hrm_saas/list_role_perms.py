import sqlite3
conn=sqlite3.connect('databases/users.db')
c=conn.cursor()
for role in ['admin','hr_manager','accountant','management','employee']:
    c.execute("SELECT id FROM roles WHERE name=?",(role,))
    r=c.fetchone()
    if not r:
        print(role,'not found')
        continue
    rid=r[0]
    c.execute("SELECT permission FROM role_permissions WHERE role_id=?",(rid,))
    perms=[p[0] for p in c.fetchall()]
    print(role, '->', perms)
conn.close()
