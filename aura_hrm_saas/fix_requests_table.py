import sqlite3
import os

def fix_requests_table():
    db_path = 'databases/requests.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check existing columns
    cursor.execute("PRAGMA table_info(requests)")
    columns = [col[1] for col in cursor.fetchall()]
    
    print("📋 Existing columns:", columns)
    
    # Add missing columns if not exist
    if 'submitted_date' not in columns:
        print("✅ Adding column: submitted_date")
        cursor.execute("ALTER TABLE requests ADD COLUMN submitted_date TEXT")
    
    if 'reviewer_id' not in columns:
        print("✅ Adding column: reviewer_id")
        cursor.execute("ALTER TABLE requests ADD COLUMN reviewer_id INTEGER")
    
    if 'reviewer_name' not in columns:
        print("✅ Adding column: reviewer_name")
        cursor.execute("ALTER TABLE requests ADD COLUMN reviewer_name TEXT")
    
    if 'reviewer_remarks' not in columns:
        print("✅ Adding column: reviewer_remarks")
        cursor.execute("ALTER TABLE requests ADD COLUMN reviewer_remarks TEXT")
    
    if 'reviewed_date' not in columns:
        print("✅ Adding column: reviewed_date")
        cursor.execute("ALTER TABLE requests ADD COLUMN reviewed_date TEXT")
    
    conn.commit()
    
    # Set default submitted_date for existing records
    cursor.execute("UPDATE requests SET submitted_date = datetime('now') WHERE submitted_date IS NULL")
    conn.commit()
    
    # Verify
    cursor.execute("PRAGMA table_info(requests)")
    updated_columns = [col[1] for col in cursor.fetchall()]
    print("\n📋 Updated columns:", updated_columns)
    
    conn.close()
    print("\n✅ Database fixed successfully!")

if __name__ == '__main__':
    fix_requests_table()