import sqlite3

def add_attendance_permissions():
    # Connect to users database
    conn = sqlite3.connect('databases/users.db')
    cursor = conn.cursor()
    
    # Check if role_permissions table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='role_permissions'")
    if not cursor.fetchone():
        print("❌ role_permissions table not found!")
        conn.close()
        return
    
    # Get admin role id
    cursor.execute("SELECT id FROM roles WHERE name = 'admin'")
    admin = cursor.fetchone()
    
    if not admin:
        print("❌ Admin role not found!")
        conn.close()
        return
    
    admin_id = admin[0]
    
    # Add attendance permissions for admin
    permissions = ['view_attendance', 'edit_attendance']
    
    for perm in permissions:
        try:
            cursor.execute("INSERT INTO role_permissions (role_id, permission) VALUES (?, ?)", (admin_id, perm))
            print(f"✅ Added permission: {perm} for admin")
        except sqlite3.IntegrityError:
            print(f"⚠️ Permission {perm} already exists")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Attendance permissions added successfully!")

if __name__ == '__main__':
    add_attendance_permissions()