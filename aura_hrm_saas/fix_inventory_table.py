import sqlite3
import os

def fix_inventory_table():
    db_path = 'databases/inventory.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check existing columns
    cursor.execute("PRAGMA table_info(assets)")
    columns = [col[1] for col in cursor.fetchall()]
    
    print("📋 Existing columns:", columns)
    
    # Add missing columns if not exist
    if 'date_of_allotment' not in columns:
        print("✅ Adding column: date_of_allotment")
        cursor.execute("ALTER TABLE assets ADD COLUMN date_of_allotment TEXT")
    
    if 'date_of_return' not in columns:
        print("✅ Adding column: date_of_return")
        cursor.execute("ALTER TABLE assets ADD COLUMN date_of_return TEXT")
    
    if 'assigned_to' not in columns:
        print("✅ Adding column: assigned_to")
        cursor.execute("ALTER TABLE assets ADD COLUMN assigned_to INTEGER")
    
    if 'assigned_date' not in columns:
        print("✅ Adding column: assigned_date")
        cursor.execute("ALTER TABLE assets ADD COLUMN assigned_date TEXT")
    
    if 'warranty_until' not in columns:
        print("✅ Adding column: warranty_until")
        cursor.execute("ALTER TABLE assets ADD COLUMN warranty_until TEXT")
    
    if 'purchase_date' not in columns:
        print("✅ Adding column: purchase_date")
        cursor.execute("ALTER TABLE assets ADD COLUMN purchase_date TEXT")
    
    conn.commit()
    
    # Verify
    cursor.execute("PRAGMA table_info(assets)")
    updated_columns = [col[1] for col in cursor.fetchall()]
    print("\n📋 Updated columns:", updated_columns)
    
    conn.close()
    print("\n✅ Inventory database fixed successfully!")

if __name__ == '__main__':
    fix_inventory_table()