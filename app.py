from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId
import math

app = Flask(__name__)
app.secret_key = 'supersecret'

# MongoDB Setup
MONGO_URI = "mongodb+srv://dummy:1234@cluster0.6wr4bga.mongodb.net/sprintzeal?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.get_default_database()
collection = db["employees"]

# User credentials
USERS = {
    "admin": {"password": "1234", "role": "admin"},
    "hr": {"password": "hr123", "role": "hr"}
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        user = USERS.get(uname)
        if user and user["password"] == pwd:
            session['username'] = uname
            session['role'] = user['role']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Home route with pagination
@app.route('/')
def home():
    if not session.get('username'):
        return redirect(url_for('login'))

    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = 5

    filter_query = build_filter(query)
    total = collection.count_documents(filter_query)
    total_pages = math.ceil(total / per_page)

    employees = collection.find(filter_query).skip((page - 1) * per_page).limit(per_page)
    return render_template('index.html', employees=employees, view='All Employees',
                           page=page, total_pages=total_pages, query=query, role=session.get('role'))

@app.route('/active')
def active():
    if not session.get('username'):
        return redirect(url_for('login'))

    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = 5

    filter_query = build_filter(query, filter_by='active')
    total = collection.count_documents(filter_query)
    total_pages = math.ceil(total / per_page)

    employees = collection.find(filter_query).skip((page - 1) * per_page).limit(per_page)
    return render_template('index.html', employees=employees, view='Active Employees',
                           page=page, total_pages=total_pages, query=query, role=session.get('role'))

@app.route('/inactive')
def inactive():
    if not session.get('username'):
        return redirect(url_for('login'))

    query = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    per_page = 5

    filter_query = build_filter(query, filter_by='inactive')
    total = collection.count_documents(filter_query)
    total_pages = math.ceil(total / per_page)

    employees = collection.find(filter_query).skip((page - 1) * per_page).limit(per_page)
    return render_template('index.html', employees=employees, view='Inactive Employees',
                           page=page, total_pages=total_pages, query=query, role=session.get('role'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if session.get('role') not in ['admin', 'hr']:
        return redirect(url_for('login'))
    if request.method == 'POST':
        last_date = request.form.get('last_date') or None
        is_active = False if last_date else (request.form.get('is_active') == 'on')

        data = {
            'name': request.form['name'],
            'employee_id': request.form['employee_id'],
            'job_role': request.form.get('job_role'),
            'address': request.form['address'],
            'phone': request.form.get('phone'),
            'assets': request.form.getlist('assets'),
            'shift': request.form['shift'],
            'is_active': is_active,
            'join_date': request.form['join_date'],
            'last_date': last_date,
            'laptop_name': request.form.get('laptop_name'),
            'laptop_config': request.form.get('laptop_config'),
            'desktop_name': request.form.get('desktop_name'),
            'sim_number': request.form.get('sim_number'),
            'phone_device': request.form.get('phone_device'),
            'official_email': request.form.get('official_email'),
            'employee_email': request.form.get('employee_email')
        }
        collection.insert_one(data)
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route('/edit/<emp_id>', methods=['GET', 'POST'])
def edit(emp_id):
    if session.get('role') != 'admin':
        flash('Access Denied', 'warning')
        return redirect(url_for('home'))

    emp = collection.find_one({'_id': ObjectId(emp_id)})
    if request.method == 'POST':
        last_date = request.form.get('last_date') or None
        is_active = False if last_date else request.form.get('is_active') == 'on'

        updated_data = {
            'name': request.form['name'],
            'employee_id': request.form['employee_id'],
            'job_role': request.form.get('job_role'),
            'address': request.form['address'],
            'phone': request.form['phone'],
            'assets': request.form.getlist('assets'),
            'shift': request.form['shift'],
            'is_active': is_active,
            'join_date': request.form['join_date'],
            'last_date': last_date,
            'laptop_name': request.form.get('laptop_name'),
            'laptop_config': request.form.get('laptop_config'),
            'desktop_name': request.form.get('desktop_name'),
            'sim_number': request.form.get('sim_number'),
            'phone_device': request.form.get('phone_device'),
            'official_email': request.form.get('official_email'),
            'employee_email': request.form.get('employee_email')
        }
        collection.update_one({'_id': ObjectId(emp_id)}, {'$set': updated_data})
        return redirect(url_for('home'))
    return render_template('edit.html', emp=emp)

@app.route('/about')
def about():
    return render_template('about.html')

# Utility
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
