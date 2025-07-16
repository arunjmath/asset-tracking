from datetime import datetime

def format_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%d/%m/%y")
    except:
        return date_str

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def build_filter(query, filter_by=None):
    filter_query = {}
    if filter_by == 'active':
        filter_query['is_active'] = True
    elif filter_by == 'inactive':
        filter_query['is_active'] = False
    if query:
        filter_query["$or"] = [
            {"name": {"$regex": query, "$options": "i"}},
            {"employee_id": {"$regex": query, "$options": "i"}}
        ]
    return filter_query
