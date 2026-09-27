from modules.database import get_db_connection

def get_all_assets():
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM assets ORDER BY id DESC')
    assets = c.fetchall()
    conn.close()
    return assets

def get_asset_categories():
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    c.execute('SELECT category_name FROM asset_categories')
    categories = [row[0] for row in c.fetchall()]
    conn.close()
    return categories

def get_asset_by_id(asset_id):
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM assets WHERE id = ?', (asset_id,))
    asset = c.fetchone()
    conn.close()
    return asset

def get_asset_stats():
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM assets')
    total = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM assets WHERE status = "Available"')
    available = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM assets WHERE status = "Assigned"')
    assigned = c.fetchone()[0]
    conn.close()
    return {'total': total, 'available': available, 'assigned': assigned}

def add_asset(asset_name, category, serial_number, brand_model, date_of_allotment, date_of_return, cost, remarks):
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    c.execute('''INSERT INTO assets (asset_name, category, serial_number, brand_model, date_of_allotment, date_of_return, cost, remarks, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (asset_name, category, serial_number, brand_model, date_of_allotment, date_of_return, cost, remarks, 'Available'))
    conn.commit()
    conn.close()

def update_asset(asset_id, asset_name, category, serial_number, brand_model, date_of_allotment, date_of_return, cost, remarks):
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    c.execute('''UPDATE assets SET asset_name=?, category=?, serial_number=?, brand_model=?, date_of_allotment=?, date_of_return=?, cost=?, remarks=?
                 WHERE id=?''',
              (asset_name, category, serial_number, brand_model, date_of_allotment, date_of_return, cost, remarks, asset_id))
    conn.commit()
    conn.close()

def delete_asset(asset_id):
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    c.execute('DELETE FROM assets WHERE id = ?', (asset_id,))
    conn.commit()
    conn.close()

def assign_asset(asset_id, employee_id, assigned_date):
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    c.execute('UPDATE assets SET assigned_to=?, assigned_date=?, date_of_allotment=?, status="Assigned" WHERE id=?', (employee_id, assigned_date, assigned_date, asset_id))
    conn.commit()
    conn.close()

def return_asset(asset_id, return_date=None):
    conn = get_db_connection('inventory.db')
    c = conn.cursor()
    if not return_date:
        from datetime import datetime
        return_date = datetime.now().strftime('%Y-%m-%d')
    c.execute('UPDATE assets SET assigned_to=NULL, assigned_date=NULL, date_of_return=?, status="Available" WHERE id=?', (return_date, asset_id))
    conn.commit()
    conn.close()