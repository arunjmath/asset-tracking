from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'supersecret'  # Used for sessions

# MongoDB Setup
MONGO_URI = "mongodb+srv://dummy:1234@cluster0.6wr4bga.mongodb.net/sprintzeal?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client.get_default_database()
collection = db["employees"]

# Admin credentials (hardcoded)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

# Protect this route
@app.route('/')
def home():
    if not session.get('admin'):
        return redirect(url_for('login'))
    query = request.args.get('q', '')
    employees = search_employees(query)
    return render_template('index.html', employees=employees, view='All Employees')

@app.route('/active')
def active():
    if not session.get('admin'):
        return redirect(url_for('login'))
    query = request.args.get('q', '')
    employees = search_employees(query, filter_by='active')
    return render_template('index.html', employees=employees, view='Active Employees')

@app.route('/inactive')
def inactive():
    if not session.get('admin'):
        return redirect(url_for('login'))
    query = request.args.get('q', '')
    employees = search_employees(query, filter_by='inactive')
    return render_template('index.html', employees=employees, view='Inactive Employees')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if not session.get('admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        last_date = request.form.get('last_date') or None
        is_active = False if last_date else (request.form.get('is_active') == 'on' or request.form.get('active') == 'on')

        data = {
            'name': request.form['name'],
            'employee_id': request.form['employee_id'],
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
    if not session.get('admin'):
        return redirect(url_for('login'))

    emp = collection.find_one({'_id': ObjectId(emp_id)})
    if request.method == 'POST':
        last_date = request.form.get('last_date') or None
        is_active = False if last_date else request.form.get('is_active') == 'on'

        updated_data = {
            'name': request.form['name'],
            'employee_id': request.form['employee_id'],
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

# Search filter
def search_employees(query, filter_by=None):
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

    return collection.find(filter_query)

if __name__ == '__main__':
    app.run(debug=True)
