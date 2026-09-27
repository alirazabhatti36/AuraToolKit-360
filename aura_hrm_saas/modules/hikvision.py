import base64
import json
import os
import ssl
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urlparse, urlunparse

import pandas as pd

from modules.database import get_db_connection
from modules.employees import get_employee_by_id


def _strip_namespace(tag):
    if '}' in tag:
        return tag.split('}', 1)[1]
    return tag


def _parse_datetime(value):
    if not value:
        return None

    value = value.strip()
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%d-%m-%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.strptime(value[:19], fmt)
        except Exception:
            continue
    return None


def _normalize_host(device_ip):
    trimmed = device_ip.strip()
    parsed = urlparse(trimmed)
    if not parsed.scheme:
        trimmed = 'https://' + trimmed
        parsed = urlparse(trimmed)

    netloc = parsed.netloc or parsed.path
    return parsed.scheme, netloc.split('/', 1)[0]


def _build_hikvision_urls(device_ip, start_date, end_date):
    scheme, netloc = _normalize_host(device_ip)
    query = f'startTime={start_date}T00:00:00&endTime={end_date}T23:59:59'
    endpoints = [
        '/ISAPI/Attendance/Record',
        '/ISAPI/attendance/record',
        '/ISAPI/Attendance/Record?format=json',
        '/ISAPI/AccessControl/AcsEvent',
        '/ISAPI/AccessControl/AcsEvent?startTime={}&endTime={}'.format(start_date + 'T00:00:00', end_date + 'T23:59:59')
    ]

    urls = []
    for path in endpoints:
        urls.append(urlunparse((scheme, netloc, path.split('?')[0], '', path.split('?')[1] if '?' in path else query, '')))
    if scheme == 'https':
        urls.append(urlunparse(('http', netloc, '/ISAPI/Attendance/Record', '', query, '')))
    else:
        urls.append(urlunparse(('https', netloc, '/ISAPI/Attendance/Record', '', query, '')))
    return urls


# ============= ✅ UPDATED: SSL Verification Disabled =============
def _create_hikvision_opener(username, password):
    """
    Create opener with SSL verification disabled for self-signed certificates
    """
    # SSL context - DISABLE verification (self-signed certificate ke liye)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Password handlers
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, 'http://', username, password)
    password_mgr.add_password(None, 'https://', username, password)
    
    # Create handlers
    https_handler = urllib.request.HTTPSHandler(context=ssl_context)
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    digest_handler = urllib.request.HTTPDigestAuthHandler(password_mgr)
    
    # Return opener with all handlers
    return urllib.request.build_opener(https_handler, auth_handler, digest_handler)


# ============= ✅ UPDATED: fetch_hikvision_attendance =============
def fetch_hikvision_attendance(device_ip, username, password, start_date, end_date):
    """Fetch attendance records from a Hikvision device using ISAPI."""
    if not device_ip:
        raise ValueError('Device IP is required')

    opener = _create_hikvision_opener(username, password)  # SSL context now inside
    last_error = None
    debug_log = []

    for url in _build_hikvision_urls(device_ip, start_date, end_date):
        request = urllib.request.Request(url)
        request.add_header('Accept', 'application/xml, application/json, text/xml, */*')
        request.add_header('User-Agent', 'Mozilla/5.0 (compatible; HikvisionSync/1.0)')
        request.add_header('Connection', 'close')

        try:
            with opener.open(request, timeout=20) as response:
                payload = response.read().decode('utf-8', errors='replace')
                debug_log.append(f'✅ SUCCESS: {url}')
                return _parse_hikvision_xml(payload), debug_log
        except urllib.error.HTTPError as exc:
            debug_log.append(f'❌ {url} -> HTTP {exc.code}: {exc.reason}')
            if exc.code in (404, 401, 403, 405):
                last_error = f'HTTP {exc.code}: {exc.reason}'
                continue
            raise RuntimeError(f'Hikvision HTTP error for {url}: {exc.code} {exc.reason}')
        except urllib.error.URLError as exc:
            debug_log.append(f'❌ {url} -> URLError: {exc.reason}')
            last_error = f'Connection error: {exc.reason}'
            continue
        except Exception as exc:
            debug_log.append(f'❌ {url} -> Exception: {str(exc)}')
            last_error = str(exc)
            continue

    raise RuntimeError(f'All endpoints failed. Last error: {last_error}\n\nDebug log:\n' + '\n'.join(debug_log))


