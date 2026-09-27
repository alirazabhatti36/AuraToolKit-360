import sqlite3
import os

def check_attendance():
    db_path = 'databases/attendance.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("📋 Tables in attendance.db:", tables)
    
    # Check attendance table columns
    cursor.execute("PRAGMA table_info(attendance)")
    columns = [col[1] for col in cursor.fetchall()]
    print("\n📋 Columns in attendance table:", columns)
    
    # Check if any data exists
    cursor.execute("SELECT COUNT(*) FROM attendance")
    count = cursor.fetchone()[0]
    print(f"\n📊 Total attendance records: {count}")
    
    if count > 0:
        cursor.execute("SELECT * FROM attendance LIMIT 3")
        sample = cursor.fetchall()
        print("\n📋 Sample data:", sample)
    
    conn.close()

if __name__ == '__main__':
    check_attendance()