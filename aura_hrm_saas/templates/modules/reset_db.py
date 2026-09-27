import os
import sqlite3

DB_PATH = 'databases/'

print("=" * 50)
print("🔧 FORCE RESET DATABASES")
print("=" * 50)

# Force close any connections
import gc
gc.collect()

# Delete all database files
db_files = ['candidates.db', 'employees.db', 'inventory.db', 'payroll.db']
for db_file in db_files:
    db_path = os.path.join(DB_PATH, db_file)
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"✅ Deleted: {db_file}")
        except PermissionError:
            print(f"⚠️ Permission error on {db_file}, trying force...")
            try:
                # Try to change file attributes
                os.chmod(db_path, 0o666)
                os.remove(db_path)
                print(f"✅ Force deleted: {db_file}")
            except:
                print(f"❌ Could not delete {db_file}")
    else:
        print(f"⚠️ {db_file} not found")

# Recreate employees database directly
print("\n📀 Recreating employees database with CNIC column...")
db_path = os.path.join(DB_PATH, 'employees.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    position TEXT,
    department TEXT,
    joining_date TEXT,
    salary TEXT,
    location TEXT,
    cv_filename TEXT,
    employee_type TEXT DEFAULT 'Probation',
    status TEXT DEFAULT 'active',
    cnic TEXT,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)''')
conn.commit()
conn.close()
print("✅ employees.db created with CNIC column!")

print("\n" + "=" * 50)
print("🎉 RESET COMPLETE! Now run python app.py")
print("=" * 50)