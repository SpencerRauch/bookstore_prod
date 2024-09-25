from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.employee_model import Employee
from flask_app.models.authorization_model import Authorization
from flask_app.controllers import enforce_login, enforce_admin
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#! Home Page
@app.route('/')
def index():
    return render_template('index.html')

#! Register Logic
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
    session['employee_name'] = request.form['first_name'] + " " + request.form['last_name']
    return redirect('/dashboard')

#! Login Logic
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
    session['employee_name'] = potential_employee.first_name + " " + potential_employee.last_name
    return redirect('/dashboard')

#! Logout Logic
@app.route('/employees/logout')
def logout():
    if "employee_id" in session:
        del session['employee_id']
    if "employee_name" in session:
        del session['employee_name']
    # session.clear()
    return redirect('/')

#! Credentials error page
@app.route("/employees/credentials_error")
@enforce_login
def credentials_error():
    return render_template("credentials_error.html")


# #! Admin credentials test page
# @app.route("/employees/admin/test")
# @enforce_admin
# def admin_test():
#     return "You are an admin"
