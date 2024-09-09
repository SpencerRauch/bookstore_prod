from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.employee_model import Employee
from flask_app.models.authorization_model import Authorization
from flask_app.models.stockitem_model import StockItem
from flask_app.controllers import enforce_login, enforce_admin, enforce_inventory_access, enforce_sales_access


#! Employee Dashboard Route
@app.route('/dashboard')
@enforce_login
def dashboard():
    employee = Employee.get_by_id({'id':session['employee_id']})
    all_items = StockItem.get_all_with_manufacturer()
    return render_template('dashboard.html', employee=employee, all_items=all_items)

