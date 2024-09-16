from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.employee_model import Employee
from flask_app.models.authorization_model import Authorization
from flask_app.models.stockitem_model import StockItem
from flask_app.models.address_model import Address
from flask_app.models.manufacturer_model import Manufacturer
from flask_app.models.customer_model import Customer
from flask_app.models.sale_order_model import SalesOrder
from flask_app.controllers import enforce_login, enforce_admin, enforce_inventory_access, enforce_sales_access, enforce_sales_or_inventory

@app.route('/sales')
@enforce_sales_or_inventory
def sales_dash():
    context = {
        'all_orders' : SalesOrder.get_all_with_customer(),
        'statuses' : SalesOrder.statuses,
        'employee' : Employee.get_by_id({'id':session['employee_id']})
    }
    return render_template("sales_dash.html", **context)
    
