from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import validate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = validate_user(request.form['username'], request.form['password'])
        if user:
            session['username'] = request.form['username']
            session['role'] = user['role']
            return redirect(url_for('employee.home'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route('/about')
def about():
    return render_template('about.html')
