from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.employee_model import Employee
from flask_app.models.authorization_model import Authorization
from flask_app.models.adjustment_model import Adjustment
from flask_app.models.stockitem_model import StockItem
from flask_app.models.manufacturer_model import Manufacturer
from flask_app.controllers import enforce_login, enforce_admin, enforce_inventory_access, enforce_sales_access


#! Employee Dashboard Route
@app.route('/dashboard')
@enforce_login
def dashboard():
    employee = Employee.get_by_id({'id':session['employee_id']})
    all_items = StockItem.get_all_with_manufacturer()
    return render_template('dashboard.html', employee=employee, all_items=all_items)

@app.route('/inventory/new')
@enforce_inventory_access
def new_stock():
    all_manufacturers = Manufacturer.get_all()
    return render_template("inventory_new.html", all_manufacturers = all_manufacturers)

@app.route('/inventory/create', methods=['post'])
@enforce_inventory_access
def create_stock():
    if not StockItem.valid_stock_item(request.form):
        return redirect('/inventory/new')
    StockItem.create(request.form)
    return redirect("/dashboard")

@app.route('/inventory/<int:id>/adjust_form')
@enforce_inventory_access
def adjust_stock_form(id):
    to_adjust = StockItem.get_by_id({'id':id})
    reasons = Adjustment.reasons
    return render_template("inventory_adjustment.html", to_adjust = to_adjust, reasons=reasons)

@app.route('/inventory/<int:id>/adjust', methods=['post'])
@enforce_inventory_access
def adjust_stock(id):
    if not Adjustment.valid_adjustment(request.form):
        return redirect(f"/inventory/{id}/adjust_form")
    #perform adjustment
    stock_data = {
        **request.form,
        'id':id
    }
    StockItem.direct_adjust(stock_data)
    #create adjustment record
    record_data = {
        **request.form,
        'employee_id':session['employee_id'],
        'stock_item_id':id
    }
    Adjustment.create(record_data)
    return redirect('/dashboard')