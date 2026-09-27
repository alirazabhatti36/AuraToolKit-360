from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, session, make_response
import csv
import io
import math
import os
import ssl
import urllib.error
import urllib.request
from datetime import datetime
from werkzeug.utils import secure_filename

# Import all modules
from modules.database import init_all_dbs
from modules.helpers import get_db_size, get_uploads_size, delete_old_files, delete_all_uploads
from modules.auth import (login_required, permission_required, role_required, superadmin_required, has_permission,
                          get_user_role, get_current_employee_id, get_all_users, add_user,
                          update_user, delete_user, change_user_password, authenticate_user,
                          get_user_by_username, get_user_permissions, verify_password,
                          get_all_companies, add_company, toggle_company_status, get_company_stats)
from modules.ats import (extract_text, extract_location, match_resume, 
                         get_all_candidates, count_by_status, update_candidate_status)
from modules.employees import (get_all_employees, get_employee_by_id, get_active_employees,
                               add_employee, update_employee, delete_employee, search_employees, get_employee_details)
from modules.inventory import (get_all_assets, get_asset_categories, get_asset_stats,
                               add_asset, update_asset, delete_asset, get_asset_by_id,
                               assign_asset, return_asset)
from modules.payroll import (get_all_payroll, get_payroll_stats, get_payroll_by_id,
                             add_payroll, update_payroll, delete_payroll, process_payroll_record)
from modules.weekend import get_all_weekend, get_weekend_stats, add_weekend_bulk, delete_weekend
from modules.attendance import get_today_attendance, get_leave_requests
from modules.activity_logs import log_activity, get_all_logs, get_logs_stats, clear_old_logs
from modules.requests import (get_all_requests, get_pending_requests, get_requests_by_employee,
                              get_requests_stats, add_request, approve_request, reject_request,
                              get_requests_by_status, get_all_requests_with_status)
from modules.increment import (get_all_increments, get_increments_by_team, get_teams as get_increment_teams, get_increment_stats,
                               add_or_update_increment, approve_increment, reject_increment, 
                               implement_increment, bulk_update_increment)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'auratoolkit360_secret_key_super_secure_2026')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

# Create uploads folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize all databases
init_all_dbs()


def build_csv_response(filename, headers, rows):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    return response


# ============= HELPER FOR TEMPLATES =============
@app.context_processor
def utility_processor():
    def check_permission(permission_name):
        try:
            user_id = session.get('user_id')
            return has_permission(user_id, permission_name)
        except Exception:
            return False

    def format_currency(value):
        try:
            return '₨ ' + '{:,.0f}'.format(float(value))
        except Exception:
            return '₨ 0'
    
    current_company = session.get('company_name', 'AuraToolKit 360 Inc')
    return dict(has_permission=check_permission, format_currency=format_currency, current_company=current_company)


# ============= SUPER ADMIN ROUTES =============
@app.route('/superadmin/dashboard')
@login_required
@superadmin_required
def superadmin_dashboard():
    companies = get_all_companies()
    stats = get_company_stats()
    return render_template('superadmin_dashboard.html', companies=companies, stats=stats)

@app.route('/superadmin/company/add', methods=['POST'])
@login_required
@superadmin_required
def add_company_route():
    name = request.form.get('name')
    slug = request.form.get('slug')
    domain = request.form.get('domain', '')
    email = request.form.get('email')
    phone = request.form.get('phone', '')
    plan = request.form.get('plan', 'pro')
    max_employees = request.form.get('max_employees', 100)
    admin_username = request.form.get('admin_username')
    admin_password = request.form.get('admin_password')

    company_id = add_company(name, slug, domain, email, phone, plan, max_employees, admin_username, admin_password)
    if company_id:
        flash(f'✅ Company "{name}" and Admin account registered successfully!', 'success')
    else:
        flash('❌ Error creating company. Slug or email may already exist.', 'danger')
    return redirect(url_for('superadmin_dashboard'))

@app.route('/superadmin/company/toggle/<int:company_id>')
@login_required
@superadmin_required
def toggle_company(company_id):
    toggle_company_status(company_id)
    flash('✅ Company status updated successfully.', 'success')
    return redirect(url_for('superadmin_dashboard'))


