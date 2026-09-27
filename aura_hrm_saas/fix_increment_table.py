import sqlite3
import os

def create_increment_table():
    db_path = 'databases/increment.db'
    
    # Create databases folder if not exists
    os.makedirs('databases', exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create increment table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS increments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            employee_name TEXT,
            team TEXT,
            current_salary REAL,
            increment_percent REAL,
            new_salary REAL,
            last_increment_date TEXT,
            next_increment_date TEXT,
            effective_date TEXT,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            approved_by TEXT,
            approved_date TEXT,
            remarks TEXT,
            created_at TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Increment table created successfully!")

if __name__ == '__main__':
    create_increment_table()