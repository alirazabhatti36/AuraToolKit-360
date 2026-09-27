import os
from datetime import datetime

UPLOAD_FOLDER = 'uploads'

def delete_old_files():
    try:
        now = datetime.now().timestamp()
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                if now - os.path.getmtime(filepath) > 7 * 24 * 3600:
                    os.remove(filepath)
    except:
        pass

def delete_all_uploads():
    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
    except:
        pass

def get_db_size():
    try:
        size = os.path.getsize('databases/candidates.db') / (1024 * 1024)
        return round(size, 2)
    except:
        return 0

def get_uploads_size():
    try:
        total = 0
        for file in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, file)
            if os.path.isfile(filepath):
                total += os.path.getsize(filepath)
        return round(total / (1024 * 1024), 2)
    except:
        return 0