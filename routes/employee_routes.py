from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from services.employee_service import insert_employee, update_employee, get_employee, get_all_employees
from utils.helpers import allowed_file
import os
from werkzeug.utils import secure_filename

emp_bp = Blueprint('employee', __name__)

@emp_bp.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    query = request.args.get('q', '').lower()
    page = int(request.args.get('page', 1))
    per_page = 5

    all_employees = get_all_employees()
    if query:
        all_employees = [e for e in all_employees if query in (e.get('name') or '').lower() or query in (e.get('employee_id') or '').lower()]

    total_pages = (len(all_employees) + per_page - 1) // per_page
    employees = all_employees[(page - 1) * per_page: page * per_page]

    return render_template('index.html', employees=employees, page=page, total_pages=total_pages, query=query, view="All Employees")

@emp_bp.route('/active')
def active():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    query = request.args.get('q', '').lower()
    page = int(request.args.get('page', 1))
    per_page = 5

    all_employees = [e for e in get_all_employees() if e.get('is_active')]
    if query:
        all_employees = [e for e in all_employees if query in (e.get('name') or '').lower() or query in (e.get('employee_id') or '').lower()]

    total_pages = (len(all_employees) + per_page - 1) // per_page
    employees = all_employees[(page - 1) * per_page: page * per_page]

    return render_template('index.html', employees=employees, page=page, total_pages=total_pages, query=query, view="Active Employees")

@emp_bp.route('/inactive')
def inactive():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    query = request.args.get('q', '').lower()
    page = int(request.args.get('page', 1))
    per_page = 5

    all_employees = [e for e in get_all_employees() if not e.get('is_active')]
    if query:
        all_employees = [e for e in all_employees if query in (e.get('name') or '').lower() or query in (e.get('employee_id') or '').lower()]

    total_pages = (len(all_employees) + per_page - 1) // per_page
    employees = all_employees[(page - 1) * per_page: page * per_page]

    return render_template('index.html', employees=employees, page=page, total_pages=total_pages, query=query, view="Inactive Employees")

@emp_bp.route('/add', methods=['GET', 'POST'])
def add():
    if session.get('role') not in ['admin', 'hr']:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        last_date = request.form.get('last_date') or None
        is_active = False if last_date else request.form.get('active') == 'on'

        document_url = None
        file = request.files.get('document')
        if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            document_url = filepath

        data = {key: request.form.get(key) for key in request.form}
        data['assets'] = request.form.getlist('assets')
        data['is_active'] = is_active
        data['document_url'] = document_url

        insert_employee(data)
        return redirect(url_for('employee.home'))

    return render_template('add.html')

@emp_bp.route('/edit/<emp_id>', methods=['GET', 'POST'])
def edit(emp_id):
    if session.get('role') != 'admin':
        flash("Access Denied: Admins only", 'warning')
        return redirect(url_for('employee.home'))

    emp = get_employee(emp_id)
    if not emp:
        flash("Employee not found", "danger")
        return redirect(url_for('employee.home'))

    if request.method == 'POST':
        last_date = request.form.get('last_date') or None
        is_active = False if last_date else request.form.get('is_active') == 'on'

        document_url = emp.get('document_url')
        file = request.files.get('document')
        if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            document_url = filepath

        updated_data = {key: request.form.get(key) for key in request.form}
        updated_data['assets'] = request.form.getlist('assets')
        updated_data['is_active'] = is_active
        updated_data['document_url'] = document_url

        update_employee(emp_id, updated_data)
        return redirect(url_for('employee.home'))

    return render_template('edit.html', emp=emp)
