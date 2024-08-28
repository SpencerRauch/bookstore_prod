from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.employee_model import Employee
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employees/register', methods=['post'])
def register_employee():
    if not Employee.valid_register(request.form):
        return redirect('/')
    
    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hashed_pass,
        'confirm_pass': hashed_pass
    }
    employee_id = Employee.create(data) #UUID
    session['employee_id'] = employee_id
    return redirect('/dashboard')

@app.route('/employees/login',methods=['post'])
def login_employee():
    potential_employee = Employee.get_by_email(request.form)
    if not potential_employee:
        flash('Invalid Credentials', 'log')
        return redirect('/')
    
    if not bcrypt.check_password_hash(potential_employee.password,request.form['password']):
        flash('Invalid Credentials', 'log')
        return redirect('/')
    session['employee_id'] = potential_employee.id
    return redirect('/dashboard')

@app.route('/employees/logout')
def logout():
    del session['employee_id']
    # session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'employee_id' not in session:
        return redirect('/')