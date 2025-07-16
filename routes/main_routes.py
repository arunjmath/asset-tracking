from flask import Blueprint, render_template, request, session, redirect, url_for
from services.employee_service import get_employees
from utils.helpers import format_date, build_filter
import math

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    if not session.get('username'):
        return redirect(url_for('auth.login'))

    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = 5
    filter_query = build_filter(query)
    employees, total = get_employees(filter_query, page, per_page)
    for emp in employees:
        emp['join_date'] = format_date(emp.get('join_date'))
        emp['last_date'] = format_date(emp.get('last_date'))
    total_pages = math.ceil(total / per_page)
    return render_template('index.html', employees=employees, view="All Employees", page=page, total_pages=total_pages, query=query, role=session.get('role'))

@main_bp.route('/about')
def about():
    return render_template('about.html')
