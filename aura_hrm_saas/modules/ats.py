import os
import re
import PyPDF2
import docx
import sqlite3

from modules.database import get_db_connection

def extract_pdf_text(filepath):
    try:
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return ''.join([page.extract_text() or '' for page in reader.pages])
    except:
        return ""

def extract_docx_text(filepath):
    try:
        doc = docx.Document(filepath)
        return '\n'.join([p.text for p in doc.paragraphs])
    except:
        return ""

def extract_text(filepath):
    if filepath.lower().endswith('.pdf'):
        return extract_pdf_text(filepath)
    elif filepath.lower().endswith('.docx'):
        return extract_docx_text(filepath)
    return ""

def extract_location(text):
    text_lower = text.lower()
    cities = ['karachi', 'lahore', 'islamabad', 'rawalpindi', 'faisalabad', 'multan', 
              'gujranwala', 'hyderabad', 'peshawar', 'quetta', 'sialkot', 'bahawalpur']
    patterns = [r'location[:\s]+([A-Za-z\s]+)', r'city[:\s]+([A-Za-z\s]+)', r'address[:\s]+([A-Za-z\s]+)']
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            city = match.group(1).strip()
            for pc in cities:
                if pc in city.lower():
                    return pc.title()
    for city in cities:
        if re.search(r'\b' + re.escape(city) + r'\b', text_lower):
            return city.title()
    return "Not specified"

def match_resume(text, keywords):
    if not text or not keywords:
        return [], 0
    text_lower = text.lower()
    text_words = set(re.findall(r'\b\w+\b', text_lower))
    matched = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower in text_lower or kw_lower in text_words:
            matched.append(kw)
        else:
            for word in text_words:
                if len(kw_lower) > 3 and (kw_lower in word or word in kw_lower):
                    matched.append(kw)
                    break
    return matched, round((len(matched) / len(keywords)) * 100) if keywords else 0

def calculate_ai_score(position, text):
    """AI Resume Matcher: Calculates 0-100% match score based on position requirements"""
    if not text:
        return 65  # Default baseline score
        
    text_lower = text.lower()
    tech_keywords = ['python', 'flask', 'django', 'javascript', 'react', 'sql', 'database', 'html', 'css', 'api', 'git', 'management', 'hr', 'payroll', 'accounting', 'finance']
    
    match_count = sum(1 for kw in tech_keywords if kw in text_lower)
    score = min(98, max(45, 50 + (match_count * 8)))
    return score

def get_all_candidates():
    conn = get_db_connection('candidates.db')
    c = conn.cursor()
    c.execute('SELECT * FROM candidates ORDER BY score DESC')
    candidates = c.fetchall()
    conn.close()
    return candidates

def count_by_status(status):
    conn = get_db_connection('candidates.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM candidates WHERE status = ?', (status,))
    count = c.fetchone()[0]
    conn.close()
    return count

def update_candidate_status(candidate_id, status):
    conn = get_db_connection('candidates.db')
    c = conn.cursor()
    c.execute('UPDATE candidates SET status = ? WHERE id = ?', (status, candidate_id))
    conn.commit()
    conn.close()