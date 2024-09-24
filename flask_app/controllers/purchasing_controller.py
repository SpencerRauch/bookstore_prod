from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.employee_model import Employee
from flask_app.models.stockitem_model import StockItem
from flask_app.models.address_model import Address
from flask_app.models.purchase_order_model import PurchaseOrder
from flask_app.models.purchase_line_item_model import PurchaseLineItem
from flask_app.models.manufacturer_model import Manufacturer
from flask_app.controllers import enforce_inventory_access

@app.route('/purchasing')
@enforce_inventory_access 
def purchasing_dash():
    context = {
        'all_orders' : PurchaseOrder.get_all_with_manufacturer(),
        'statuses' : PurchaseOrder.statuses,
        'employee' : Employee.get_by_id({'id':session['employee_id']})
    }
    return render_template("purchasing_dash.html", **context)
    
@app.route('/purchasing/new')
@enforce_inventory_access
def purchasing_new():
    all_manufacturers = Manufacturer.get_all()
    return render_template("purchasing_new.html", all_manufacturers=all_manufacturers)

@app.route('/purchasing/create', methods=['POST'])
@enforce_inventory_access
def purchasing_order_create():
    if not PurchaseOrder.valid_sale_order(request.form):
        return redirect("/purchasing/new")
    data = {
        **request.form,
        'employee_id':session['employee_id']
    }
    id = PurchaseOrder.create(data)
    return redirect(f"/purchasing/{id}/edit")

@app.route('/purchasing/<int:id>/edit')
@enforce_inventory_access
def purchasing_order_edit(id):
    to_edit = PurchaseOrder.get_by_id({'id':id})
    if to_edit.status != 0:
        flash("Order cannot be edited, only orders with a status of entering may be edited","edit_err")
        return redirect('/purchasing')
    all_items = StockItem.get_all_with_manufacturer()
    return render_template("purchasing_edit.html", to_edit=to_edit, all_items=all_items)

@app.route('/purchasing/<int:id>/add_item', methods = ['POST'])
@enforce_inventory_access
def purchasing_order_add(id):
    line_item_data = {
        'ordered_quantity':request.form['quantity'],
        'purchase_order_id':id,
        'stock_item_id': request.form['stock_item_id']
    }
    if not PurchaseLineItem.valid_sale_line_item(line_item_data):
        return redirect(f"/purchasing/{id}/edit")
    PurchaseLineItem.create(line_item_data)
    return redirect(f"/purchasing/{id}/edit")
    
@app.route('/purchasing/<int:order_id>/adjust_order_line/<int:line_id>', methods=['POST'])
@enforce_inventory_access
def po_adjust_ordered(order_id,line_id):
    data = {
        **request.form,
        'id':line_id
    }
    try:
        val = int(request.form['ordered_quantity'])
        if val <= 0:
            flash("quantity must be positive. Use remove button to delete from order","qty"+str(line_id))
            return redirect(f"/purchasing/{order_id}/edit")
    except ValueError:
            flash("quantity must be numerical. Use remove button to delete from order", "qty"+str(line_id))
            return redirect(f"/purchasing/{order_id}/edit")

    PurchaseLineItem.update_ordered(data)
    return redirect(f"/purchasing/{order_id}/edit")

@app.route('/purchasing/<int:order_id>/remove_order_line/<int:line_id>', methods=['POST'])
@enforce_inventory_access
def po_remove_order_line(order_id,line_id):
    PurchaseLineItem.delete({"id":line_id})
    return redirect(f"/purchasing/{order_id}/edit")

@app.route('/purchasing/<int:id>/finalize')
@enforce_inventory_access
def finalize_purchasing_order(id):
    PurchaseOrder.update_status({'id':id,'status':1})
    return redirect('/purchasing')

@app.route('/purchasing/<int:id>/cancel')
@enforce_inventory_access
def cancel_purchasing_order(id):
    PurchaseOrder.update_status({'id':id,'status':3})
    return redirect('/purchasing')

@app.route('/purchasing/<int:id>/view')
@enforce_inventory_access
def view_only_purchasing(id):
    one_order = PurchaseOrder.get_by_id({"id":id})
    statuses = PurchaseOrder.statuses
    return render_template("purchasing_view.html",one_order=one_order, statuses=statuses)

@app.route('/purchasing/<int:id>/receive')
@enforce_inventory_access
def receiving_reconciliation(id):
    one_order = PurchaseOrder.get_by_id({"id":id})
    statuses = PurchaseOrder.statuses
    return render_template("purchasing_receive.html",one_order=one_order, statuses=statuses)

@app.route('/purchasing/<int:id>/receive_final')
@enforce_inventory_access
def finalize_receiving(id):
    lines = PurchaseLineItem.get_all_for_order({'id':id})
    # if not StockItem.ship_lines(lines): #TODO: Write receive lines method
    #     return redirect(f"/purchasing/{id}/ship")
    PurchaseOrder.update_status({'id':id,'status':2})
    return redirect('/purchasing')

@app.route('/purchasing/<int:id>/receive_full')
@enforce_inventory_access
def set_full_receive(id):
    lines = PurchaseLineItem.get_all_for_order({'id':id})
    PurchaseLineItem.receive_full(lines)
    return redirect(f"/purchasing/{id}/receive")


@app.route('/purchasing/<int:order_id>/receive_order_line/<int:line_id>', methods=['POST'])
@enforce_inventory_access
def receive_ordered(order_id,line_id):
    data = {
        **request.form,
        'id':line_id
    }
    try:
        val = int(request.form['received_quantity'])
        if val < 0:
            flash("quantity must be positive.","qty"+str(line_id))
            return redirect(f"/purchasing/{order_id}/ship")
    except ValueError:
            flash("quantity must be numerical", "qty"+str(line_id))
            return redirect(f"/purchasing/{order_id}/ship")

    PurchaseLineItem.update_received(data)
    return redirect(f"/purchasing/{order_id}/ship")