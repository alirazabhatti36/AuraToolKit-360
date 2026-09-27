import sqlite3
import os

def check_request_table():
    db_path = 'databases/requests.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check table structure
    cursor.execute("PRAGMA table_info(requests)")
    columns = cursor.fetchall()
    
    print("=" * 60)
    print("📋 REQUESTS TABLE STRUCTURE:")
    print("=" * 60)
    for col in columns:
        print(f"  {col[0]}: {col[1]} ({col[2]})")
    
    # Check if status column exists
    status_exists = any(col[1] == 'status' for col in columns)
    print(f"\n✅ Status column exists: {status_exists}")
    
    # Sample data
    print("\n" + "=" * 60)
    print("📊 SAMPLE DATA (Last 5 requests):")
    print("=" * 60)
    
    try:
        cursor.execute("SELECT id, request_type, status, submitted_date FROM requests ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(f"  ID: {row[0]}, Type: {row[1]}, Status: {row[2]}, Date: {row[3]}")
        else:
            print("  No requests found in database.")
    except Exception as e:
        print(f"  Error reading data: {e}")
    
    # Count by status
    print("\n" + "=" * 60)
    print("📊 REQUESTS COUNT BY STATUS:")
    print("=" * 60)
    
    try:
        cursor.execute("SELECT status, COUNT(*) FROM requests GROUP BY status")
        stats = cursor.fetchall()
        for stat in stats:
            print(f"  {stat[0]}: {stat[1]}")
    except Exception as e:
        print(f"  Error counting: {e}")
    
    conn.close()

if __name__ == '__main__':
    check_request_table()