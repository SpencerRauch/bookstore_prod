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