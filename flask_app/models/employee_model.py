from flask_app.config.mysqlconfig import connect_to_mysql
from flask_app import DATABASE
from flask_app.models import authorization_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

"""
ACCESS LEVELS:
             0 - no access (default)
             1 - granted
             2 - requested
             3 - denied
"""

class Employee:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.inventory_access = data['inventory_access']
        self.sales_access = data['sales_access']
        self.admin = data['admin']


    @classmethod
    def create(cls,data):
        query = """
            INSERT INTO employees (first_name, last_name, email, password)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connect_to_mysql(DATABASE).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = """
            SELECT * FROM employees WHERE employees.id = %(id)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def get_by_email(cls,data):
        query = """
            SELECT * FROM employees WHERE employees.email = %(email)s;
        """
        results = connect_to_mysql(DATABASE).query_db(query,data)
        if results:
            return cls(results[0])
        return False
    
    @classmethod
    def new_auth_request(cls,category,employee_id):
        attribute = ""
        print(category)
        category = int(category)
        match category:
            case 0:
                attribute = "sales_access"
            case 1:
                attribute = "inventory_access"
            case 2:
                attribute = "admin"
        query = """
            UPDATE employees
            SET """ + attribute + """ = 2
            WHERE id = %(employee_id)s;
        """
        data = {
            'attribute': attribute,
            'employee_id': employee_id
        }
        return connect_to_mysql(DATABASE).query_db(query,data)


    
    @staticmethod
    def valid_register(data):
        is_valid = True
        if len(data['first_name']) < 1:
            is_valid = False
            flash('First name required','reg_first_name')
        if len(data['last_name']) < 1:
            is_valid = False
            flash('Last name required','reg_last_name')
        if len(data['email']) < 1:
            is_valid = False
            flash('Email required','reg_email')
        elif not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('Email must be in valid format','reg_email')
        elif not '@bookstore.com' in data['email']:
            is_valid = False
            flash('only bookstore.com emails allowed','reg_email')
        else:
            potential_employee = Employee.get_by_email({'email':data['email']})
            if potential_employee:
                is_valid = False
                flash('Email already registered, contact Admin','reg_email')
        if len(data['password']) < 1:
            is_valid = False
            flash("Please provide password", 'reg_password')
        elif len(data['password']) < 8:
            is_valid = False
            flash("Password must be > 8 char", 'reg_password')
        elif data['password'] != data['confirm_pass']:
            is_valid = False
            flash("Passwords do not match", 'reg_password')
        return is_valid

        