def _parse_report_datetime(value):
    if pd.isna(value):
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y-%m-%d %H:%M', '%d-%m-%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.strptime(text, fmt)
        except Exception:
            continue
    try:
        return pd.to_datetime(text, errors='coerce')
    except Exception:
        return None


def _normalize_column_name(name):
    return ''.join(ch.lower() if ch.isalnum() else '_' for ch in str(name).strip())


def _find_column(columns, candidates):
    normalized = { _normalize_column_name(col): col for col in columns }
    for candidate in candidates:
        norm = _normalize_column_name(candidate)
        if norm in normalized:
            return normalized[norm]
    return None


def import_hikvision_report(filepath, clear_existing=True):
    if not os.path.exists(filepath):
        return {'success': False, 'message': 'File not found.'}

    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == '.csv':
            df = pd.read_csv(filepath)
        elif ext in ('.xls', '.xlsx'):
            engine = 'xlrd' if ext == '.xls' else 'openpyxl'
            df = pd.read_excel(filepath, engine=engine)
        else:
            return {'success': False, 'message': 'Unsupported report format.'}
    except Exception as exc:
        return {'success': False, 'message': f'Could not read report file: {exc}'}

    if df.empty:
        return {'success': False, 'message': 'Report file is empty.'}

    employee_id_col = _find_column(df.columns, ['employee_id', 'emp_id', 'userid', 'user_id', 'cardno', 'card_no', 'user no', 'id'])
    employee_name_col = _find_column(df.columns, ['employee_name', 'name', 'username', 'full_name', 'full name', 'employee'])
    date_col = _find_column(df.columns, ['date', 'attendance_date', 'record_date', 'check_date', 'day'])
    check_in_col = _find_column(df.columns, ['check_in', 'checkin', 'in_time', 'check_in_time', 'checktime', 'time', 'datetime', 'record_time', 'timestamp'])
    check_out_col = _find_column(df.columns, ['check_out', 'checkout', 'out_time', 'check_out_time', 'checkout_time'])
    status_col = _find_column(df.columns, ['status', 'state', 'attendance_status', 'result', 'event'])
    remarks_col = _find_column(df.columns, ['remarks', 'remark', 'comment', 'description', 'note'])

    if employee_id_col is None and employee_name_col is None:
        return {'success': False, 'message': 'Report must contain employee ID or employee name.'}

    raw_records = []
    for _, row in df.iterrows():
        emp_id = None
        if employee_id_col is not None:
            emp_value = row.get(employee_id_col)
            if pd.notna(emp_value):
                try:
                    emp_id = int(float(emp_value))
                except Exception:
                    emp_id = None

        emp_name = ''
        if employee_name_col is not None:
            emp_name = str(row.get(employee_name_col)).strip()

        date_value = row.get(date_col) if date_col else None
        if pd.isna(date_value):
            date_value = None

        dt_value = None
        if check_in_col and pd.notna(row.get(check_in_col)):
            dt_value = _parse_report_datetime(row.get(check_in_col))
        elif status_col and pd.notna(row.get(status_col)):
            dt_value = _parse_report_datetime(row.get(status_col))
        elif date_col and pd.notna(date_value) and isinstance(date_value, datetime):
            dt_value = date_value

        if dt_value is None and check_out_col and pd.notna(row.get(check_out_col)):
            dt_value = _parse_report_datetime(row.get(check_out_col))

        if date_value is None and dt_value is not None:
            report_date = dt_value.date()
        else:
            report_date = dt_value.date() if isinstance(date_value, datetime) else None
            if report_date is None and date_value is not None:
                try:
                    report_date = pd.to_datetime(str(date_value), errors='coerce').date()
                except Exception:
                    report_date = None

        if report_date is None:
            continue

        check_in = ''
        if check_in_col and pd.notna(row.get(check_in_col)):
            check_in_dt = _parse_report_datetime(row.get(check_in_col))
            if check_in_dt:
                check_in = check_in_dt.strftime('%H:%M:%S')
        elif dt_value is not None:
            check_in = dt_value.strftime('%H:%M:%S')

        check_out = ''
        if check_out_col and pd.notna(row.get(check_out_col)):
            check_out_dt = _parse_report_datetime(row.get(check_out_col))
            if check_out_dt:
                check_out = check_out_dt.strftime('%H:%M:%S')

        status = ''
        if status_col and pd.notna(row.get(status_col)):
            status = str(row.get(status_col)).strip().lower()
            if status in ['present', 'p', '1']:
                status = 'present'
            elif status in ['late', 'l']:
                status = 'late'
            elif status in ['absent', 'a']:
                status = 'absent'
            elif status in ['half_day', 'half day', 'halfday']:
                status = 'half_day'
            else:
                status = status

        remarks = ''
        if remarks_col and pd.notna(row.get(remarks_col)):
            remarks = str(row.get(remarks_col)).strip()

        raw_records.append({
            'employee_id': emp_id if emp_id is not None else 0,
            'employee_name': emp_name,
            'date': report_date.isoformat(),
            'check_in': check_in,
            'check_out': check_out,
            'status': status if status else 'present',
            'remarks': remarks
        })

    if not raw_records:
        return {'success': False, 'message': 'No valid attendance rows were extracted from the report.'}

    grouped = {}
    for row in raw_records:
        key = (row['employee_id'], row['employee_name'], row['date'])
        entry = grouped.setdefault(key, {
            'employee_id': row['employee_id'],
            'employee_name': row['employee_name'],
            'date': row['date'],
            'check_in': None,
            'check_out': None,
            'status': 'present',
            'remarks': ''
        })
        if row['check_in']:
            if entry['check_in'] is None or row['check_in'] < entry['check_in']:
                entry['check_in'] = row['check_in']
        if row['check_out']:
            if entry['check_out'] is None or row['check_out'] > entry['check_out']:
                entry['check_out'] = row['check_out']
        if row['status'] in ['absent', 'late', 'half_day']:
            entry['status'] = row['status']
        if row['remarks']:
            entry['remarks'] = row['remarks']

    conn = get_db_connection('attendance.db')
    cursor = conn.cursor()
    if clear_existing:
        cursor.execute('DELETE FROM attendance')
    inserted = 0
    for row in grouped.values():
        cursor.execute('''
            INSERT INTO attendance (employee_id, employee_name, date, status, check_in, check_out, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['employee_id'], row['employee_name'], row['date'], row['status'], row['check_in'] or '', row['check_out'] or '', row['remarks']))
        inserted += 1
    conn.commit()
    conn.close()

    return {'success': True, 'message': f'Imported {inserted} attendance records from report and cleared old attendance.'}


def _parse_hikvision_xml(payload):
    try:
        root = ET.fromstring(payload)
    except ET.ParseError:
        try:
            json_body = json.loads(payload)
            return _parse_hikvision_json(json_body)
        except json.JSONDecodeError:
            return []

    records = []
    for element in root.iter():
        tag = _strip_namespace(element.tag).lower()
        if tag == 'attendancerecord':
            record = {}
            for child in element:
                name = _strip_namespace(child.tag).lower()
                text = child.text.strip() if child.text else ''
                record[name] = text
            records.append(record)
    return records


def _parse_hikvision_json(json_body):
    if isinstance(json_body, dict):
        for key in ('attendanceRecords', 'data', 'records', 'attendance_record'):
            if key in json_body:
                return _parse_hikvision_json(json_body[key])

        if 'attendanceRecord' in json_body:
            return _parse_hikvision_json(json_body['attendanceRecord'])

    if isinstance(json_body, list):
        records = []
        for item in json_body:
            if isinstance(item, dict):
                normalized = {k.lower(): str(v).strip() if v is not None else '' for k, v in item.items()}
                records.append(normalized)
        return records

    return []


def _get_employee_id_from_record(record):
    candidate_keys = ['employeeno', 'employeeid', 'userid', 'userno', 'personid', 'cardno']
    for key in candidate_keys:
        value = record.get(key)
        if value:
            try:
                return int(value.strip())
            except ValueError:
                continue
    return None


def _get_record_time(record):
    for key in ('time', 'timestamp', 'checktime', 'datetime', 'checkintime', 'checkouttime', 'attendance_time', 'attendancetime', 'eventtime'):
        if record.get(key):
            return _parse_datetime(record.get(key))

    # If record contains separate in/out values, prefer check-in
    if record.get('checkintime'):
        return _parse_datetime(record.get('checkintime'))
    if record.get('attendancerecordtime'):
        return _parse_datetime(record.get('attendancerecordtime'))
    return None


def sync_hikvision_attendance(device_ip, username, password, start_date, end_date, late_threshold='09:30:00'):
    summary = {'imported': 0, 'updated': 0, 'skipped': 0}

    records = fetch_hikvision_attendance(device_ip, username, password, start_date, end_date)
    if not records:
        return {'success': True, 'message': 'No Hikvision attendance records found for the selected range.'}

    grouped = {}
    for record in records:
        employee_id = _get_employee_id_from_record(record)
        record_datetime = _get_record_time(record)
        if employee_id is None or record_datetime is None:
            summary['skipped'] += 1
            continue

        date_key = record_datetime.date().isoformat()
        group_key = (employee_id, date_key)

        meta = grouped.setdefault(group_key, {
            'times': [],
            'raw': record
        })
        meta['times'].append(record_datetime)

    conn = get_db_connection('attendance.db')
    cursor = conn.cursor()

    for (employee_id, attendance_date), meta in grouped.items():
        check_in_dt = min(meta['times'])
        check_out_dt = max(meta['times'])
        check_in = check_in_dt.strftime('%H:%M:%S')
        check_out = check_out_dt.strftime('%H:%M:%S') if len(meta['times']) > 1 else ''
        status = 'present' if check_in <= late_threshold else 'late'

        raw_record = meta['raw']
        employee = get_employee_by_id(employee_id)
        employee_name = employee[1] if employee else raw_record.get('employeename') or raw_record.get('name') or f'Employee {employee_id}'
        remarks = 'Synced from Hikvision'

        cursor.execute('SELECT id FROM attendance WHERE employee_id = ? AND date = ?', (employee_id, attendance_date))
        existing = cursor.fetchone()
        if existing:
            cursor.execute('''
                UPDATE attendance
                SET employee_name = ?, status = ?, check_in = ?, check_out = ?, remarks = ?
                WHERE id = ?
            ''', (employee_name, status, check_in, check_out, remarks, existing[0]))
            summary['updated'] += 1
        else:
            cursor.execute('''
                INSERT INTO attendance (employee_id, employee_name, date, status, check_in, check_out, remarks)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (employee_id, employee_name, attendance_date, status, check_in, check_out, remarks))
            summary['imported'] += 1

    conn.commit()
    conn.close()

    return {
        'success': True,
        'message': f'Hikvision sync completed: {summary["imported"]} imported, {summary["updated"]} updated, {summary["skipped"]} skipped.'
    }