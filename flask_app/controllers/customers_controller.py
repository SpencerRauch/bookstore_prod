from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.employee_model import Employee
from flask_app.models.authorization_model import Authorization
from flask_app.models.stockitem_model import StockItem
from flask_app.models.address_model import Address
from flask_app.models.customer_model import Customer
from flask_app.controllers import enforce_login, enforce_admin, enforce_sales_access


@app.route('/customers')
@enforce_sales_access
def customers_dash():
    all_customers = Customer.get_all_with_address()
    return render_template("customers_dash.html", all_customers=all_customers)

@app.route('/customers/new')
@enforce_sales_access
def new_customer():
    return render_template("customer_new.html",state_codes = Address.state_codes)

@app.route('/customers/create', methods=['POST'])
@enforce_sales_access
def create_customer():
    valid = True
    if not Address.valid_address(request.form):
        valid = False
    if not Customer.valid_customer(request.form):
        valid = False
    if not valid:
        session['name'] = request.form['name']
        session['city'] = request.form['city']
        session['street'] = request.form['street']
        session['state'] = request.form['state']
        session['zip'] = request.form['zip']
        return redirect('/customers/new')
    address_id = Address.create(request.form)
    data = {
        **request.form,
        'address_id': address_id
    }
    Customer.create(data)
    session.pop('name',None)
    session.pop('city',None)
    session.pop('street',None)
    session.pop('state',None)
    session.pop('zip',None)
    return redirect('/customers')

@app.route('/customers/clear_form')
@enforce_sales_access
def clear_cust_form():
    session.pop('name',None)
    session.pop('city',None)
    session.pop('street',None)
    session.pop('state',None)
    session.pop('zip',None)
    return redirect('/customers/new')

@app.route('/customers/<int:id>/edit')
@enforce_sales_access
def edit_customer(id):
    to_edit = Customer.get_by_id({"id":id})
    state_codes = Address.state_codes
    return render_template("customer_edit.html",to_edit=to_edit,state_codes=state_codes)

@app.route('/customers/<int:id>/update', methods=['POST'])
@enforce_sales_access
def update_customer(id):
    valid = True
    if not Address.valid_address(request.form):
        valid = False
    if not Customer.valid_customer(request.form):
        valid = False
    if not valid:
        return redirect(f'/customers/{id}/edit')
    Address.update(request.form)
    data = {
        'name':request.form['name'],
        'id': id
    }
    Customer.update(data)
    
    return redirect('/customers')   