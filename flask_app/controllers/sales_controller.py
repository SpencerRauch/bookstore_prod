from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.employee_model import Employee
from flask_app.models.authorization_model import Authorization
from flask_app.models.stockitem_model import StockItem
from flask_app.models.address_model import Address
from flask_app.models.manufacturer_model import Manufacturer
from flask_app.models.customer_model import Customer
from flask_app.models.sale_order_model import SalesOrder
from flask_app.models.sale_line_item_model import SaleLineItem
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
    
@app.route('/sales/new')
@enforce_sales_access
def sales_new():
    all_customers = Customer.get_all()
    return render_template("sales_new.html", all_customers=all_customers)

@app.route('/sales/create', methods=['POST'])
@enforce_sales_access
def sales_order_create():
    if not SalesOrder.valid_sale_order(request.form):
        return redirect("/sales/new")
    data = {
        **request.form,
        'employee_id':session['employee_id']
    }
    id = SalesOrder.create(data)
    return redirect(f"/sales/{id}/edit")

@app.route('/sales/<int:id>/edit')
@enforce_sales_access
def sales_order_edit(id):
    to_edit = SalesOrder.get_by_id({'id':id})
    all_items = StockItem.get_all_with_manufacturer()
    return render_template("sales_edit.html", to_edit=to_edit, all_items=all_items)

@app.route('/sales/<int:id>/add_item', methods = ['POST'])
@enforce_sales_access
def sales_order_add(id):
    line_item_data = {
        'ordered_quantity':request.form['quantity'],
        'sales_order_id':id,
        'stock_item_id': request.form['stock_item_id']
    }
    if not SaleLineItem.valid_sale_line_item(line_item_data):
        return redirect(f"/sales/{id}/edit")
    SaleLineItem.create(line_item_data)
    return redirect(f"/sales/{id}/edit")
    
@app.route('/sales/<int:order_id>/adjust_order_line/<int:line_id>', methods=['POST'])
@enforce_sales_access
def adjust_ordered(order_id,line_id):
    data = {
        **request.form,
        'id':line_id
    }
    try:
        val = int(request.form['ordered_quantity'])
        if val <= 0:
            flash("quantity must be positive. Use remove button to delete from order","qty"+str(line_id))
            return redirect(f"/sales/{order_id}/edit")
    except ValueError:
            flash("quantity must be numerical. Use remove button to delete from order", "qty"+str(line_id))
            return redirect(f"/sales/{order_id}/edit")

    SaleLineItem.update_ordered(data)
    return redirect(f"/sales/{order_id}/edit")

@app.route('/sales/<int:order_id>/remove_order_line/<int:line_id>', methods=['POST'])
@enforce_sales_access
def remove_order_line(order_id,line_id):
    SaleLineItem.delete({"id":line_id})
    return redirect(f"/sales/{order_id}/edit")