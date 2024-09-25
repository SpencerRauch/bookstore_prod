from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.employee_model import Employee
from flask_app.models.authorization_model import Authorization
from flask_app.models.stockitem_model import StockItem
from flask_app.models.address_model import Address
from flask_app.models.manufacturer_model import Manufacturer
from flask_app.controllers import enforce_login, enforce_admin, enforce_inventory_access, enforce_sales_access


@app.route('/manufacturers')
@enforce_inventory_access
def manufacturers_dash():
    all_manufacturers = Manufacturer.get_all()
    return render_template("manufacturers_dash.html", all_manufacturers=all_manufacturers)

@app.route('/manufacturers/new')
@enforce_inventory_access
def new_manufacturer():
    return render_template("manufacturer_new.html",state_codes = Address.state_codes)

@app.route('/manufacturers/create', methods=['POST'])
@enforce_inventory_access
def create_manufacturer():
    valid = True
    if not Address.valid_address(request.form):
        valid = False
    if not Manufacturer.valid_manufacturer(request.form):
        valid = False
    if not valid:
        session['name'] = request.form['name']
        session['city'] = request.form['city']
        session['street'] = request.form['street']
        session['state'] = request.form['state']
        session['zip'] = request.form['zip']
        return redirect('/manufacturers/new')
    address_id = Address.create(request.form)
    data = {
        **request.form,
        'address_id': address_id
    }
    Manufacturer.create(data)
    session.pop('name',None)
    session.pop('city',None)
    session.pop('street',None)
    session.pop('state',None)
    session.pop('zip',None)
    return redirect('/manufacturers')

@app.route('/manufacturers/clear_form')
@enforce_inventory_access
def clear_manu_form():
    session.pop('name',None)
    session.pop('city',None)
    session.pop('street',None)
    session.pop('state',None)
    session.pop('zip',None)
    return redirect('/manufacturers/new')

@app.route('/manufacturers/<int:id>/edit')
@enforce_inventory_access
def edit_manufacturer(id):
    to_edit = Manufacturer.get_by_id({"id":id})
    state_codes = Address.state_codes
    return render_template("manufacturer_edit.html",to_edit=to_edit,state_codes=state_codes)

@app.route('/manufacturers/<int:id>/update', methods=['POST'])
@enforce_inventory_access
def update_manufacturer(id):
    valid = True
    if not Address.valid_address(request.form):
        valid = False
    if not Manufacturer.valid_manufacturer(request.form):
        valid = False
    if not valid:
        return redirect(f'/manufacturers/{id}/edit')
    Address.update(request.form)
    data = {
        'name':request.form['name'],
        'id': id
    }
    Manufacturer.update(data)
    
    return redirect('/manufacturers')   