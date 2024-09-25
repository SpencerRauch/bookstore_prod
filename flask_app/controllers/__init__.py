from functools import wraps
from flask import redirect, session, url_for
from flask_app.models.employee_model import Employee

def enforce_login(func): # usage: @enforce_login above a controller method
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check to make sure that employee_id is in session and redirect to index if it's not
        if "employee_id" not in session:
            return redirect(url_for("index"))
        return func(*args,**kwargs)
    return wrapper

def enforce_admin(func): # usage: @enforce_admin above a controller method
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check to make sure that employee_id is in session and redirect to index if it's not
        if "employee_id" not in session:
            return redirect(url_for("index"))
        employee = Employee.get_by_id({'id':session['employee_id']})
        if not employee:
            return redirect(url_for("logout"))
        if not employee.admin == 1:
            return redirect(url_for("credentials_error"))
        return func(*args,**kwargs)
    return wrapper

def enforce_inventory_access(func): # usage: @enforce_admin above a controller method
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check to make sure that employee_id is in session and redirect to index if it's not
        if "employee_id" not in session:
            return redirect(url_for("index"))
        employee = Employee.get_by_id({'id':session['employee_id']})
        if not employee:
            return redirect(url_for("logout"))
        if not employee.inventory_access == 1:
            return redirect(url_for("credentials_error"))
        return func(*args,**kwargs)
    return wrapper

def enforce_sales_access(func): # usage: @enforce_admin above a controller method
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check to make sure that employee_id is in session and redirect to index if it's not
        if "employee_id" not in session:
            return redirect(url_for("index"))
        employee = Employee.get_by_id({'id':session['employee_id']})
        if not employee:
            return redirect(url_for("logout"))
        if not employee.sales_access == 1:
            return redirect(url_for("credentials_error"))
        return func(*args,**kwargs)
    return wrapper

def enforce_sales_or_inventory(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # check to make sure that employee_id is in session and redirect to index if it's not
        if "employee_id" not in session:
            return redirect(url_for("index"))
        employee = Employee.get_by_id({'id':session['employee_id']})
        if not employee:
            return redirect(url_for("logout"))
        if not (employee.sales_access == 1 or employee.inventory_access == 1):
            return redirect(url_for("credentials_error"))
        return func(*args,**kwargs)
    return wrapper