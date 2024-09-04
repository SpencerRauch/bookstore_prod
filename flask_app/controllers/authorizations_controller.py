from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.employee_model import Employee
from flask_app.models.authorization_model import Authorization
from flask_app.controllers import enforce_login, enforce_admin


#! Auth page
@app.route("/auth")
@enforce_login
def auth_page():
    employee = Employee.get_by_id({'id':session['employee_id']})
    return render_template('auth.html', employee=employee)

#! New authorization request processing
@app.route('/auth/<int:requesting_id>/<int:requested_level>')
@enforce_login
def new_auth_request(requesting_id, requested_level):
    if session['employee_id'] != requesting_id:
        flash("Id error -- contact admin")
        return redirect("/auth")
    if requested_level < 0 or requested_level > 2:
        flash("Access level error - contact admin")
        return redirect("/auth")
    employee = Employee.get_by_id({'id':requesting_id})
    if not employee:
        flash("Session error - contact admin")
        return redirect("/auth")
    new_request = False
    match requested_level:
        case 0:
            if employee.sales_access == 0:
                new_request = True
                Employee.new_auth_request(0,requesting_id)
            if employee.sales_access == 3:
                flash("Request previously denied")
                return redirect("/auth")
        case 1:
            if employee.inventory_access == 0:
                new_request = True
                Employee.new_auth_request(1,requesting_id)
            if employee.inventory_access == 3:
                flash("Request previously denied")
                return redirect("/auth")
        case 2:
            if employee.admin == 0:
                new_request = True
                Employee.new_auth_request(2,requesting_id)
            if employee.admin == 3:
                flash("Request previously denied")
                return redirect("/auth")
    if new_request:
        Authorization.create({'requesting_id':requesting_id, 'requested_level':requested_level})
    
    return redirect("/auth")

@app.route("/auth/admin")
@enforce_admin
def auth_admin():
    all_requests = Authorization.get_all_with_requester()
    return render_template("auth_admin.html", all_requests = all_requests)