# ============= LOGIN ROUTES =============
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        user = authenticate_user(username, password)
        if user:
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['user_role'] = user[6]
            session['user_full_name'] = user[3]
            session['employee_id'] = user[5] if user[5] else 0
            session['company_id'] = user[9] if len(user) > 9 else 1
            session['company_name'] = user[10] if len(user) > 10 else 'AuraToolKit 360 Inc'
            
            log_activity(user[1], 'Login', f'Successful login to {session["company_name"]}')
            
            role_names = {
                'super_admin': 'Super Admin',
                'admin': 'Admin',
                'hr_manager': 'HR Manager',
                'accountant': 'Accountant',
                'management': 'Management',
                'employee': 'Employee'
            }
            flash(f'✅ Welcome {user[3]}! Logged in to {session["company_name"]} as {role_names.get(user[6], user[6])}.', 'success')
            
            if user[6] == 'super_admin':
                return redirect(url_for('superadmin_dashboard'))
            elif user[6] == 'admin':
                return redirect(url_for('dashboard'))
            elif user[6] == 'hr_manager':
                return redirect(url_for('employees'))
            elif user[6] == 'accountant':
                return redirect(url_for('payroll'))
            else:
                return redirect(url_for('dashboard'))
        else:
            log_activity(username, 'Failed Login', f'Failed attempt')
            flash('❌ Invalid username or password!', 'warning')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    log_activity(session.get('username', 'User'), 'Logout', 'User logged out')
    session.clear()
    flash('🔓 You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password_route():
    if request.method == 'POST':
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if new_password != confirm_password:
            flash('❌ New passwords do not match!', 'danger')
            return redirect(url_for('change_password_route'))
        
        user = get_user_by_username(session.get('username'))
        if user and verify_password(user[2], old_password):
            change_user_password(user[0], new_password)
            log_activity(session.get('username'), 'Change Password', 'Password changed')
            flash('✅ Password changed successfully! Please login again.', 'success')
            session.clear()
            return redirect(url_for('login'))
        else:
            flash('❌ Current password is incorrect!', 'danger')
        return redirect(url_for('change_password_route'))
    
    return render_template('change_password.html')


# ============= HOME / LANDING ROUTE =============
@app.route('/')
def home():
    return render_template('landing.html')


# ============= GOOGLE ADSENSE & LEGAL ROUTES =============
@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')

@app.route('/cookie-policy')
def cookie_policy():
    return render_template('cookie_policy.html')

@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

@app.route('/robots.txt')
def robots_txt():
    content = """User-agent: *
Allow: /
Allow: /about-us
Allow: /privacy-policy
Allow: /terms-of-service
Allow: /cookie-policy
Disallow: /superadmin/
Disallow: /dashboard

Sitemap: https://auratoolkit360.com/sitemap.xml"""
    return content, 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap_xml():
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://auratoolkit360.com/</loc><priority>1.0</priority></url>
  <url><loc>https://auratoolkit360.com/about-us</loc><priority>0.8</priority></url>
  <url><loc>https://auratoolkit360.com/privacy-policy</loc><priority>0.7</priority></url>
  <url><loc>https://auratoolkit360.com/terms-of-service</loc><priority>0.7</priority></url>
  <url><loc>https://auratoolkit360.com/cookie-policy</loc><priority>0.6</priority></url>
</urlset>"""
    return content, 200, {'Content-Type': 'application/xml'}

@app.route('/ads.txt')
def ads_txt():
    content = "google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0"
    return content, 200, {'Content-Type': 'text/plain'}


# ============= B2B SELF-ONBOARDING & ENTERPRISE ROUTES =============
@app.route('/register-company', methods=['GET', 'POST'])
def register_company_route():
    if request.method == 'POST':
        company_name = request.form.get('company_name', '').strip()
        domain = request.form.get('domain', '').strip().lower()
        admin_name = request.form.get('admin_name', '').strip()
        admin_email = request.form.get('admin_email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        plan = request.form.get('plan', 'Pro')
        
        if not company_name or not username or not password:
            flash('❌ Please fill in all required fields.', 'danger')
            return redirect(url_for('register_company_route'))
            
        from modules.auth import add_company
        from werkzeug.security import generate_password_hash
        import sqlite3, os
        
        # 1. Add company
        comp_id = add_company(company_name, domain, domain + "@company.com", "0300-0000000", plan)
        
        # 2. Add company admin user
        conn = sqlite3.connect(os.path.join('databases', 'users.db'))
        c = conn.cursor()
        c.execute('''
            INSERT OR IGNORE INTO users (company_id, username, password, full_name, email, employee_id, role, department)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (comp_id, username, generate_password_hash(password), admin_name, admin_email, 0, 'admin', 'Management'))
        conn.commit()
        conn.close()
        
        # 3. Log in automatically
        session['logged_in'] = True
        session['user_id'] = comp_id
        session['username'] = username
        session['user_role'] = 'admin'
        session['company_id'] = comp_id
        session['company_name'] = company_name
        
        flash(f'🎉 Welcome to AuraToolKit 360! Company "{company_name}" successfully registered.', 'success')
        return redirect(url_for('dashboard'))
        
    return render_template('register_company.html')

@app.route('/org-chart')
@login_required
def org_chart_route():
    return render_template('org_chart.html')

@app.route('/invoices')
@login_required
def invoices_route():
    return render_template('invoices.html')

@app.route('/demo-login')
def demo_login_route():
    session['logged_in'] = True
    session['user_id'] = 1
    session['username'] = 'demo_admin'
    session['user_full_name'] = 'Demo Admin'
    session['user_role'] = 'admin'
    session['company_id'] = 1
    session['company_name'] = 'AuraToolKit 360 Demo Corp'
    
    flash('🎮 Welcome to Instant Live Demo Mode! Exploring AuraToolKit 360 Tenant Portal.', 'info')
    return redirect(url_for('dashboard'))

@app.route('/leave-calendar')
@login_required
def leave_calendar_route():
    return render_template('leave_calendar.html')


# ============= API ROUTES =============
@app.route('/api/search-employees')
@login_required
def api_search_employees():
    search_term = request.args.get('q', '')
    if len(search_term) < 2:
        return jsonify({'employees': []})
    
    employees = search_employees(search_term)
    emp_list = []
    for e in employees:
        emp_list.append({
            'id': e[0],
            'name': e[1],
            'team': e[2],
            'position': e[3],
            'salary': float(e[4]) if e[4] else 0,
            'petrol_allowance': float(e[5]) if e[5] else 0,
            'bank_name': e[6] or '',
            'account_number': e[7] or ''
        })
    return jsonify({'employees': emp_list})

@app.route('/api/employee-details/<int:employee_id>')
@login_required
def api_employee_details(employee_id):
    details = get_employee_details(employee_id)
    if details:
        return jsonify({'success': True, 'employee': details})
    return jsonify({'success': False, 'message': 'Employee not found'})


# ============= ATS ROUTES =============
@app.route('/ats')
@login_required
@permission_required('view_ats')
def ats():
    return render_template('ats.html', db_size=get_db_size(), 
                          uploads_size=get_uploads_size(), 
                          today_date=datetime.now().strftime('%Y-%m-%d'))

@app.route('/ats-upload', methods=['POST'])
@login_required
@permission_required('edit_ats')
def ats_upload():
    from modules.database import get_db_connection
    
    job_title = request.form.get('job_title', 'Not specified')
    keywords_text = request.form.get('keywords', '')
    received_date = request.form.get('received_date', datetime.now().strftime('%Y-%m-%d'))
    keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]
    
    try:
        received_date = datetime.strptime(received_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    except:
        received_date = datetime.now().strftime('%d-%m-%Y')
    
    files = request.files.getlist('resumes')
    conn = get_db_connection('candidates.db')
    c = conn.cursor()
    
    for file in files:
        if file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            text = extract_text(filepath)
            if text:
                location = extract_location(text)
                matched, score = match_resume(text, keywords)
            else:
                location = "Not specified"
                matched, score = [], 0
            c.execute('''INSERT INTO candidates (filename, location, received_date, score, matched_keywords, status, job_title)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (filename, location, received_date, score, ','.join(matched), 'pending', job_title))
    conn.commit()
    conn.close()
    delete_old_files()
    log_activity(session.get('username'), 'Upload Resume', f'Uploaded {len(files)} resume(s) for {job_title}')
    flash(f'✅ {len(files)} resume(s) uploaded!', 'success')
    return redirect(url_for('ats_dashboard'))

@app.route('/ats-dashboard')
@login_required
@permission_required('view_ats')
def ats_dashboard():
    status_filter = request.args.get('status', 'all')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    candidates = get_all_candidates()
    if status_filter != 'all':
        candidates = [c for c in candidates if c[6] == status_filter]

    total_items = len(candidates)
    total_pages = max(1, math.ceil(total_items / per_page))
    page = min(max(page, 1), total_pages)
    start = (page - 1) * per_page
    page_candidates = candidates[start:start + per_page]

    return render_template('ats_dashboard.html', 
                          candidates=page_candidates,
                          total=total_items,
                          shortlisted=count_by_status('shortlisted'),
                          pending=count_by_status('pending'),
                          rejected=count_by_status('rejected'),
                          status_filter=status_filter,
                          page=page,
                          total_pages=total_pages,
                          per_page=per_page)

@app.route('/ats-shortlist/<int:candidate_id>')
@login_required
@permission_required('edit_ats')
def ats_shortlist(candidate_id):
    status_filter = request.args.get('status', 'all')
    page = request.args.get('page', 1, type=int)
    log_activity(session.get('username'), 'Shortlist Candidate', f'Shortlisted candidate ID: {candidate_id}')
    update_candidate_status(candidate_id, 'shortlisted')
    flash('⭐ Candidate shortlisted!', 'success')
    return redirect(url_for('ats_dashboard', status=status_filter, page=page))

@app.route('/ats-reject/<int:candidate_id>')
@login_required
@permission_required('edit_ats')
def ats_reject(candidate_id):
    status_filter = request.args.get('status', 'all')
    page = request.args.get('page', 1, type=int)
    log_activity(session.get('username'), 'Reject Candidate', f'Rejected candidate ID: {candidate_id}')
    update_candidate_status(candidate_id, 'rejected')
    flash('❌ Candidate rejected', 'info')
    return redirect(url_for('ats_dashboard', status=status_filter, page=page))

@app.route('/ats-hire/<int:candidate_id>')
@login_required
@permission_required('edit_ats')
def ats_hire(candidate_id):
    status_filter = request.args.get('status', 'all')
    page = request.args.get('page', 1, type=int)
    from modules.database import get_db_connection
    
    conn = get_db_connection('candidates.db')
    c = conn.cursor()
    c.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,))
    candidate = c.fetchone()
    conn.close()
    
    if candidate:
        name = candidate[1].replace('_', ' ').replace('.pdf', '').replace('.docx', '').title()
        add_employee(name, "", "", candidate[7], "", datetime.now().strftime('%Y-%m-%d'), 
                    "", "0", candidate[2], candidate[1], 'Permanent', '', '', '')
        update_candidate_status(candidate_id, 'hired')
        log_activity(session.get('username'), 'Hire Candidate', f'Hired {name} from ATS')
        flash(f'🎉 {name} hired and added to Employees!', 'success')
    return redirect(url_for('ats_dashboard'))


# ============= EMPLOYEE ROUTES =============
@app.route('/employees')
@login_required
@permission_required('view_employees')
def employees():
    employee_type = request.args.get('employee_type', 'all')
    emps = get_all_employees()
    if employee_type != 'all':
        emps = [e for e in emps if len(e) > 11 and e[11] == employee_type]
    total = len(emps)
    permanent = len([e for e in get_all_employees() if len(e) > 11 and e[11] == 'Permanent'])
    probation = len([e for e in get_all_employees() if len(e) > 11 and e[11] == 'Probation'])
    intern = len([e for e in get_all_employees() if len(e) > 11 and e[11] == 'Intern'])
    return render_template('employees.html', employees=emps, total=total,
                          permanent=permanent, probation=probation, intern=intern,
                          selected_type=employee_type)


@app.route('/export-employees')
@login_required
@permission_required('view_employees')
def export_employees():
    emps = get_all_employees()
    headers = ['ID', 'Name', 'Email', 'Phone', 'Position', 'Department', 'Joining Date', 'Salary', 'Petrol Allowance', 'Location', 'CV', 'Employee Type', 'CNIC', 'Bank Name', 'Account Number']
    rows = []
    for emp in emps:
        rows.append(list(emp[:15]))
    return build_csv_response('employees.csv', headers, rows)

@app.route('/add-employee', methods=['POST'])
@login_required
@permission_required('edit_employees')
def add_employee_route():
    name = request.form.get('name', '')
    add_employee(
        name=name,
        email=request.form.get('email', ''),
        phone=request.form.get('phone', ''),
        position=request.form.get('position', ''),
        department=request.form.get('department', ''),
        joining_date=request.form.get('joining_date', ''),
        salary=request.form.get('salary', ''),
        petrol_allowance=request.form.get('petrol_allowance', '0'),
        location=request.form.get('location', ''),
        cv_filename='',
        employee_type=request.form.get('employee_type', 'Probation'),
        cnic=request.form.get('cnic', ''),
        bank_name=request.form.get('bank_name', ''),
        account_number=request.form.get('account_number', '')
    )
    log_activity(session.get('username'), 'Add Employee', f'Added employee: {name}')
    flash('✅ Employee added!', 'success')
    return redirect(url_for('employees'))

@app.route('/edit-employee/<int:employee_id>')
@login_required
@permission_required('view_employees')
def edit_employee(employee_id):
    emp = get_employee_by_id(employee_id)
    return render_template('edit_employee.html', employee=emp) if emp else redirect(url_for('employees'))

@app.route('/update-employee/<int:employee_id>', methods=['POST'])
@login_required
@permission_required('edit_employees')
def update_employee_route(employee_id):
    name = request.form.get('name', '')
    update_employee(
        employee_id,
        name=name,
        email=request.form.get('email', ''),
        phone=request.form.get('phone', ''),
        position=request.form.get('position', ''),
        department=request.form.get('department', ''),
        joining_date=request.form.get('joining_date', ''),
        salary=request.form.get('salary', ''),
        petrol_allowance=request.form.get('petrol_allowance', '0'),
        location=request.form.get('location', ''),
        employee_type=request.form.get('employee_type', 'Probation'),
        cnic=request.form.get('cnic', ''),
        bank_name=request.form.get('bank_name', ''),
        account_number=request.form.get('account_number', '')
    )
    log_activity(session.get('username'), 'Edit Employee', f'Updated employee: {name}')
    flash('✅ Employee updated!', 'success')
    return redirect(url_for('employees'))

@app.route('/delete-employee/<int:employee_id>')
@login_required
@permission_required('delete_employees')
def delete_employee_route(employee_id):
    emp = get_employee_by_id(employee_id)
    if emp:
        delete_employee(employee_id)
        log_activity(session.get('username'), 'Delete Employee', f'Deleted employee: {emp[1]}')
        flash(f'❌ Employee {emp[1]} deleted!', 'info')
    return redirect(url_for('employees'))


# ============= ATTENDANCE ROUTES =============
@app.route('/attendance')
@login_required
def attendance():
    # Allow access if user is an employee (self-service) or has the view_attendance permission
    if session.get('user_role') != 'employee' and not has_permission(session.get('user_id'), 'view_attendance'):
        flash('🔒 You do not have permission to view attendance.', 'danger')
        return redirect(url_for('dashboard'))

    from modules.database import get_db_connection

    conn = get_db_connection('attendance.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            employee_name TEXT,
            date TEXT,
            status TEXT,
            check_in TEXT,
            check_out TEXT,
            remarks TEXT
        )
    ''')
    conn.commit()
    
    # Get all attendance records
    cursor.execute('''
        SELECT id, employee_id, employee_name, date, status, check_in, check_out, remarks
        FROM attendance
        ORDER BY date DESC
        LIMIT 100
    ''')
    attendances = cursor.fetchall()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_row = cursor.fetchone()
    total = total_row[0] if total_row else 0
    
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'present'")
    present_row = cursor.fetchone()
    present = present_row[0] if present_row else 0
    
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'absent'")
    absent_row = cursor.fetchone()
    absent = absent_row[0] if absent_row else 0
    
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'late'")
    late_row = cursor.fetchone()
    late = late_row[0] if late_row else 0
    
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'half_day'")
    half_day_row = cursor.fetchone()
    half_day = half_day_row[0] if half_day_row else 0
    
    conn.close()
    
    employees = get_all_employees()
    
    # Create stats dictionary
    stats = {
        'total': total,
        'present': present,
        'absent': absent,
        'late': late,
        'half_day': half_day
    }
    
    return render_template('attendance.html',
                          attendances=attendances,
                          employees=employees,
                          stats=stats,
                          current_date=datetime.now().strftime('%Y-%m-%d'))


@app.route('/sync-hikvision', methods=['POST'])
@login_required
@permission_required('edit_attendance')
def sync_hikvision():
    flash('ℹ️ Hikvision device sync is disabled. Please add attendance manually.', 'info')
    return redirect(url_for('attendance'))


@app.route('/sync-hikvision-manual')
@login_required
@permission_required('edit_attendance')
def sync_hikvision_manual():
    flash('ℹ️ Hikvision device sync is disabled. Please add attendance manually.', 'info')
    return redirect(url_for('attendance'))


@app.route('/hikvision-test')
@login_required
def hikvision_test():
    return jsonify({'status': 'disabled', 'message': 'Hikvision device integration is disabled. Use manual attendance entry.'})


@app.route('/upload-hikvision-report', methods=['POST'])
@login_required
@permission_required('edit_attendance')
def upload_hikvision_report():
    flash('ℹ️ Hikvision report import is disabled. Please add attendance manually.', 'info')
    return redirect(url_for('attendance'))


@app.route('/mark-attendance', methods=['POST'])
@login_required
def mark_attendance():
    # Only allow employees (self) or roles with edit_attendance permission to mark attendance
    if session.get('user_role') != 'employee' and not has_permission(session.get('user_id'), 'edit_attendance'):
        flash('🔒 You do not have permission to mark attendance.', 'danger')
        return redirect(url_for('attendance'))

    from modules.database import get_db_connection
    
    employee_id = request.form.get('employee_id')
    employee_name = request.form.get('employee_name')
    date = request.form.get('date')
    status = request.form.get('status')
    check_in = request.form.get('check_in', '')
    check_out = request.form.get('check_out', '')
    remarks = request.form.get('remarks', '')
    
    conn = get_db_connection('attendance.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            employee_name TEXT,
            date TEXT,
            status TEXT,
            check_in TEXT,
            check_out TEXT,
            remarks TEXT
        )
    ''')
    conn.commit()
    
    # Check if attendance already marked
    cursor.execute("SELECT id FROM attendance WHERE employee_id = ? AND date = ?", (employee_id, date))
    existing = cursor.fetchone()
    
    if existing:
        cursor.execute('''
            UPDATE attendance 
            SET status = ?, check_in = ?, check_out = ?, remarks = ?
            WHERE employee_id = ? AND date = ?
        ''', (status, check_in, check_out, remarks, employee_id, date))
        flash('✅ Attendance updated!', 'success')
    else:
        cursor.execute('''
            INSERT INTO attendance (employee_id, employee_name, date, status, check_in, check_out, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (employee_id, employee_name, date, status, check_in, check_out, remarks))
        flash('✅ Attendance marked!', 'success')
    
    conn.commit()
    conn.close()
    
    log_activity(session.get('username'), 'Mark Attendance', f'Marked attendance for {employee_name} on {date}')
    
    return redirect(url_for('attendance'))


@app.route('/attendance-report')
@login_required
def attendance_report():
    from modules.database import get_db_connection

    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    year = request.args.get('year', datetime.now().strftime('%Y'))
    date_filter = request.args.get('date', '')
    employee_id = request.args.get('employee_id', 'all')
    status_filter = request.args.get('status', 'all')

    conn = get_db_connection('attendance.db')
    cursor = conn.cursor()

    query = '''
        SELECT id, employee_id, employee_name, date, status, check_in, check_out, remarks
        FROM attendance
        WHERE 1=1
    '''
    params = []

    if date_filter:
        query += ' AND date = ?'
        params.append(date_filter)
    else:
        if month and month != 'all':
            query += " AND strftime('%Y-%m', date) = ?"
            params.append(month)
        if year and year != 'all':
            query += " AND strftime('%Y', date) = ?"
            params.append(year)

    if employee_id != 'all':
        query += ' AND employee_id = ?'
        params.append(int(employee_id))

    if status_filter != 'all':
        query += ' AND lower(status) = ?'
        params.append(status_filter.lower())

    query += ' ORDER BY date DESC'
    cursor.execute(query, params)
    attendances = cursor.fetchall()
    conn.close()

    employees = get_all_employees()
    years = [datetime.now().year - i for i in range(5)]
    months = [
        {'value': f'{year}-01', 'name': 'January'} for year in years
    ]
    summary = {
        'total': len(attendances),
        'present': sum(1 for a in attendances if str(a[4]).lower() == 'present'),
        'late': sum(1 for a in attendances if str(a[4]).lower() == 'late'),
        'absent': sum(1 for a in attendances if str(a[4]).lower() == 'absent'),
        'half_day': sum(1 for a in attendances if str(a[4]).lower() == 'half_day'),
        'wfh': sum(1 for a in attendances if str(a[4]).lower() == 'wfh'),
    }

    return render_template('attendance_report.html',
                          attendance=attendances,
                          employees=employees,
                          month=month,
                          year=year,
                          date_filter=date_filter,
                          selected_employee=employee_id,
                          selected_status=status_filter,
                          summary=summary,
                          months=months,
                          years=years)


@app.route('/export-attendance')
@login_required
def export_attendance():
    from modules.database import get_db_connection

    month = request.args.get('month', datetime.now().strftime('%Y-%m'))
    year = request.args.get('year', datetime.now().strftime('%Y'))
    date_filter = request.args.get('date', '')
    employee_id = request.args.get('employee_id', 'all')
    status_filter = request.args.get('status', 'all')

    conn = get_db_connection('attendance.db')
    cursor = conn.cursor()
    query = '''
        SELECT id, employee_id, employee_name, date, status, check_in, check_out, remarks
        FROM attendance
        WHERE 1=1
    '''
    params = []
    if date_filter:
        query += ' AND date = ?'
        params.append(date_filter)
    else:
        if month and month != 'all':
            query += " AND strftime('%Y-%m', date) = ?"
            params.append(month)
        if year and year != 'all':
            query += " AND strftime('%Y', date) = ?"
            params.append(year)
    if employee_id != 'all':
        query += ' AND employee_id = ?'
        params.append(int(employee_id))
    if status_filter != 'all':
        query += ' AND lower(status) = ?'
        params.append(status_filter.lower())
    query += ' ORDER BY date DESC'
    cursor.execute(query, params)
    attendances = cursor.fetchall()
    conn.close()

    headers = ['ID', 'Employee ID', 'Employee Name', 'Date', 'Status', 'Check In', 'Check Out', 'Remarks']
    rows = [
        [a[0], a[1], a[2], a[3], a[4], a[5] or '', a[6] or '', a[7] or '']
        for a in attendances
    ]
    return build_csv_response('attendance_report.csv', headers, rows)


# ============= INVENTORY ROUTES =============
@app.route('/inventory')
@login_required
@permission_required('view_inventory')
def inventory():
    return render_template('inventory.html', 
                          assets=get_all_assets(), 
                          stats=get_asset_stats(),
                          categories=get_asset_categories(), 
                          active_employees=get_active_employees(),
                          get_employee_by_id=get_employee_by_id)

@app.route('/add-asset', methods=['POST'])
@login_required
@permission_required('edit_inventory')
def add_asset_route():
    asset_name = request.form.get('asset_name', '')
    add_asset(asset_name, request.form.get('category',''),
             request.form.get('serial_number',''), request.form.get('brand_model',''),
             request.form.get('purchase_date',''), request.form.get('warranty_until',''),
             request.form.get('cost',''), request.form.get('remarks',''))
    log_activity(session.get('username'), 'Add Asset', f'Added asset: {asset_name}')
    flash('✅ Asset added!', 'success')
    return redirect(url_for('inventory'))

@app.route('/edit-asset/<int:asset_id>')
@login_required
@permission_required('view_inventory')
def edit_asset(asset_id):
    asset = get_asset_by_id(asset_id)
    return render_template('edit_asset.html', asset=asset) if asset else redirect(url_for('inventory'))

@app.route('/update-asset/<int:asset_id>', methods=['POST'])
@login_required
@permission_required('edit_inventory')
def update_asset_route(asset_id):
    asset_name = request.form.get('asset_name', '')
    update_asset(asset_id, asset_name, request.form.get('category',''),
                request.form.get('serial_number',''), request.form.get('brand_model',''),
                request.form.get('purchase_date',''), request.form.get('warranty_until',''),
                request.form.get('cost',''), request.form.get('remarks',''))
    log_activity(session.get('username'), 'Edit Asset', f'Updated asset: {asset_name}')
    flash('✅ Asset updated!', 'success')
    return redirect(url_for('inventory'))

@app.route('/delete-asset/<int:asset_id>')
@login_required
@permission_required('delete_inventory')
def delete_asset_route(asset_id):
    asset = get_asset_by_id(asset_id)
    if asset:
        delete_asset(asset_id)
        log_activity(session.get('username'), 'Delete Asset', f'Deleted asset: {asset[1]}')
        flash(f'❌ Asset {asset[1]} deleted!', 'info')
    return redirect(url_for('inventory'))

@app.route('/assign-asset', methods=['POST'])
@login_required
@permission_required('edit_inventory')
def assign_asset_route():
    assign_asset(request.form.get('asset_id',''), request.form.get('employee_id',''),
                request.form.get('assigned_date',''))
    log_activity(session.get('username'), 'Assign Asset', f'Assigned asset to employee')
    flash('✅ Asset assigned!', 'success')
    return redirect(url_for('inventory'))

@app.route('/return-asset/<int:asset_id>')
@login_required
@permission_required('edit_inventory')
def return_asset_route(asset_id):
    return_asset(asset_id)
    log_activity(session.get('username'), 'Return Asset', f'Asset returned')
    flash('✅ Asset returned!', 'success')
    return redirect(url_for('inventory'))


# ============= PAYROLL ROUTES =============
@app.route('/payroll')
@login_required
@permission_required('view_payroll')
def payroll():
    payrolls = get_all_payroll()
    stats = get_payroll_stats()
    return render_template('payroll.html', payrolls=payrolls, stats=stats, team_stats=stats.get('team_stats', []))


@app.route('/export-payroll')
@login_required
@permission_required('view_payroll')
def export_payroll():
    payrolls = get_all_payroll()
    headers = ['ID', 'Team', 'Employee', 'Basic Salary', 'Petrol Allowance', 'Additional Earnings', 'Gross Salary', 'Income Tax', 'Other Deductions', 'Net Salary', 'Month', 'Year', 'Status']
    rows = []
    for p in payrolls:
        rows.append([p[0], p[2], p[3], p[5], p[6], p[7], p[8], p[9], p[10], p[12], p[18], p[19], p[20]])
    return build_csv_response('payroll.csv', headers, rows)

@app.route('/add-payroll', methods=['POST'])
@login_required
@permission_required('edit_payroll')
def add_payroll_route():
    try:
        def safe_float(value, default=0):
            if value is None or value == '':
                return default
            try:
                return float(value)
            except:
                return default
        
        def safe_int(value, default=0):
            if value is None or value == '':
                return default
            try:
                return int(value)
            except:
                return default
        
        employee_id = safe_int(request.form.get('employee_id', 0))
        employee_name = request.form.get('employee_name', '')
        month = request.form.get('month', '')
        year = request.form.get('year', '')
        
        if employee_id > 0:
            emp_details = get_employee_details(employee_id)
            if emp_details:
                petrol_from_employee = emp_details.get('petrol_allowance', 0)
            else:
                petrol_from_employee = 0
        else:
            petrol_from_employee = 0
        
        basic = safe_float(request.form.get('basic_salary'))
        petrol = safe_float(request.form.get('petrol_allowance')) if safe_float(request.form.get('petrol_allowance')) > 0 else petrol_from_employee
        additional = safe_float(request.form.get('additional_earnings'))
        income_tax = safe_float(request.form.get('income_tax'))
        other_deductions = safe_float(request.form.get('other_deductions'))
        
        gross = basic + petrol + additional
        net = gross - (income_tax + other_deductions)
        
        payment_method = request.form.get('payment_method', 'cash')
        bank_salary = safe_float(request.form.get('bank_salary'))
        cash_salary = safe_float(request.form.get('cash_salary'))
        
        if payment_method == 'cash':
            cash_salary = net
            bank_salary = 0
        elif payment_method == 'bank':
            bank_salary = net
            cash_salary = 0
        elif payment_method == 'both':
            if abs(bank_salary + cash_salary - net) > 1:
                bank_salary = net / 2
                cash_salary = net / 2
        
        data = {
            'employee_id': employee_id,
            'team': request.form.get('team', ''),
            'employee_name': employee_name,
            'working_days': 30,
            'basic_salary': basic,
            'petrol_allowance': petrol,
            'additional_earnings': additional,
            'gross_salary': gross,
            'income_tax': income_tax,
            'other_deductions': other_deductions,
            'leaves': safe_int(request.form.get('leaves', 0)),
            'net_salary': net,
            'bank_salary': bank_salary,
            'cash_salary': cash_salary,
            'remarks': request.form.get('remarks', ''),
            'bank_name': request.form.get('bank_name', ''),
            'account_number': request.form.get('account_number', ''),
            'month': month,
            'year': year,
            'status': request.form.get('status', 'Pending')
        }
        add_payroll(data)
        log_activity(session.get('username'), 'Add Payroll', f'Added payroll for {employee_name} - {month}/{year}')
        flash('✅ Payroll added successfully!', 'success')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'error')
    return redirect(url_for('payroll'))

@app.route('/edit-payroll/<int:payroll_id>')
@login_required
@permission_required('view_payroll')
def edit_payroll(payroll_id):
    payroll = get_payroll_by_id(payroll_id)
    if payroll:
        return render_template('edit_payroll.html', payroll=payroll)
    flash('Payroll record not found', 'error')
    return redirect(url_for('payroll'))

@app.route('/update-payroll/<int:payroll_id>', methods=['POST'])
@login_required
@permission_required('edit_payroll')
def update_payroll_route(payroll_id):
    try:
        def safe_float(value, default=0):
            if value is None or value == '':
                return default
            try:
                return float(value)
            except:
                return default
        
        basic = safe_float(request.form.get('basic_salary'))
        petrol = safe_float(request.form.get('petrol_allowance'))
        additional = safe_float(request.form.get('additional_earnings'))
        income_tax = safe_float(request.form.get('income_tax'))
        other_deductions = safe_float(request.form.get('other_deductions'))
        
        gross = basic + petrol + additional
        net = gross - (income_tax + other_deductions)
        
        data = {
            'employee_id': 0,
            'team': request.form.get('team', ''),
            'employee_name': request.form.get('employee_name', ''),
            'working_days': 30,
            'basic_salary': basic,
            'petrol_allowance': petrol,
            'additional_earnings': additional,
            'gross_salary': gross,
            'income_tax': income_tax,
            'other_deductions': other_deductions,
            'leaves': int(request.form.get('leaves', 0)) if request.form.get('leaves', '0') else 0,
            'net_salary': net,
            'bank_salary': safe_float(request.form.get('bank_salary')),
            'cash_salary': safe_float(request.form.get('cash_salary')),
            'remarks': request.form.get('remarks', ''),
            'bank_name': request.form.get('bank_name', ''),
            'account_number': request.form.get('account_number', ''),
            'month': request.form.get('month', ''),
            'year': request.form.get('year', ''),
            'status': request.form.get('status', 'Pending')
        }
        update_payroll(payroll_id, data)
        log_activity(session.get('username'), 'Edit Payroll', f'Updated payroll ID: {payroll_id}')
        flash('✅ Payroll updated successfully!', 'success')
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'error')
    return redirect(url_for('payroll'))

@app.route('/delete-payroll/<int:payroll_id>')
@login_required
@permission_required('delete_payroll')
def delete_payroll_route(payroll_id):
    delete_payroll(payroll_id)
    log_activity(session.get('username'), 'Delete Payroll', f'Deleted payroll ID: {payroll_id}')
    flash('❌ Payroll record deleted!', 'info')
    return redirect(url_for('payroll'))

@app.route('/process-payroll/<int:payroll_id>')
@login_required
@permission_required('edit_payroll')
def process_payroll_route(payroll_id):
    process_payroll_record(payroll_id)
    log_activity(session.get('username'), 'Process Payroll', f'Processed payroll ID: {payroll_id}')
    flash('✅ Payroll processed and marked as Paid!', 'success')
    return redirect(url_for('payroll'))


# ============= WEEKEND ROUTES =============
@app.route('/weekend')
@login_required
@permission_required('view_weekend')
def weekend():
    weekend = get_all_weekend()
    stats = get_weekend_stats()
    employees = get_all_employees()
    return render_template('weekend.html', weekend=weekend, stats=stats, employees=employees)

@app.route('/add-weekend-bulk', methods=['POST'])
@login_required
@permission_required('edit_weekend')
def add_weekend_bulk_route():
    employee_ids = request.form.getlist('employee_id[]')
    employee_names = request.form.getlist('employee_name[]')
    teams = request.form.getlist('team[]')
    weekend_counts = request.form.getlist('weekend_count[]')
    month = request.form.get('month')
    year = request.form.get('year')
    
    entries = []
    for i in range(len(employee_ids)):
        if employee_ids[i] and weekend_counts[i] and int(weekend_counts[i]) > 0:
            entries.append({
                'employee_id': int(employee_ids[i]),
                'employee_name': employee_names[i],
                'team': teams[i],
                'weekend_count': int(weekend_counts[i])
            })
    
    if entries:
        add_weekend_bulk(entries, month, year)
        log_activity(session.get('username'), 'Add Weekend', f'Added {len(entries)} weekend entries for {month}/{year}')
        flash(f'✅ {len(entries)} weekend entries added! Payroll updated automatically.', 'success')
    else:
        flash('❌ No valid entries found.', 'error')
    
    return redirect(url_for('weekend'))

@app.route('/export-weekend')
@login_required
@permission_required('view_weekend')
def export_weekend():
    weekend = get_all_weekend()
    headers = ['ID', 'Employee ID', 'Employee Name', 'Team', 'Weekend Days', 'Month', 'Year', 'Amount']
    rows = []
    for w in weekend:
        rows.append([w[0], w[1], w[2], w[3], w[4], w[5], w[6], w[7]])
    return build_csv_response('weekend.csv', headers, rows)


@app.route('/delete-weekend/<int:weekend_id>')
@login_required
@permission_required('edit_weekend')
def delete_weekend_route(weekend_id):
    delete_weekend(weekend_id)
    log_activity(session.get('username'), 'Delete Weekend', f'Deleted weekend entry ID: {weekend_id}')
    flash('❌ Weekend entry deleted! Payroll updated automatically.', 'info')
    return redirect(url_for('weekend'))


# ============= REQUESTS ROUTES =============
@app.route('/my-requests')
@login_required
def my_requests():
    employee_id = get_current_employee_id()
    status_filter = request.args.get('status', 'all')
    requests = get_requests_by_employee(employee_id) if employee_id > 0 else []
    if status_filter != 'all':
        requests = [r for r in requests if r[8] == status_filter]
    stats = get_requests_stats()
    return render_template('requests.html', requests=requests, stats=stats, selected_status=status_filter)

@app.route('/add-request', methods=['POST'])
@login_required
def add_request_route():
    employee_id = get_current_employee_id()
    employee_name = session.get('user_full_name', 'Employee')
    request_type = request.form.get('request_type', '')
    subject = request.form.get('subject', '')
    description = request.form.get('description', '')
    start_date = request.form.get('start_date', '')
    end_date = request.form.get('end_date', '')
    
    add_request(employee_id, employee_name, request_type, subject, description, start_date, end_date)
    log_activity(session.get('username'), 'Add Request', f'Added {request_type} request')
    flash('✅ Request submitted successfully!', 'success')
    return redirect(url_for('my_requests'))

@app.route('/pending-requests')
@login_required
@permission_required('approve_requests')
def pending_requests():
    pending = get_requests_by_status('pending')
    approved = get_requests_by_status('approved')
    rejected = get_requests_by_status('rejected')
    stats = get_requests_stats()
    return render_template('pending_requests.html', 
                          pending=pending, 
                          approved=approved, 
                          rejected=rejected,
                          stats=stats)


@app.route('/export-pending-requests')
@login_required
@permission_required('approve_requests')
def export_pending_requests():
    pending = get_requests_by_status('pending')
    approved = get_requests_by_status('approved')
    rejected = get_requests_by_status('rejected')
    rows = []
    for req in pending + approved + rejected:
        rows.append([req[0], req[2], req[3], req[4], req[6] or '', req[7] or '', req[8], req[10] or '', req[11] or '', req[13][:10] if req[13] else ''])
    headers = ['ID', 'Employee', 'Type', 'Subject', 'Start Date', 'End Date', 'Status', 'Reviewer', 'Remarks', 'Date']
    return build_csv_response('pending_requests.csv', headers, rows)

@app.route('/approve-request/<int:request_id>', methods=['POST'])
@login_required
@permission_required('approve_requests')
def approve_request_route(request_id):
    reviewer_id = session.get('user_id', 0)
    reviewer_name = session.get('user_full_name', 'Admin')
    remarks = request.form.get('remarks', '')
    
    approve_request(request_id, reviewer_id, reviewer_name, remarks)
    log_activity(session.get('username'), 'Approve Request', f'Approved request ID: {request_id}')
    flash('✅ Request approved!', 'success')
    return redirect(url_for('pending_requests'))

@app.route('/reject-request/<int:request_id>', methods=['POST'])
@login_required
@permission_required('approve_requests')
def reject_request_route(request_id):
    reviewer_id = session.get('user_id', 0)
    reviewer_name = session.get('user_full_name', 'Admin')
    remarks = request.form.get('remarks', '')
    
    reject_request(request_id, reviewer_id, reviewer_name, remarks)
    log_activity(session.get('username'), 'Reject Request', f'Rejected request ID: {request_id}')
    flash('❌ Request rejected!', 'info')
    return redirect(url_for('pending_requests'))

@app.route('/all-requests-report')
@login_required
@permission_required('approve_requests')
def all_requests_report():
    requests = get_all_requests_with_status()
    stats = get_requests_stats()
    return render_template('all_requests_report.html', requests=requests, stats=stats)


# ============= INCREMENT SHEET ROUTES =============
@app.route('/increment-sheet')
@login_required
@permission_required('view_increment')
def increment_sheet():
    increments = get_all_increments()
    teams = get_increment_teams()
    stats = get_increment_stats()
    
    return render_template('increment_sheet.html', 
                          increments=increments,
                          teams=teams,
                          stats=stats,
                          today_date=datetime.now().strftime('%Y-%m-%d'))

@app.route('/increment-sheet/team/<team_name>')
@login_required
@permission_required('view_increment')
def increment_sheet_by_team(team_name):
    increments = get_increments_by_team(team_name)
    teams = get_increment_teams()
    stats = get_increment_stats()
    
    return render_template('increment_sheet.html', 
                          increments=increments,
                          teams=teams,
                          stats=stats,
                          current_team=team_name,
                          today_date=datetime.now().strftime('%Y-%m-%d'))

@app.route('/update-increment', methods=['POST'])
@login_required
@permission_required('edit_increment')
def update_increment():
    employee_id = request.form.get('employee_id')
    employee_name = request.form.get('employee_name')
    team = request.form.get('team')
    current_salary = float(request.form.get('current_salary', 0))
    increment_percent = float(request.form.get('increment_percent', 0))
    new_salary = current_salary * (1 + increment_percent / 100)
    last_increment_date = request.form.get('last_increment_date')
    next_increment_date = request.form.get('next_increment_date')
    effective_date = request.form.get('effective_date')
    reason = request.form.get('reason')
    remarks = request.form.get('remarks', '')
    
    add_or_update_increment(employee_id, employee_name, team, current_salary, 
                           increment_percent, new_salary, last_increment_date,
                           next_increment_date, effective_date, reason, remarks)
    
    log_activity(session.get('username'), 'Update Increment', f'Updated increment for {employee_name}')
    flash('✅ Increment updated successfully!', 'success')
    
    return redirect(url_for('increment_sheet'))

@app.route('/approve-increment/<int:increment_id>', methods=['POST'])
@login_required
@permission_required('approve_increment')
def approve_increment_route(increment_id):
    approved_by = session.get('user_full_name', 'Admin')
    remarks = request.form.get('remarks', '')
    
    approve_increment(increment_id, approved_by, remarks)
    log_activity(session.get('username'), 'Approve Increment', f'Approved increment ID: {increment_id}')
    flash('✅ Increment approved!', 'success')
    
    return redirect(url_for('increment_sheet'))

@app.route('/reject-increment/<int:increment_id>', methods=['POST'])
@login_required
@permission_required('approve_increment')
def reject_increment_route(increment_id):
    remarks = request.form.get('remarks', '')
    
    reject_increment(increment_id, remarks)
    log_activity(session.get('username'), 'Reject Increment', f'Rejected increment ID: {increment_id}')
    flash('❌ Increment rejected!', 'info')
    
    return redirect(url_for('increment_sheet'))

@app.route('/bulk-increment', methods=['POST'])
@login_required
@permission_required('edit_increment')
def bulk_increment():
    team = request.form.get('team')
    increment_percent = float(request.form.get('increment_percent', 0))
    effective_date = request.form.get('effective_date')
    reason = request.form.get('reason')
    
    affected = bulk_update_increment(team, increment_percent, effective_date, reason)
    
    log_activity(session.get('username'), 'Bulk Increment', f'Applied {increment_percent}% increment to {team} team ({affected} employees)')
    flash(f'✅ {affected} employees updated in {team} team!', 'success')
    
    return redirect(url_for('increment_sheet'))

@app.route('/implement-increment/<int:increment_id>')
@login_required
@permission_required('edit_increment')
def implement_increment_route(increment_id):
    implement_increment(increment_id)
    log_activity(session.get('username'), 'Implement Increment', f'Implemented increment ID: {increment_id}')
    flash('✅ Increment implemented and salary updated!', 'success')
    
    return redirect(url_for('increment_sheet'))


# ============= ACTIVITY LOGS ROUTES =============
@app.route('/activity-logs')
@login_required
@permission_required('view_logs')
def activity_logs():
    logs = get_all_logs(500)
    stats = get_logs_stats()
    return render_template('activity_logs.html', logs=logs, stats=stats)

@app.route('/activity-logs/clear', methods=['POST'])
@login_required
@permission_required('view_logs')
def clear_activity_logs():
    days = int(request.form.get('days', 30))
    deleted = clear_old_logs(days)
    log_activity(session.get('username'), 'Clear Logs', f'Cleared {deleted} old activity logs')
    flash(f'✅ {deleted} old activity logs deleted!', 'success')
    return redirect(url_for('activity_logs'))


# ============= USER MANAGEMENT ROUTES =============
@app.route('/users')
@login_required
@permission_required('view_users')
def users():
    users = get_all_users()
    from modules.employees import get_all_employees
    employees = get_all_employees()
    existing_ids = [e[0] for e in employees]
    next_id = 1
    while next_id in existing_ids:
        next_id += 1
    return render_template('users.html', users=users, next_employee_id=next_id)

@app.route('/add-user', methods=['POST'])
@login_required
@permission_required('edit_users')
def add_user_route():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    full_name = request.form.get('full_name', '')
    email = request.form.get('email', '')
    employee_id = int(request.form.get('employee_id', 0)) if request.form.get('employee_id') else 0
    role = request.form.get('role', 'employee')
    department = request.form.get('department', '')
    
    if add_user(username, password, full_name, email, employee_id, role, department):
        log_activity(session.get('username'), 'Add User', f'Added user: {username}')
        flash(f'✅ User {username} added successfully!', 'success')
    else:
        flash('❌ Username already exists!', 'danger')
    return redirect(url_for('users'))

@app.route('/edit-user/<int:user_id>', methods=['POST'])
@login_required
@permission_required('edit_users')
def edit_user_route(user_id):
    full_name = request.form.get('full_name', '')
    email = request.form.get('email', '')
    role = request.form.get('role', 'employee')
    department = request.form.get('department', '')
    is_active = int(request.form.get('is_active', 1))
    
    update_user(user_id, full_name, email, role, department, is_active)
    log_activity(session.get('username'), 'Edit User', f'Edited user ID: {user_id}')
    flash('✅ User updated successfully!', 'success')
    return redirect(url_for('users'))

@app.route('/delete-user/<int:user_id>')
@login_required
@permission_required('delete_users')
def delete_user_route(user_id):
    delete_user(user_id)
    log_activity(session.get('username'), 'Delete User', f'Deleted user ID: {user_id}')
    flash('❌ User deleted!', 'info')
    return redirect(url_for('users'))

@app.route('/change-user-password/<int:user_id>', methods=['POST'])
@login_required
@permission_required('edit_users')
def change_user_password_route(user_id):
    new_password = request.form.get('new_password', '')
    change_user_password(user_id, new_password)
    log_activity(session.get('username'), 'Change User Password', f'Changed password for user ID: {user_id}')
    flash('✅ Password changed successfully!', 'success')
    return redirect(url_for('users'))


# ============= DASHBOARD ROUTE =============
@app.route('/dashboard')
@login_required
def dashboard():
    user_role = session.get('user_role', 'employee')
    employee_id = session.get('employee_id', 0)
    
    if user_role == 'super_admin':
        return redirect(url_for('superadmin_dashboard'))
    
    if user_role == 'employee' and employee_id > 0:
        from modules.employees import get_employee_by_id
        from modules.inventory import get_all_assets
        from modules.payroll import get_all_payroll
        from modules.requests import get_requests_by_employee
        
        employee = get_employee_by_id(employee_id)
        emp_dict = {
            'id': employee[0] if employee else 0,
            'name': employee[1] if employee else 'Unknown',
            'email': employee[2] if employee else '',
            'phone': employee[3] if employee else '',
            'department': employee[5] if employee else '',
            'position': employee[4] if employee else '',
            'joining_date': employee[6] if employee else ''
        }
        
        all_assets = get_all_assets()
        employee_assets = [a for a in all_assets if len(a) > 5 and a[5] == employee_id]
        
        all_payroll = get_all_payroll()
        employee_payroll = [p for p in all_payroll if p[1] == employee_id]
        
        employee_requests = get_requests_by_employee(employee_id)
        
        stats = {'present_days': 22, 'absent_days': 2, 'late_days': 1, 'leave_balance': 12}
        
        return render_template('employee_dashboard.html',
                              employee=emp_dict,
                              assets=employee_assets,
                              payrolls=employee_payroll,
                              requests=employee_requests,
                              stats=stats)
    
    else:
        candidates = get_all_candidates()
        employees = get_all_employees()
        stats = get_asset_stats()
        payroll_stats = get_payroll_stats()
        requests_stats = get_requests_stats()
        
        current_date = datetime.now().strftime('%A, %B %d, %Y')
        
        if user_role == 'management':
            return render_template('dashboard.html',
                                  management_dashboard=True,
                                  management_restricted=True,
                                  current_date=current_date)

        if user_role == 'accountant':
            return render_template('dashboard.html',
                                  accountant_dashboard=True,
                                  payroll_total=payroll_stats['total_amount'],
                                  payroll_total_count=payroll_stats['total_count'],
                                  payroll_paid=payroll_stats['paid_count'],
                                  payroll_pending=payroll_stats['pending_count'],
                                  payroll_paid_amount=payroll_stats['paid_amount'],
                                  payroll_pending_amount=payroll_stats['pending_amount'],
                                  current_date=current_date)

        dept_counts = {}
        for e in employees:
            dept = e[5] if len(e) > 5 and e[5] else 'Not specified'
            dept_counts[dept] = dept_counts.get(dept, 0) + 1

        today_attendance = get_today_attendance()
        attendance_today = len(today_attendance)
        attendance_total = len(employees)
        
        return render_template('dashboard.html',
                              ats_total=len(candidates),
                              ats_shortlisted=count_by_status('shortlisted'),
                              ats_rejected=count_by_status('rejected'),
                              emp_total=len(employees),
                              emp_probation=len([e for e in employees if len(e) > 11 and e[11] == 'Probation']),
                              emp_permanent=len([e for e in employees if len(e) > 11 and e[11] == 'Permanent']),
                              emp_intern=len([e for e in employees if len(e) > 11 and e[11] == 'Intern']),
                              attendance_today=attendance_today,
                              attendance_total=attendance_total,
                              departments=[{'name': k, 'count': v} for k, v in sorted(dept_counts.items(), key=lambda x: x[1], reverse=True)],
                              inv_total=stats['total'],
                              inv_available=stats['available'],
                              inv_assigned=stats['assigned'],
                              payroll_total=payroll_stats['total_amount'],
                              payroll_paid=payroll_stats['paid_count'],
                              payroll_pending=payroll_stats['pending_count'],
                              pending_requests=requests_stats['pending'],
                              total_requests=requests_stats['total'],
                              recent_candidates=candidates[:5] if candidates else [],
                              current_date=current_date)


# ============= DOWNLOAD ROUTE =============
@app.route('/download/<filename>')
@login_required
def download_cv(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=filename)
    flash('File not found', 'error')
    return redirect(url_for('ats_dashboard'))


# ============= CLEAR DATA ROUTE =============
@app.route('/clear-all-data', methods=['POST'])
@login_required
@role_required(['admin'])
def clear_all_data():
    from modules.database import get_db_connection
    delete_all_uploads()
    conn = get_db_connection('candidates.db')
    conn.execute('DELETE FROM candidates')
    conn.commit()
    conn.close()
    return {'success': True, 'message': 'ATS data cleared!'}


# ============= UPDATE EMPLOYEE SALARY FUNCTION =============
def update_employee_salary(employee_id, new_salary):
    """Update employee salary in employees.db"""
    from modules.database import get_db_connection
    conn = get_db_connection('employees.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE employees SET salary = ? WHERE id = ?", (new_salary, employee_id))
    conn.commit()
    conn.close()


# ============= RUN APP =============
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)