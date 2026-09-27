import sqlite3
import os

def reset_employee_ids():
    # Database ka path
    db_path = 'databases/employees.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees'")
    if not cursor.fetchone():
        print("❌ Employees table not found!")
        conn.close()
        return
    
    # Get current data
    cursor.execute("PRAGMA table_info(employees)")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Create new table
    cursor.execute('''
        CREATE TABLE employees_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT, phone TEXT, position TEXT, 
            department TEXT, joining_date TEXT, salary REAL, 
            petrol_allowance REAL, location TEXT, cv_filename TEXT, 
            employee_type TEXT, status TEXT, cnic TEXT, 
            bank_name TEXT, account_number TEXT
        )
    ''')
    
    # Copy data without IDs
    column_names = ', '.join([col for col in columns if col != 'id'])
    cursor.execute(f'''
        INSERT INTO employees_new ({column_names})
        SELECT {column_names}
        FROM employees
        ORDER BY id ASC
    ''')
    
    # Drop old table
    cursor.execute('DROP TABLE employees')
    
    # Rename new table
    cursor.execute('ALTER TABLE employees_new RENAME TO employees')
    
    conn.commit()
    
    # Get new count
    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]
    
    conn.close()
    
    print(f"✅ IDs reset successfully! Total employees: {count}")
    print("📌 IDs will now start from 1 in sequence.")

if __name__ == '__main__':
    print("🔄 Resetting employee IDs...")
    reset_employee_ids()
    print("✅ Done!")